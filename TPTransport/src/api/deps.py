"""Shared FastAPI dependencies and slowapi rate-limiter configuration."""

from __future__ import annotations

from ipaddress import ip_address
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session

# ---------------------------------------------------------------------------
# DB session dependency
# ---------------------------------------------------------------------------

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ---------------------------------------------------------------------------
# slowapi rate-limiter
# Spec §3.2: 1 req / 5 s per IP = 12 req/min on public endpoints.
# The Limiter instance is attached to app.state.limiter in app.py.
# ---------------------------------------------------------------------------

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=[])

PUBLIC_RATE = "12/minute"  # 1 req / 5 s


# ---------------------------------------------------------------------------
# Localhost-only guard for admin endpoints (spec §1.3)
# ---------------------------------------------------------------------------

_LOCALHOST = {"127.0.0.1", "::1"}


def require_localhost(request: Request) -> None:
    """Dependency that rejects requests not coming from localhost."""
    client_host = request.client.host if request.client else ""

    # Direct (no proxy)
    if client_host in _LOCALHOST:
        return

    # Behind Docker/nginx the client becomes a private gateway/container IP.
    # Admin is still protected externally by docker-compose publishing the
    # admin listener only to 127.0.0.1 on the host.
    try:
        if client_host and ip_address(client_host).is_private:
            return
    except ValueError:
        pass

    if client_host not in _LOCALHOST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin API is only accessible from localhost.",
        )


LocalhostGuard = Depends(require_localhost)
