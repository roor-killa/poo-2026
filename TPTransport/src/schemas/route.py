"""Schemas for the routes resource (admin CRUD + public read)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.stop import StopRead


# ---------------------------------------------------------------------------
# Sub-schemas
# ---------------------------------------------------------------------------

class RouteStopIn(BaseModel):
    """One stop entry when creating / updating a route's stop sequence."""

    stop_id: UUID
    stop_order: int = Field(..., ge=1)
    distance_from_prev_m: float | None = Field(None, ge=0.0)


class RouteStopRead(BaseModel):
    """Stop-in-route entry returned in route detail responses."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    stop_order: int
    distance_from_prev_m: float | None
    stop: StopRead


# ---------------------------------------------------------------------------
# Request bodies
# ---------------------------------------------------------------------------

class RouteCreate(BaseModel):
    """Admin POST /routes body — includes the initial stop sequence."""

    name: str = Field(..., max_length=120)
    description: str | None = None
    is_active: bool = True
    stops: list[RouteStopIn] = Field(default_factory=list)


class RouteUpdate(BaseModel):
    """Admin PUT /routes/{id} body — all fields optional."""

    name: str | None = Field(None, max_length=120)
    description: str | None = None
    is_active: bool | None = None
    stops: list[RouteStopIn] | None = None  # None = don't touch the sequence


# ---------------------------------------------------------------------------
# Response bodies
# ---------------------------------------------------------------------------

class RouteRead(BaseModel):
    """Route summary returned in list responses (no stop detail)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RouteDetailRead(RouteRead):
    """Route detail returned by GET /routes/{id} — includes ordered stops."""

    route_stops: list[RouteStopRead] = Field(default_factory=list)
