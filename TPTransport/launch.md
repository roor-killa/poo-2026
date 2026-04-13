# Launch guide (Windows)

This project is designed to run:
- **PostgreSQL/PostGIS** via Docker (container)
- **FastAPI** via Python (local process)

You can run it in two ways:
- **Option A (recommended): all-in-docker** — `db` + `api` + `nginx` (HTTPS)
- **Option B: DB in Docker + API locally** — simplest when you don’t want HTTPS

---

## 0) Prereqs

- Docker Desktop (WSL2 backend)
- Python 3.11+ (project spec)

Quick sanity checks:

```powershell
docker version
wsl -l -v
```

You should see a **Server** section in `docker version` and a `docker-desktop` WSL distro in `wsl -l -v`.

---

## 1) Configure environment

From the repo root:

```powershell
cd "c:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TPTransport"
Copy-Item .env.example .env -Force
```

Defaults work out of the box:

- `DATABASE_URL=postgresql+asyncpg://bus:bus@localhost:5432/bus_tracking`

---

## 2) Start PostGIS (Docker)

```powershell
docker-compose up -d db
docker-compose ps
```

Wait until `db` is shown as `healthy`.

---

## 3) Create venv + install Python deps

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## 4) Run database migrations

```powershell
alembic upgrade head
```

---

## 5) Start the API server

Development:

```powershell
python main.py
```

Alternative (explicit):

```powershell
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --workers 1
```

Note: keep **`--workers 1`** because the broadcaster/offline-detector keep in-process state.

---

## 6) Open the app

- Public UI: http://localhost:8000/
- Admin UI:  http://localhost:8000/admin/
- Swagger:   http://localhost:8000/docs
- Health:    http://localhost:8000/healthz

---

# Option A — all-in-docker (nginx + HTTPS)

This uses:
- `db` (PostGIS)
- `api` (FastAPI/Uvicorn)
- `nginx` (reverse proxy)
- `certs-init` (one-shot helper that creates a self-signed `localhost` cert in the `certs` volume)

Start everything:

```powershell
cd "c:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TPTransport"
docker-compose up -d --build
docker-compose ps
```

Open:

- Public UI (HTTPS): https://localhost/
- Health (HTTPS): https://localhost/healthz
- Admin (localhost-only): http://127.0.0.1:8080/

Notes:

- The cert is self-signed; your browser will show a warning the first time.
- Admin remains bound to `127.0.0.1:8080` per spec (not exposed externally).

---

## 7) Stop everything

- Stop API: `Ctrl+C` in the API terminal
- Stop DB container:

```powershell
docker-compose down
```

---

## Docker “from scratch” recovery (if an update broke it)

Start with the least destructive fix:

```powershell
wsl --shutdown
```

Then start Docker Desktop again and re-check:

```powershell
docker version
```

If Docker Desktop is still broken and you truly want a full reset (this **deletes all images/volumes**):

```powershell
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```

Then launch Docker Desktop; it will recreate its WSL distros.
