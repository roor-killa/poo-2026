#!/usr/bin/env bash
set -euo pipefail

# Petit diagnostic VPS: il aide a savoir quel dossier existe et quels conteneurs tournent.
# A lancer depuis le VPS avec:
# bash scripts/vps-diagnose.sh

OLD_ARCHIVE_DIR="${OLD_ARCHIVE_DIR:-$HOME/RL_scrapper_bizouk}"
GIT_REPO_DIR="${GIT_REPO_DIR:-$HOME/RL_poo_2026}"
GIT_APP_DIR="${GIT_APP_DIR:-$GIT_REPO_DIR/Scrapper_bizouk}"

echo "== Dossiers detectes =="
for dir in "$OLD_ARCHIVE_DIR" "$GIT_APP_DIR"; do
  if [ -d "$dir" ]; then
    echo "OK  $dir"
  else
    echo "NO  $dir"
  fi
done

echo
echo "== Conteneurs RL_bizouk =="
docker ps -a --filter "name=RL_bizouk" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || true

echo
echo "== Compose ancien dossier archive =="
if [ -f "$OLD_ARCHIVE_DIR/docker-compose.prod.yml" ]; then
  (cd "$OLD_ARCHIVE_DIR" && docker compose -f docker-compose.prod.yml ps) || true
else
  echo "Aucun docker-compose.prod.yml trouve dans $OLD_ARCHIVE_DIR"
fi

echo
echo "== Compose nouveau dossier Git =="
if [ -f "$GIT_APP_DIR/docker-compose.prod.yml" ]; then
  (cd "$GIT_APP_DIR" && docker compose -f docker-compose.prod.yml ps) || true
else
  echo "Aucun docker-compose.prod.yml trouve dans $GIT_APP_DIR"
fi
