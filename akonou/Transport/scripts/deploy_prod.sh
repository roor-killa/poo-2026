#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/rtg-transport/akonou/Transport"

if [[ ! -f "$APP_DIR/.env.prod" ]]; then
  echo "Missing $APP_DIR/.env.prod"
  exit 1
fi

cd "$APP_DIR"
docker compose -f docker-compose.prod.yml --env-file .env.prod pull
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d

echo "Production deploy done"
