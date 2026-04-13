# CLAUDE.md — Folder Ownership & Agent Rules

## Project: Système de Suivi en Temps Réel des Bus Publics

See `spec_suivi_bus.md` for the full technical specification.

---

## Completion status

| Layer | Status | Location |
|---|---|---|
| Docker Compose + PostGIS + nginx | Done | `docker-compose.yml`, `nginx/nginx.conf` |
| Alembic migration (initial schema) | Done | `alembic/versions/0001_initial_schema.py` |
| SQLAlchemy async models (7 tables) | Done | `app/db/models/` |
| DB engine + session factory | Done | `app/db/base.py` |
| Repository implementations | Done | `app/db/repositories/` |
| Repository re-export layer | Done | `src/repositories/` |
| Pydantic schemas (all endpoints + WS) | Done | `src/schemas/` |
| FastAPI routers | Done | `src/api/` |
| Business logic / services | Done | `src/services/` |
| Offline-detection background job | Done | `src/jobs/offline_detector.py` |
| ETA calculation | Done | `src/services/eta.py` |
| WebSocket broadcaster | Done | `src/ws/` |
| Admin frontend | Done | `src/frontend/admin/index.html` |
| Public frontend | Done | `src/frontend/public/index.html` |
| nginx config | Done | `nginx/nginx.conf` |
| Embedded bus client (Raspberry Pi) | Done | `client/` |

---

## Folder ownership rules

These rules prevent agents from trampling each other's work.

### `app/db/models/` — ORM models
- **Owner:** DB layer agent (completed).
- **Do not** regenerate, move, or delete these files.
- **Do not** add business logic here; models are plain data containers.
- One file per table. Relationships use `TYPE_CHECKING` imports to avoid circular deps.
- Geography columns use `geoalchemy2.Geography`; the service layer converts WKB → lat/lon.

### `app/db/repositories/` — Repository layer
- **Owner:** DB layer agent (completed).
- **Do not** add HTTP concerns (request/response objects) here.
- Repositories receive and return SQLAlchemy model instances, never Pydantic schemas.
- Every public method must be `async`.

### `app/db/base.py` — Engine & session
- **Owner:** DB layer agent (completed).
- `DATABASE_URL` is read from the `DATABASE_URL` environment variable.
- `get_session()` is the FastAPI dependency; do not create a second session factory.

### `alembic/` — Migrations
- **Owner:** DB layer agent (completed).
- New migrations must be added as new revision files; never edit `0001_*`.
- `env.py` uses async mode via `asyncpg`; do not switch to sync.

### `src/repositories/` — Repository re-export layer
- **Owner:** DB layer agent (completed).
- Contains only one-line re-exports that forward to `app/db/repositories/`.
- **Do not** add implementation logic here; keep it as a stable public facade.
- When the rest of the codebase needs a repository, import from here:
  `from src.repositories import BusRepository`

### `nginx/` — Reverse-proxy configuration
- **Owner:** DB layer agent (completed).
- `nginx.conf` maps public port 443, HTTP-to-HTTPS redirect on 80, and admin-only
  `127.0.0.1:8080` — do not expose admin endpoints on other ports.
- TLS certificates are expected at `/etc/nginx/certs/{fullchain,privkey}.pem`
  mounted via the `certs` Docker volume — do not commit real certs.
- The upstream is named `api_backend` and points to `api:8000`.  When the
  FastAPI service is added to `docker-compose.yml`, use the service name `api`.

### `src/schemas/` — Pydantic schemas
- **Owner:** Foundations agent (completed).
- **Do not** embed SQLAlchemy types here; schemas are pure Pydantic.
- When an ORM model uses `Geography`, the **service layer** extracts `lat`/`lon`
  before constructing a schema — schemas never import `geoalchemy2`.
- All `from_attributes=True` models must match the corresponding ORM model field names.

### `src/services/` — Business logic (completed)
- **Owner:** services agent (completed).
- `geo.py` — pure geographic helpers (WKB → lat/lon, haversine, WKT builder). No DB access.
- `eta.py` — pure ETA and progress_pct formulae (no DB access). Safe to unit-test in isolation.
- `position_service.py` — full ingest pipeline: auth, persist, stop detection, EMA trigger, ETA, status upsert.
- `bus_service.py` — read-side: assembles `BusPublicRead` / `BusDetailRead` from ORM rows; converts all Geography WKB → lat/lon here.
- Services call `src/repositories/` only — never `app/db/repositories/` directly.
- Services return Pydantic schemas, never ORM instances.

### `src/jobs/` — Background asyncio tasks (completed)
- **Owner:** services agent (completed).
- `offline_detector.py` — runs every 10 s per spec §5.4. Flip `is_online` on rows where
  `(now - last_seen_at) > OFFLINE_THRESHOLD_S` (30 s). Log stale buses at 300 s.
- Instantiate `OfflineDetector` in the FastAPI lifespan; `asyncio.create_task(detector.run())`.
- **Do not** add HTTP logic here. The job only talks to `BusStatusRepository`.

### `src/api/` — FastAPI routers (completed)
- **Owner:** API agent (completed).
- `app.py` — FastAPI factory, mounts all routers, attaches slowapi, starts `OfflineDetector` in lifespan.
- `deps.py` — shared dependencies: `SessionDep`, `limiter`, `PUBLIC_RATE = "12/minute"`, `LocalhostGuard`.
- `positions.py` — `POST /api/v1/positions` (Bearer token, delegates to `PositionService`).
- `public/routes.py` — `GET /api/v1/public/routes`, `/routes/{id}` (rate-limited).
- `public/buses.py` — `GET /api/v1/public/buses`, `/buses/{id}` (rate-limited, delegates to `BusService`).
- `public/stops.py` — `GET /api/v1/public/stops/{id}/arrivals` (rate-limited).
- `admin/buses.py` — full CRUD, `LocalhostGuard`, token exposed once on POST then masked.
- `admin/routes.py` — full CRUD with stop-sequence replace on PUT.
- `admin/stops.py` — POST / PUT / DELETE (hard delete, cascades `route_stops`).
- **Do not** call repositories from `public/` routers directly — use services.
- **Do not** add business logic here; if logic grows, move it to `src/services/`.

### `src/services/` — Business logic (TODO)
- One service per aggregate root (`bus_service.py`, `route_service.py`, …).
- Services call repositories and return Pydantic schemas (not ORM instances).
- `eta.py` implements the ETA formula from spec §5.2 — keep it pure (no DB calls).

### `src/ws/` — WebSocket broadcaster (completed)
- **Owner:** WS agent (completed).
- `broadcaster.py` — `Broadcaster` singleton; two `set[WebSocket]` (public / admin).
  - `start()` returns an `asyncio.Task` for the 5-s broadcast loop.
  - Detects online→offline transitions per bus and emits `BusOfflineEvent` once.
  - `get_broadcaster()` returns the module-level singleton.
- `router.py` — `@router.websocket("/ws/buses")` and `"/ws/admin"` (localhost guard).
- Both channels are started in `src/api/app.py` lifespan alongside `OfflineDetector`.
- **Do not** push HTTP/REST logic here; keep it pure WebSocket.

### `src/frontend/` — HTML/JS frontends (completed)
- **Owner:** WS/frontend agent (completed).
- `public/index.html` — fullscreen Leaflet map, line selector, bus interpolation animation (lerp over 5-s interval), stop-click ETA panel, offline badge, auto-reconnect WS.
- `admin/index.html` — sidebar nav, Leaflet map + sortable bus table (dashboard), CRUD pages for buses/routes/stops via modal forms, token shown once on creation.
- Served by FastAPI `StaticFiles` mounts in `app.py`: `/` → `public/`, `/admin` → `admin/`.
- **Do not** use frameworks (React, Vue) — plain HTML/CSS/JS only.
- **Do not** hardcode IP addresses — use `location.host` for WS URLs.

### `src/jobs/` — Background asyncio tasks (TODO)
- `offline_detector.py` — runs every 10 s, marks buses offline per spec §5.4.
- `speed_updater.py` — updates `segment_speeds` EMA on bus arrival at stop.

---

### `client/` — Embedded Raspberry Pi client (completed)
- **Owner:** client agent (completed).
- **Completely independent** of the `src/` / `app/` trees — no shared imports.
- `config.py` — all tunables read from environment variables; deployed via `/etc/bus-client/env`.
- `gps.py` — thin wrapper around `gpsd-py3`; returns a `GpsFix` dataclass or `None` on no-lock.
- `buffer.py` — `OfflineBuffer` over SQLite (WAL mode); FIFO ring-buffer capped at `BUFFER_MAX_ENTRIES`. `push / drain / ack` API.
- `sender.py` — `Sender` posts to `POST /api/v1/positions`; maps 401/422 to discard-without-buffering, 429/5xx/network to buffer.  After each successful send, drains the buffer in 50-row batches until it empties or the server fails again.
- `logger.py` — `TimedRotatingFileHandler` (midnight, 7 backups) + stderr handler.
- `main.py` — main loop: read fix → send → sleep for remainder of 5 s interval. SIGTERM / SIGINT handled for clean shutdown (systemd `ExecStop`).
- `bus-client.service` — `Restart=always`, `RestartSec=5`, `EnvironmentFile=/etc/bus-client/env`, `MemoryMax=128M`, `NoNewPrivileges=true`, `ProtectSystem=strict`.
- `install.sh` — idempotent installer: creates `bus-client` system user, deploys to `/opt/bus-client/`, creates venv, installs systemd unit, provisions directories.
- **Do not** import anything from `src/` or `app/` — the client runs on a Pi with no server dependencies.

## Cross-cutting conventions

- **Python version:** 3.11+
- **Async throughout:** every function that touches the DB must be `async`.
- **No raw SQL in routers or services** — use repositories for all DB access.
- **UUID primary keys everywhere** — pass as `uuid.UUID`, not strings.
- **Timestamps** — always timezone-aware (`datetime` with `tz=timezone.utc`).
- **Secrets** — `api_token` is never logged; in admin responses it is shown once
  on creation, masked (`abc***xyz`) on subsequent reads.
- **Rate limiting** — applied in routers via `slowapi`; not in services.
