"""Pydantic schemas for WebSocket message payloads.

Public channel:  ws://host/ws/buses      — SnapshotMessage, BusOfflineEvent
Admin channel:   ws://localhost/ws/admin  — AdminSnapshotMessage
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.common import StopWithEta


class BusSnapshot(BaseModel):
    """Single bus entry inside a snapshot push (public channel)."""

    bus_id: UUID
    code: str
    route_id: UUID | None
    route_name: str | None
    lat: float | None
    lon: float | None
    speed_kmh: float | None
    heading: float | None
    is_online: bool
    offline_since_s: int | None
    current_stop: StopWithEta | None
    next_stop: StopWithEta | None
    terminus_eta_s: int | None
    progress_pct: float | None


class SnapshotMessage(BaseModel):
    """Full snapshot pushed every 5 s on the public channel."""

    type: Literal["snapshot"] = "snapshot"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    buses: list[BusSnapshot] = Field(default_factory=list)


class BusOfflineEvent(BaseModel):
    """Emitted once when a bus transitions to offline."""

    type: Literal["bus_offline"] = "bus_offline"
    bus_id: UUID
    last_seen_at: datetime


# ---------------------------------------------------------------------------
# Admin channel (same base + extra fields)
# ---------------------------------------------------------------------------

class BusSnapshotAdmin(BusSnapshot):
    """Enriched bus snapshot for the admin WebSocket channel."""

    api_token_masked: str  # e.g. "abc***xyz"
    is_active: bool
    positions_last_hour: int


class AdminSnapshotMessage(BaseModel):
    """Full snapshot on ws://localhost/ws/admin."""

    type: Literal["snapshot"] = "snapshot"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    buses: list[BusSnapshotAdmin] = Field(default_factory=list)
