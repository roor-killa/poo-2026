# Système de Suivi en Temps Réel des Bus Publics

Real-time public-bus tracking system.  
A FastAPI server ingests GPS positions from Raspberry Pi clients, stores them in PostgreSQL/PostGIS, and streams live snapshots to a Leaflet.js web map over WebSocket.

---

## Architecture overview

```
Raspberry Pi (client/)
  └─ gpsd → client/main.py ──HTTPS POST /api/v1/positions──► FastAPI (src/)
                                                               ├─ app/db/        SQLAlchemy models + repositories
                                                               ├─ src/services/  business logic (ETA, stop detect)
                                                               ├─ src/jobs/      asyncio offline-detector
                                                               ├─ src/ws/        WebSocket broadcaster (5 s)
                                                               └─ src/frontend/  public map + admin dashboard
nginx (docker-compose)
  ├─ :443   → public  REST + /ws/buses + static site
  └─ 127.0.0.1:8080 → admin REST + /ws/admin
```

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.11 |
| Docker + Docker Compose | 24 / v2 |
| gpsd (Pi only) | any |

---

## Quick start

### 1. Clone and configure

```bash
git clone <repo-url>
cd TPTransport

cp .env.example .env
# .env is read by docker-compose and by the server at runtime.
# Edit DATABASE_URL if you change the default credentials.
```

### 2. Start PostgreSQL + nginx

```bash
docker compose up -d db nginx
# Wait until the db health-check passes (~10 s):
docker compose ps
```

### 3. Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
# Applies 0001_initial_schema.py — creates all tables + PostGIS indexes
alembic upgrade head
```

### 5. Start the server

```bash
# Development
python main.py

# Production (single worker — required for shared in-process state)
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

The server starts two asyncio background tasks automatically:

- **OfflineDetector** — polls `bus_status` every 10 s, flips `is_online` after 30 s silence  
- **Broadcaster** — pushes full bus snapshots to all WebSocket clients every 5 s

### 6. Open the frontends

| URL | Description |
|-----|-------------|
| `http://localhost/` | Public Leaflet map (bus positions, ETAs) |
| `http://localhost:8080/admin/` | Admin dashboard (CRUD buses / routes / stops) |
| `http://localhost:8000/docs` | OpenAPI (Swagger) — dev only |
| `http://localhost:8000/healthz` | Health probe |

> When nginx is running on ports 80/443/8080, use those.  
> When running without nginx (dev), the FastAPI static files are served directly on port 8000.

---

## API reference

### Bus-client ingest

```
POST /api/v1/positions
Authorization: Bearer <api_token>
Content-Type: application/json

{
  "latitude": 48.8566,
  "longitude": 2.3522,
  "speed_kmh": 32.5,
  "heading": 270,
  "recorded_at": "2024-01-15T14:30:00Z"
}
```

### Public endpoints (rate-limited: 12 req/min per IP)

```
GET /api/v1/public/routes
GET /api/v1/public/routes/{route_id}
GET /api/v1/public/buses
GET /api/v1/public/buses/{bus_id}
GET /api/v1/public/stops/{stop_id}/arrivals
```

### Admin endpoints (localhost only — via port 8080)

```
POST   /api/v1/admin/buses
GET    /api/v1/admin/buses
GET    /api/v1/admin/buses/{bus_id}
PUT    /api/v1/admin/buses/{bus_id}
DELETE /api/v1/admin/buses/{bus_id}

POST   /api/v1/admin/routes
GET    /api/v1/admin/routes
GET    /api/v1/admin/routes/{route_id}
PUT    /api/v1/admin/routes/{route_id}
DELETE /api/v1/admin/routes/{route_id}

POST   /api/v1/admin/stops
GET    /api/v1/admin/stops
GET    /api/v1/admin/stops/{stop_id}
PUT    /api/v1/admin/stops/{stop_id}
DELETE /api/v1/admin/stops/{stop_id}
```

The `api_token` for a bus is returned **once** in the 201 response body and masked (`abc***xyz`) on all subsequent reads.

### WebSocket channels

```
ws://host/ws/buses       # public — SnapshotMessage every 5 s + BusOfflineEvent
ws://localhost:8080/ws/admin  # admin — same + token_masked, is_active, position count
```

Message types:

```json
// SnapshotMessage
{"type": "snapshot", "timestamp": "...", "buses": [...]}

// BusOfflineEvent
{"type": "bus_offline", "bus_id": "...", "last_seen_at": "..."}
```

---

## Raspberry Pi client deployment

### Requirements on the Pi

```bash
sudo apt install gpsd gpsd-clients python3-venv
sudo systemctl enable --now gpsd
```

### Install

```bash
sudo bash client/install.sh
```

The installer:
1. Creates a `bus-client` system user  
2. Copies the package to `/opt/bus-client/`  
3. Creates a Python venv and installs `gpsd-py3` + `requests`  
4. Installs the systemd unit  
5. Creates log and buffer directories  
6. Creates `/etc/bus-client/env` from the template  

### Configure and start

```bash
sudo nano /etc/bus-client/env
# Set:
#   BUS_API_TOKEN=<token from admin dashboard>
#   BUS_SERVER_URL=https://your-server.example.com

sudo systemctl enable --now bus-client
sudo journalctl -u bus-client -f
```

### What the client does

- Reads a GPS fix from `gpsd` every 5 s  
- POSTs `{latitude, longitude, speed_kmh, heading, recorded_at}` with Bearer auth  
- On network failure: buffers up to 1 000 fixes in a local SQLite WAL database  
- On reconnect: drains the buffer oldest-first before sending the live fix  
- Logs rotate daily, 7-day retention at `/var/log/bus-client/`

---

## TLS / nginx setup

The `certs` Docker volume must contain:
- `fullchain.pem` — server certificate chain  
- `privkey.pem` — private key  

```bash
# Example with Let's Encrypt:
certbot certonly --standalone -d bus.example.com
docker run --rm -v tptransport_certs:/certs \
  -v /etc/letsencrypt/live/bus.example.com:/src:ro \
  alpine sh -c "cp /src/fullchain.pem /src/privkey.pem /certs/"
```

---

## Project structure

```
TPTransport/
├── main.py                     # entry point (uvicorn runner)
├── docker-compose.yml
├── requirements.txt
├── alembic/                    # async migrations
│   ├── env.py
│   └── versions/0001_initial_schema.py
├── app/
│   └── db/
│       ├── base.py             # engine, AsyncSessionLocal, Base, get_session
│       ├── models/             # SQLAlchemy 2.x ORM models (7 tables)
│       └── repositories/       # data-access layer (CRUD + domain queries)
├── src/
│   ├── repositories/           # re-export facade over app/db/repositories/
│   ├── schemas/                # Pydantic v2 request/response models
│   ├── services/               # business logic (position ingest, ETA, geo)
│   ├── jobs/                   # asyncio background tasks
│   ├── api/
│   │   ├── app.py              # FastAPI application factory
│   │   ├── deps.py             # SessionDep, limiter, LocalhostGuard
│   │   ├── positions.py        # POST /api/v1/positions
│   │   ├── public/             # public read-only REST endpoints
│   │   └── admin/              # admin CRUD endpoints (localhost only)
│   ├── ws/
│   │   ├── broadcaster.py      # WebSocket hub + 5-s broadcast loop
│   │   └── router.py           # /ws/buses  /ws/admin
│   └── frontend/
│       ├── public/index.html   # Leaflet public map
│       └── admin/index.html    # admin dashboard
├── nginx/
│   └── nginx.conf
└── client/                     # Raspberry Pi embedded client (standalone)
    ├── main.py
    ├── config.py
    ├── gps.py
    ├── buffer.py
    ├── sender.py
    ├── logger.py
    ├── bus-client.service
    ├── install.sh
    └── requirements.txt
```

---

## Development notes

- **Single worker only**: the broadcaster and offline-detector are asyncio tasks sharing in-process state. Do not use `--workers N` with N > 1.
- **Geography WKB**: `geoalchemy2` WKB objects are only converted to `(lat, lon)` inside `src/services/geo.py`. Pydantic schemas never import `geoalchemy2`.
- **Admin security**: the admin API and `/ws/admin` are guarded by `require_localhost` — nginx binds them to `127.0.0.1:8080` so they are never exposed externally.
- **Token lifecycle**: `api_token` is a 96-character hex string generated with `secrets.token_hex(48)`. It is stored in plain text in the DB and shown once on bus creation.
