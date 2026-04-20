# RL Scrapper Bizouk

Application de scraping Bizouk avec:

- backend FastAPI pour lancer les scrapers;
- frontend Next.js pour choisir la region, le nombre de pages et exporter le JSON;
- nginx comme point d'entree;
- configuration Docker locale et production;
- protections CM9: cle API, rate limiting, CORS restreint, headers de securite et secrets hors Git.

## Lancement local

Depuis la racine du projet:

```powershell
copy .env.example .env
docker compose up -d --build
```

Dans `.env`, mets par exemple:

```text
SCRAPER_API_KEY=dev-local-scraper-key
```

L'interface locale est disponible sur:

```text
http://localhost:3005
```

Dans l'interface, saisis la meme cle API:

```text
dev-local-scraper-key
```

En production, il faut remplacer cette valeur par une vraie cle longue dans `.env`.

## Test API

```powershell
curl -H "X-API-Key: dev-local-scraper-key" "http://localhost:3005/api/scrape/events?pages=1&region=martinique&limit=3"
```

## Deploiement

Les consignes VPS sont dans `DEPLOYMENT.md`.

Ne jamais versionner de mot de passe, de cle SSH, de token ou de fichier `.env`.
Actuellement je peux déployer manuellement avec git pull sur le VPS, puis docker compose up -d --build. L’étape CI/CD consiste à automatiser exactement ces commandes via GitHub Actions après chaque push sur ma branche