"""Shared building-blocks reused across multiple schema files."""

from uuid import UUID

from pydantic import BaseModel, Field


class LocationOut(BaseModel):
    """Geographic point returned in API responses (WGS-84)."""

    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class StopRef(BaseModel):
    """Minimal stop reference embedded in bus/route responses."""

    id: UUID
    name: str


class StopWithEta(StopRef):
    """Stop reference with ETA — used in bus status responses."""

    eta_seconds: int | None = None


class RouteRef(BaseModel):
    """Minimal route reference embedded in bus responses."""

    id: UUID
    name: str
