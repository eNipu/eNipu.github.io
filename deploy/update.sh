#!/usr/bin/env bash
# Runs on the OCI VM. Pulls the latest al-am.in image from GHCR and restarts
# the compose stack. Expects the shared `web-edge` docker network and the
# existing host-level Caddy (e.g. caddy-staging) to already be configured.

set -euo pipefail

cd /srv/site

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

# Make sure the shared edge network exists. Safe to run repeatedly.
if ! docker network inspect web-edge >/dev/null 2>&1; then
  echo "[deploy] creating shared web-edge network..."
  docker network create web-edge
fi

echo "[deploy] pulling latest image..."
docker compose pull

echo "[deploy] applying..."
docker compose up -d --remove-orphans

echo "[deploy] pruning old images..."
docker image prune -f

echo "[deploy] done."
docker compose ps
