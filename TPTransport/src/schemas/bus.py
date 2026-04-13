"""Schemas for the buses resource (admin CRUD + public read)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import LocationOut, RouteRef, StopWithEta
from src.schemas.position import PositionCreate


# ---------------------------------------------------------------------------
# Request bodies
# ---------------------------------------------------------------------------

class BusCreate(BaseModel):
    """Admin POST /buses body.
    The API token is generated server-side and returned once in BusAdminRead.
    """

    code: str = Field(..., max_length=20)
    label: str | None = Field(None, max_length=80)
    route_id: UUID | None = None


class BusUpdate(BaseModel):
    """Admin PUT /buses/{id} body — all fields optional."""

    code: str | None = Field(None, max_length=20)
    label: str | None = Field(None, max_length=80)
    route_id: UUID | None = None
    is_active: bool | None = None


# ---------------------------------------------------------------------------
# Response bodies — admin
# ---------------------------------------------------------------------------

class BusAdminRead(BaseModel):
    """Full bus record for admin endpoints.

    api_token is included on creation only (the router should strip it on
    subsequent reads — schema carries the field, router decides visibility).
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    label: str | None
    route: RouteRef | None
    api_token: str
    is_active: bool
    created_at: datetime
    last_seen_at: datetime | None = None
    positions_last_hour: int = 0


# ---------------------------------------------------------------------------
# Response bodies — public
# ---------------------------------------------------------------------------

class BusPublicRead(BaseModel):
    """Bus entry in GET /public/buses list and WebSocket snapshots.

    lat/lon are None while the bus has never reported a position.
    """

    bus_id: UUID
    code: str
    route: RouteRef | None
    location: LocationOut | None
    speed_kmh: float | None
    is_online: bool
    last_seen_at: datetime | None
    offline_since_s: int | None
    current_stop: StopWithEta | None
    next_stop: StopWithEta | None
    terminus: StopWithEta | None
    progress_pct: float | None


class BusDetailRead(BusPublicRead):
    """GET /public/buses/{id} — public detail with recent position history."""

    recent_positions: list[PositionCreate] = Field(default_factory=list)
