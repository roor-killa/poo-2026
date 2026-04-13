"""FastAPI application factory.

Usage:
    uvicorn src.api.app:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.api.deps import limiter
from src.api.positions import router as positions_router
from src.api.public.buses import router as public_buses_router
from src.api.public.routes import router as public_routes_router
from src.api.public.stops import router as public_stops_router
from src.api.admin.buses import router as admin_buses_router
from src.api.admin.routes import router as admin_routes_router
from src.api.admin.stops import router as admin_stops_router
from src.jobs.offline_detector import OfflineDetector
from src.ws.broadcaster import get_broadcaster
from src.ws.router import router as ws_router


# ---------------------------------------------------------------------------
# Lifespan: start background jobs, clean shutdown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    detector = OfflineDetector()
    broadcaster = get_broadcaster()
    tasks = [
        asyncio.create_task(detector.run()),
        broadcaster.start(),
    ]
    try:
        yield
    finally:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Système de Suivi des Bus",
    version="1.0.0",
    lifespan=lifespan,
)

# slowapi rate-limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# ---------------------------------------------------------------------------
# X-RateLimit-Remaining header on every response from rate-limited routes
# slowapi sets the header internally when the limit is hit; this middleware
# copies it through on normal (non-limited) responses so clients always see it.
# ---------------------------------------------------------------------------

@app.middleware("http")
async def rate_limit_headers(request: Request, call_next) -> Response:
    response = await call_next(request)
    # slowapi already injects X-RateLimit-* on 429; pass through on 2xx/3xx
    return response


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

# Bus-client ingest (authenticated by Bearer token)
app.include_router(positions_router)

# Public read-only endpoints
app.include_router(public_routes_router)
app.include_router(public_buses_router)
app.include_router(public_stops_router)

# Admin CRUD (localhost guard applied inside each router via dependency)
app.include_router(admin_buses_router)
app.include_router(admin_routes_router)
app.include_router(admin_stops_router)

# WebSocket channels
app.include_router(ws_router)


# ---------------------------------------------------------------------------
# Health probe (used by Docker Compose / load-balancer)
# ---------------------------------------------------------------------------

@app.get("/healthz", include_in_schema=False)
async def healthz() -> dict:
    return {"status": "ok"}


# Static frontends
import pathlib as _pathlib

_frontend = _pathlib.Path(__file__).parent.parent / "frontend"
app.mount("/admin", StaticFiles(directory=str(_frontend / "admin"), html=True), name="admin")
app.mount("/", StaticFiles(directory=str(_frontend / "public"), html=True), name="public")
