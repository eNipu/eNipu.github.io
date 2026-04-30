#!/usr/bin/env bash
# Runs on the OCI VM. Pulls the latest image from GHCR and restarts the stack.
# Invoked over SSH by .github/workflows/deploy-oci.yml.

set -euo pipefail

cd /srv/site

# Load env (SITE_DOMAIN, ACME_EMAIL, SITE_IMAGE, etc.)
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

echo "[deploy] pulling latest images..."
docker compose pull

echo "[deploy] applying..."
docker compose up -d --remove-orphans

echo "[deploy] pruning old images..."
docker image prune -f

echo "[deploy] done."
docker compose ps
