"""Schemas for the stops resource (admin CRUD + public arrivals endpoint)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import StopWithEta


class StopCreate(BaseModel):
    """Admin POST /stops body."""

    name: str = Field(..., max_length=120)
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class StopUpdate(BaseModel):
    """Admin PUT /stops/{id} body — all fields optional."""

    name: str | None = Field(None, max_length=120)
    lat: float | None = Field(None, ge=-90.0, le=90.0)
    lon: float | None = Field(None, ge=-180.0, le=180.0)


class StopRead(BaseModel):
    """Stop returned in admin and public-detail responses.

    Note: the service layer must extract lat/lon from the geoalchemy2
    Geography WKB before constructing this schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    lat: float
    lon: float
    created_at: datetime


class ArrivalRead(BaseModel):
    """One upcoming bus entry for GET /public/stops/{id}/arrivals."""

    bus_id: UUID
    bus_code: str
    route: "RouteRefInArrival"
    eta_seconds: int | None
    is_online: bool


class RouteRefInArrival(BaseModel):
    id: UUID
    name: str


ArrivalRead.model_rebuild()
