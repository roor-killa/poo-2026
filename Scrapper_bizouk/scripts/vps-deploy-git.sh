#!/usr/bin/env bash
set -euo pipefail

# Deploiement manuel propre depuis Git.
# A lancer sur le VPS depuis le dossier Scrapper_bizouk clone depuis GitHub:
# bash scripts/vps-deploy-git.sh

BRANCH="${BRANCH:-rosambert}"
REPO_URL="${REPO_URL:-https://github.com/roor-killa/poo-2026.git}"
GIT_REPO_DIR="${GIT_REPO_DIR:-$HOME/RL_poo_2026}"
GIT_APP_DIR="${GIT_APP_DIR:-$GIT_REPO_DIR/Scrapper_bizouk}"
OLD_ARCHIVE_DIR="${OLD_ARCHIVE_DIR:-$HOME/RL_scrapper_bizouk}"

generate_secret() {
  if ! command -v openssl >/dev/null 2>&1; then
    echo "openssl est requis pour generer SCRAPER_API_KEY automatiquement." >&2
    echo "Installe openssl ou renseigne SCRAPER_API_KEY manuellement dans .env." >&2
    exit 1
  fi

  openssl rand -hex 32
}

echo "== Stop de l'ancien deploiement archive si present =="
if [ -f "$OLD_ARCHIVE_DIR/docker-compose.prod.yml" ]; then
  (
    cd "$OLD_ARCHIVE_DIR"
    docker compose -f docker-compose.prod.yml down
  )
else
  echo "Aucun ancien docker-compose.prod.yml dans $OLD_ARCHIVE_DIR"
fi

echo
echo "== Recuperation du code depuis GitHub =="
if [ ! -d "$GIT_REPO_DIR/.git" ]; then
  git clone -b "$BRANCH" "$REPO_URL" "$GIT_REPO_DIR"
else
  (
    cd "$GIT_REPO_DIR"
    git fetch origin "$BRANCH"
    git checkout "$BRANCH"
    git pull --ff-only origin "$BRANCH"
  )
fi

cd "$GIT_APP_DIR"

echo
echo "== Preparation du .env et du dossier data =="
mkdir -p data
cp -n .env.example .env

if ! grep -q "^SCRAPER_API_KEY=" .env; then
  echo "SCRAPER_API_KEY=$(generate_secret)" >> .env
fi

if grep -q "^SCRAPER_API_KEY=replace-with-a-long-random-secret" .env; then
  sed -i "s/^SCRAPER_API_KEY=.*/SCRAPER_API_KEY=$(generate_secret)/" .env
fi

echo
echo "== Rebuild et relance Docker =="
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps

echo
echo "== Test de sante =="
for attempt in $(seq 1 12); do
  if curl -fsS http://127.0.0.1:3005/api/health; then
    echo
    break
  fi

  if [ "$attempt" -eq 12 ]; then
    echo "Le health check a echoue apres plusieurs tentatives." >&2
    echo "Logs utiles:" >&2
    docker compose -f docker-compose.prod.yml logs --tail=80 backend frontend nginx >&2
    exit 1
  fi

  echo "Health check pas encore pret, nouvelle tentative dans 5s..."
  sleep 5
done

echo
echo "Deploiement termine."
echo "Cle API a saisir dans le frontend:"
grep "^SCRAPER_API_KEY=" .env
