# RTG - MVP Suivi Bus Temps Reel

Ce dossier contient une implementation MVP du cahier des charges RTG:
- collecte de positions GPS (WebSocket agent)
- diffusion temps reel (WebSocket live)
- API REST centrale (buses, lines, arrivals, alerts, KPI)
- endpoint IA (stub) pour requetes en langage naturel
- frontend dashboard local (HTML/CSS/JS) connecte au backend
- base de donnees PostgreSQL pour persistance des alertes et donnees de reference

## Structure

- `api/app/main.py`: point d entree FastAPI
- `api/app/models.py`: modeles de donnees Pydantic
- `api/app/store.py`: stockage memoire thread-safe et donnees seed
- `api/app/database.py`: connexion SQLAlchemy
- `api/app/entities.py`: tables SQLAlchemy
- `api/app/repository.py`: operations base de donnees
- `api/app/services.py`: calcul ETA, KPI, traitement evenements
- `api/app/config.py`: configuration applicative
- `api/requirements.txt`: dependances API
- `frontend/index.html`: dashboard frontend
- `frontend/app.js`: appels API, affichage KPI/bus/lignes, formulaires
- `frontend/styles.css`: styles du dashboard

## Lancer le backend

```bash
cd akonou/Transport
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
pip install -r api/requirements.txt
uvicorn api.app.main:app --reload --port 8000
```

## Lancer le frontend

Dans un second terminal:

```bash
cd akonou/Transport/frontend
python -m http.server 5500
```

Puis ouvrir:
- `http://127.0.0.1:5500`

Le frontend appelle le backend sur `http://127.0.0.1:8000` en mode local Python, et `http://127.0.0.1:18000` en mode Docker.

## Lancer avec Docker

Depuis `akonou/Transport`:

```bash
docker compose up --build
```

Acces:
- Frontend: `http://127.0.0.1:18080`
- Backend API: `http://127.0.0.1:18000`

Arreter:

```bash
docker compose down
```

Fichiers Docker:
- `api/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

La base PostgreSQL est exposee sur `localhost:5432` (db: rtg, user: rtg, password: rtg en dev).

## CDC et livrables

- CDC complet: `docs/CDC_RTG_MVP.md`
- MVP applicatif: backend FastAPI + frontend dashboard
- Docker dev: `docker-compose.yml`
- Docker prod: `docker-compose.prod.yml`

## CI/CD et deploiement production

### CI
- Workflow: `.github/workflows/ci.yml`
- Etapes: installation deps, tests pytest, build images Docker

### CD
- Workflow: `.github/workflows/cd.yml`
- Etapes: build/push images sur GHCR, deploiement SSH sur VM

Secrets GitHub requis:
- `PROD_HOST`
- `PROD_USER`
- `PROD_SSH_KEY`

### Infra prod
- Reverse proxy: `infra/nginx/nginx.conf`
- Variables image: `.env.prod` (voir `.env.prod.example`)
- Script helper: `scripts/deploy_prod.sh`

Execution manuelle prod:

```bash
cd akonou/Transport
cp .env.prod.example .env.prod
# editer les tags d'image
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## Endpoints REST MVP

- `GET /health`
- `GET /api/v1/buses`
- `GET /api/v1/buses/{id}/position`
- `GET /api/v1/lines`
- `GET /api/v1/stops/{id}/arrivals`
- `POST /api/v1/alerts`
- `GET /api/v1/analytics/kpi`
- `POST /api/v1/ai/query`

## WebSocket MVP

- `WS /ws/agent/{bus_id}?token=agent-secret`
  - Recoit des payloads GPS
  - Exemple payload:
```json
{
  "bus_id": "BUS-001",
  "lat": 9.55,
  "lng": -13.68,
  "speed": 35.2,
  "heading": 120,
  "ts": 1744000000,
  "sig": "JWT"
}
```

- `WS /ws/live/{line_id}`
  - Diffuse les updates bus pour la ligne demandee

## Notes importantes

- Cette version est un MVP avec persistance PostgreSQL pour les alertes et les donnees de reference.
- Le cahier des charges cible Redis/PostgreSQL/TimescaleDB: ici le design est prepare pour remplacer facilement le store memoire par une persistence reelle.
- L endpoint IA est un stub (retour structure) et peut etre branche plus tard sur Claude API.
