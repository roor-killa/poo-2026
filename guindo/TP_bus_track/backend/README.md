# 🚌 BusTrack MQ — Suivi temps réel des bus en Martinique

API FastAPI de simulation et suivi GPS des bus en Martinique.  
Stack : **Python POO + FastAPI + PostgreSQL + WebSocket + Docker + CI/CD GitHub Actions**

---

## 🚀 Lancer en local (Docker)

```bash
cp .env.example .env
docker-compose up --build
```

- API : http://localhost:8000  
- Swagger : http://localhost:8000/docs  
- WebSocket : ws://localhost:8000/ws/positions

---

## 🧪 Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=.
```

---

## 📡 Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/lignes` | Liste des lignes |
| GET | `/api/lignes/{id}` | Détail d'une ligne |
| GET | `/api/bus` | Position de tous les bus |
| GET | `/api/bus/{id}` | Détail d'un bus |
| WS | `/ws/positions` | Flux temps réel |
| POST | `/api/notifications/subscribe` | Abonnement push |
| GET | `/health` | Santé de l'API |

---

## 🔔 Notifications Push (Web Push / VAPID)

Générer les clés VAPID :

```bash
pip install py-vapid
vapid --gen
```

Copier les clés dans `.env` :

```
VAPID_PRIVATE_KEY=<private_key>
VAPID_PUBLIC_KEY=<public_key>
```

---

## 🏗️ Structure

```
bustrack_mq/
├── models/          # POO : Bus, Ligne, Arrêt
├── simulation/      # Moteur GPS (BackgroundTask)
├── api/
│   ├── routes/      # lignes, bus, websocket, notifications
│   └── schemas.py   # Schémas Pydantic
├── db/              # SQLAlchemy models + session
├── core/            # Config (Settings)
├── tests/           # pytest
├── main.py          # Point d'entrée FastAPI
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci-cd.yml
```

---

## 🚢 Déploiement (Railway)

1. Créer un projet Railway  
2. Ajouter les variables d'environnement (voir `.env.example`)  
3. Ajouter le secret `RAILWAY_TOKEN` dans GitHub  
4. Pousser sur `main` → le pipeline CI/CD déploie automatiquement
