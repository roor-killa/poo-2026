"""WebSocket broadcaster — spec §4.

Maintains two connection sets (public / admin) and runs a background asyncio
loop that pushes a full snapshot every 5 s.  Also emits a one-shot
`bus_offline` event whenever a bus transitions from online → offline.

Lifecycle
---------
Instantiate once at startup, call ``start()`` which returns an asyncio.Task.
Inject the singleton via ``get_broadcaster`` FastAPI dependency.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import AsyncSessionLocal
from src.repositories import BusRepository, PositionRepository
from src.schemas.websocket import (
    AdminSnapshotMessage,
    BusOfflineEvent,
    BusSnapshot,
    BusSnapshotAdmin,
    SnapshotMessage,
)
from src.services.bus_service import BusService
from src.services.geo import wkb_to_latlon

logger = logging.getLogger(__name__)

BROADCAST_INTERVAL_S: int = 5


def _mask_token(token: str) -> str:
    if len(token) <= 6:
        return "***"
    return token[:3] + "***" + token[-3:]


def _public_snapshot(bus_reads) -> BusSnapshot | None:
    """Convert a BusPublicRead → BusSnapshot (public wire format)."""
    # BusPublicRead is already a Pydantic model; just remap field names
    b = bus_reads
    return BusSnapshot(
        bus_id=b.bus_id,
        code=b.code,
        route_id=b.route.id if b.route else None,
        route_name=b.route.name if b.route else None,
        lat=b.location.lat if b.location else None,
        lon=b.location.lon if b.location else None,
        speed_kmh=b.speed_kmh,
        heading=None,           # BusPublicRead doesn't carry heading; DB has it
        is_online=b.is_online,
        offline_since_s=b.offline_since_s,
        current_stop=b.current_stop,
        next_stop=b.next_stop,
        terminus_eta_s=b.terminus.eta_seconds if b.terminus else None,
        progress_pct=b.progress_pct,
    )


class Broadcaster:
    """Central hub for WebSocket clients.

    Two channels:
    - ``_public``  → /ws/buses       — receives SnapshotMessage
    - ``_admin``   → /ws/admin       — receives AdminSnapshotMessage
    """

    def __init__(self) -> None:
        self._public: set[WebSocket] = set()
        self._admin: set[WebSocket] = set()
        # Track previous online-state to detect transitions
        self._prev_online: dict[UUID, bool] = {}

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    async def connect_public(self, ws: WebSocket) -> None:
        await ws.accept()
        self._public.add(ws)
        logger.info("Public WS connected  (total=%d)", len(self._public))

    async def disconnect_public(self, ws: WebSocket) -> None:
        self._public.discard(ws)
        logger.info("Public WS disconnected (total=%d)", len(self._public))

    async def connect_admin(self, ws: WebSocket) -> None:
        await ws.accept()
        self._admin.add(ws)
        logger.info("Admin WS connected  (total=%d)", len(self._admin))

    async def disconnect_admin(self, ws: WebSocket) -> None:
        self._admin.discard(ws)
        logger.info("Admin WS disconnected (total=%d)", len(self._admin))

    # ------------------------------------------------------------------
    # Background broadcast loop
    # ------------------------------------------------------------------

    def start(self) -> asyncio.Task:
        """Create and return the broadcast asyncio task."""
        return asyncio.create_task(self._loop())

    async def _loop(self) -> None:
        logger.info("Broadcaster started (interval=%ds)", BROADCAST_INTERVAL_S)
        while True:
            try:
                await self._tick()
            except asyncio.CancelledError:
                logger.info("Broadcaster cancelled")
                raise
            except Exception:
                logger.exception("Broadcaster tick failed — will retry")
            await asyncio.sleep(BROADCAST_INTERVAL_S)

    async def _tick(self) -> None:
        has_public = bool(self._public)
        has_admin  = bool(self._admin)

        async with AsyncSessionLocal() as session:
            bus_reads = await BusService(session).list_all_statuses()
            admin_extras = (
                await self._build_admin_extras(session, bus_reads)
                if has_admin else []
            )

        # Always track online transitions (state machine, no clients needed)
        offline_events: list[BusOfflineEvent] = []
        for b in bus_reads:
            was_online = self._prev_online.get(b.bus_id, True)
            if was_online and not b.is_online:
                offline_events.append(
                    BusOfflineEvent(
                        bus_id=b.bus_id,
                        last_seen_at=b.last_seen_at or datetime.now(tz=timezone.utc),
                    )
                )
            self._prev_online[b.bus_id] = b.is_online

        # Build and send public snapshot only when someone is listening
        if has_public:
            snapshots   = [_public_snapshot(b) for b in bus_reads]
            public_json = SnapshotMessage(
                timestamp=datetime.now(tz=timezone.utc),
                buses=snapshots,
            ).model_dump_json()
            await self._broadcast(self._public, public_json)

        # Build and send admin snapshot only when someone is listening
        if has_admin:
            admin_snapshots = []
            for b, extra in zip(bus_reads, admin_extras):
                snap = _public_snapshot(b)
                admin_snapshots.append(
                    BusSnapshotAdmin(
                        **snap.model_dump(),
                        api_token_masked=extra["token_masked"],
                        is_active=extra["is_active"],
                        positions_last_hour=extra["positions_last_hour"],
                    )
                )
            admin_json = AdminSnapshotMessage(
                timestamp=datetime.now(tz=timezone.utc),
                buses=admin_snapshots,
            ).model_dump_json()
            await self._broadcast(self._admin, admin_json)

        # Offline events go to whoever is connected
        for evt in offline_events:
            evt_json = evt.model_dump_json()
            if has_public:
                await self._broadcast(self._public, evt_json)
            if has_admin:
                await self._broadcast(self._admin, evt_json)

    async def _broadcast(self, clients: set[WebSocket], message: str) -> None:
        dead: list[WebSocket] = []
        for ws in list(clients):
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            clients.discard(ws)

    async def _build_admin_extras(self, session: AsyncSession, bus_reads) -> list[dict]:
        """Fetch per-bus admin fields with two queries total (not N+1)."""
        bus_repo = BusRepository(session)
        pos_repo = PositionRepository(session)
        buses    = await bus_repo.list_all()
        bus_map  = {b.id: b for b in buses}
        counts   = await pos_repo.count_last_hour_all()  # single GROUP BY query

        return [
            {
                "token_masked": _mask_token(bus_map[b.bus_id].api_token)
                    if b.bus_id in bus_map else "***",
                "is_active": bus_map[b.bus_id].is_active
                    if b.bus_id in bus_map else False,
                "positions_last_hour": counts.get(b.bus_id, 0),
            }
            for b in bus_reads
        ]


# ---------------------------------------------------------------------------
# Singleton + FastAPI dependency
# ---------------------------------------------------------------------------

_broadcaster: Broadcaster | None = None


def get_broadcaster() -> Broadcaster:
    global _broadcaster
    if _broadcaster is None:
        _broadcaster = Broadcaster()
    return _broadcaster
