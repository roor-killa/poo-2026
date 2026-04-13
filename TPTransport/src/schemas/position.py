"""Schemas for POST /api/v1/positions (bus-client private endpoint)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PositionCreate(BaseModel):
    """Request body sent by the embedded client every 5 s."""

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    speed_kmh: float | None = Field(None, ge=0.0)
    heading: float | None = Field(None, ge=0.0, lt=360.0)
    recorded_at: datetime


class PositionResponse(BaseModel):
    """201 response after a position is accepted."""

    status: str = "ok"
    bus_id: UUID
    server_time: datetime
