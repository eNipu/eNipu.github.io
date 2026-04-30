# Deploy &mdash; al-am.in on shared Oracle Cloud VM

This site is designed to **coexist** with another project already running
on your Oracle Cloud Always-Free VM that uses a host-level Caddy
container (`caddy-staging`) for TLS on ports 80/443.

We do NOT start a second Caddy. Instead we:

1. Create a shared docker network (`web-edge`).
2. Attach the existing `caddy-staging` container to that network.
3. Run only the al-am.in nginx container on that network, with no host
   ports published.
4. Add two new site blocks to `/home/ubuntu/caddy/Caddyfile` so the
   shared Caddy terminates TLS for `al-am.in` and `www.al-am.in` and
   reverse-proxies to the al-am.in nginx container by DNS name
   (`al-am-in-web:80`).

```
Visitor --> Cloudflare --> caddy-staging (owns :80/:443, shared Let's Encrypt store)
                                    |--- staging.130.61.76.180.sslip.io -> norii storefront
                                    |--- al-am.in                         -> al-am-in-web (nginx)
                                    `--- www.al-am.in                     -> 301 to apex
```

Dynamic bits (photography gallery, hire form) keep talking to Supabase
directly from the browser. No database runs on the VM.

---

## 1. One-time VM setup (additive; does not touch the existing stack)

SSH in as `ubuntu` and run:

```bash
# Shared edge network (no-op if it already exists)
docker network inspect web-edge >/dev/null 2>&1 \
  || docker network create web-edge

# Attach the existing Caddy to it
docker network connect web-edge caddy-staging || true

# Dedicated site directory
sudo mkdir -p /srv/site
sudo chown -R ubuntu:ubuntu /srv/site
```

Create a dedicated `deploy` user for GitHub Actions SSH (skip if you
already have one from the other project):

```bash
sudo adduser --disabled-password --gecos "" deploy
sudo usermod -aG docker deploy
sudo mkdir -p /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo nano /home/deploy/.ssh/authorized_keys   # paste CI public key
sudo chmod 600 /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chown -R deploy:deploy /srv/site
```

Drop the al-am.in deploy files in `/srv/site/`:

```bash
cd /srv/site
curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/deploy/docker-compose.yml -o docker-compose.yml
curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/deploy/update.sh           -o update.sh
chmod +x update.sh

cat > .env <<'EOF'
SITE_DOMAIN=al-am.in
SITE_IMAGE=ghcr.io/OWNER/REPO:latest
EOF
chmod 600 .env
```

If your GHCR image is private, log in as the `deploy` user once with a
read-only PAT:

```bash
echo "$GHCR_READ_PAT" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

## 2. Extend the existing Caddyfile

Open `/home/ubuntu/caddy/Caddyfile` and append the contents of
`deploy/Caddyfile` from this repo (two blocks: `al-am.in` and
`www.al-am.in`). Then reload Caddy WITHOUT restarting other sites:

```bash
docker exec caddy-staging caddy reload --config /etc/caddy/Caddyfile
```

Let's Encrypt will issue certs for `al-am.in` and `www.al-am.in` on the
first successful request, reusing the existing `caddy-staging` cert
storage (no rate-limit collision with the other site).

## 3. First boot of the al-am.in stack

```bash
cd /srv/site
./update.sh
```

Verify:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl -I https://al-am.in/
```

The al-am.in container exposes no host ports &mdash; only the shared
Caddy can reach it, over the `web-edge` network.

## 4. DNS / CDN (Cloudflare free plan)

1. Add `al-am.in` to Cloudflare; update registrar nameservers.
2. Records (proxied, orange cloud ON):
   - `A    al-am.in       -> <OCI reserved IP>`
   - `A    www.al-am.in   -> <OCI reserved IP>`
3. SSL/TLS mode: **Full (strict)**.
4. Enable: Always Use HTTPS, Automatic HTTPS Rewrites, Brotli, Early
   Hints, Tiered Cache, HTTP/3.
5. Page rule: `al-am.in/*` &rarr; Cache Everything (origin sets TTL).
6. Security: Bot Fight Mode on, Managed WAF rules enabled.
7. Analytics: enable Cloudflare Web Analytics.

## 5. CI/CD secrets (GitHub repo &rarr; Settings &rarr; Secrets and variables &rarr; Actions)

- `OCI_HOST`        &mdash; VM IP or hostname (e.g. `130.61.76.180`)
- `OCI_USER`        &mdash; `deploy`
- `OCI_SSH_KEY`     &mdash; private half of the CI keypair (PEM)
- `OCI_SSH_PORT`    &mdash; optional, defaults to 22

Also enable in repo settings:

- Secret scanning + Push protection (free on public repos).
- Branch protection on `main`: required status checks = `validate`,
  `build-and-push`.

## 6. Monitoring

- UptimeRobot HTTPS monitor on `https://al-am.in/`, 5-minute interval.
- Cloudflare Web Analytics for the zone.
- `docker compose logs -f --tail=200` when debugging.

## 7. Rollback

Every deploy tags the image with the commit SHA. To roll back:

```bash
ssh deploy@<VM>
cd /srv/site
sed -i 's|SITE_IMAGE=.*|SITE_IMAGE=ghcr.io/OWNER/REPO:sha-<previous>|' .env
./update.sh
```

## Why this will not conflict with the existing deployment

| Resource                | Owner                              | Conflict? |
|-------------------------|------------------------------------|-----------|
| Host ports 80/443 TCP   | `caddy-staging` (unchanged)        | No        |
| Host port 443 UDP       | `caddy-staging` (unchanged)        | No        |
| `web-edge` docker net   | Shared, both stacks attached       | No        |
| Container names         | Prefixed `al-am-in-*`              | No        |
| Let's Encrypt certs     | Issued by the one `caddy-staging`  | No rate limit collision |
| Compose project name    | `al-am-in` (distinct from `norii`) | No        |
| `/srv/site` vs `/opt/norii` | Separate directories           | No        |
| VM CPU / RAM            | 4 OCPU / 24 GB free-tier headroom  | Plenty    |
