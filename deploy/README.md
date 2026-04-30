# Deploy &mdash; al-am.in on Oracle Cloud Free Tier

This folder contains everything needed to run the static site on a single
Oracle Cloud "Always Free" ARM VM behind Caddy + Cloudflare.

Architecture at a glance:

```
Visitor ---> Cloudflare (DNS + CDN + WAF) ---> Caddy (TLS, HTTP/3) ---> nginx (static files)
                                                       [Oracle Cloud Always-Free Ampere VM]
```

Dynamic bits (photography gallery, hire form) keep talking to Supabase
directly from the browser. No database runs on the VM.

---

## 1. One-time OCI VM setup

1. Create an Oracle Cloud "Always Free" account. Pick a home region close to
   most of your audience (e.g. `eu-frankfurt-1`).
2. Create a VCN with the default "Internet Connectivity" wizard.
3. Launch a **VM.Standard.A1.Flex** instance (Ampere ARM, Always Free eligible):
   - Image: Ubuntu 24.04 minimal aarch64
   - Shape: 2 OCPU, 12 GB RAM (within free tier)
   - Assign a **reserved public IP**
   - Upload an SSH public key you control (NOT the one used by CI)
4. In the VCN "Default Security List", add ingress rules:
   - TCP 80 from `0.0.0.0/0`
   - TCP 443 from `0.0.0.0/0`
   - UDP 443 from `0.0.0.0/0` (HTTP/3)
   - Keep TCP 22 open only to your admin IP range if possible.
5. SSH in as `ubuntu` and run:

   ```bash
   sudo apt-get update && sudo apt-get -y upgrade
   sudo apt-get install -y ca-certificates curl gnupg ufw fail2ban unattended-upgrades

   # Docker Engine + compose plugin
   curl -fsSL https://get.docker.com | sudo sh
   sudo usermod -aG docker ubuntu

   # Local firewall (belt & braces on top of VCN rules)
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 443/udp
   sudo ufw --force enable

   # Persistent storage for the site
   sudo mkdir -p /srv/site
   sudo chown -R ubuntu:ubuntu /srv/site
   ```

6. Create a dedicated `deploy` user whose SSH key will be held by GitHub Actions:

   ```bash
   sudo adduser --disabled-password --gecos "" deploy
   sudo usermod -aG docker deploy
   sudo mkdir -p /home/deploy/.ssh
   sudo chmod 700 /home/deploy/.ssh
   # paste the PUBLIC half of the CI keypair:
   sudo nano /home/deploy/.ssh/authorized_keys
   sudo chmod 600 /home/deploy/.ssh/authorized_keys
   sudo chown -R deploy:deploy /home/deploy/.ssh
   sudo chown -R deploy:deploy /srv/site
   ```

7. Harden SSH (`/etc/ssh/sshd_config.d/99-hardening.conf`):

   ```
   PermitRootLogin no
   PasswordAuthentication no
   KbdInteractiveAuthentication no
   ```
   Then `sudo systemctl reload ssh`.

8. On the VM, drop the `docker-compose.yml`, `Caddyfile`, `update.sh`, and a
   `.env` in `/srv/site/`. Only `.env` is machine-specific:

   ```bash
   cd /srv/site
   cat > .env <<'EOF'
   SITE_DOMAIN=al-am.in
   ACME_EMAIL=hire.credibly374@passinbox.com
   SITE_IMAGE=ghcr.io/OWNER/REPO:latest
   EOF
   chmod 600 .env
   ```

   Copy in the repo files:

   ```bash
   curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/deploy/docker-compose.yml -o docker-compose.yml
   curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/deploy/Caddyfile       -o Caddyfile
   curl -sL https://raw.githubusercontent.com/OWNER/REPO/main/deploy/update.sh       -o update.sh
   chmod +x update.sh
   ```

9. If the GHCR image is private (it is public by default for public repos),
   log Docker into GHCR as the `deploy` user with a read-only PAT:

   ```bash
   echo $GHCR_READ_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin
   ```

10. First boot:

    ```bash
    cd /srv/site
    ./update.sh
    ```

    Caddy will obtain a Let's Encrypt certificate automatically once DNS
    points at this VM.

## 2. DNS / CDN on Cloudflare (free plan)

1. Add `al-am.in` to Cloudflare; update registrar nameservers.
2. Add DNS records (proxied = orange cloud ON):
   - `A    al-am.in       -> <OCI reserved IP>`
   - `A    www.al-am.in   -> <OCI reserved IP>`
3. SSL/TLS mode: **Full (strict)**.
4. Enable: Always Use HTTPS, Automatic HTTPS Rewrites, Brotli, Early Hints,
   Tiered Cache, HTTP/3.
5. Page rule: `al-am.in/*` &rarr; Cache Level: Cache Everything; Edge TTL
   tuned per asset via origin headers.
6. Security: enable Bot Fight Mode and the free Managed WAF rules.
7. Analytics: enable Cloudflare Web Analytics for the zone.

## 3. CI/CD secrets (GitHub repo &rarr; Settings &rarr; Secrets and variables &rarr; Actions)

Required:

- `OCI_HOST`        &mdash; VM IP or hostname
- `OCI_USER`        &mdash; `deploy`
- `OCI_SSH_KEY`     &mdash; private half of the CI keypair (PEM, no passphrase)
- `OCI_SSH_PORT`    &mdash; (optional, defaults to 22)

Also enable in repo settings:

- "Secret scanning" and "Push protection" (free for public repos).
- Branch protection on `main`: required status checks = `validate`,
  `build-and-push`; no force push.

## 4. Monitoring

- UptimeRobot: HTTPS monitor on `https://al-am.in/` every 5 minutes; email
  alerts to `hire.credibly374@passinbox.com`.
- Cloudflare Web Analytics: traffic dashboard.
- VM: `docker compose logs -f --tail=200` when debugging.

## 5. Rollback

Every deploy tags the image with the commit SHA. To roll back:

```bash
ssh deploy@<VM>
cd /srv/site
sed -i 's|SITE_IMAGE=.*|SITE_IMAGE=ghcr.io/OWNER/REPO:sha-<previous>|' .env
./update.sh
```
