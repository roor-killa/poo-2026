"""Read-side bus service — assembles Pydantic response schemas from ORM rows.

Used by the public REST endpoints and the WebSocket broadcaster.
The service converts geoalchemy2 Geography WKB → lat/lon here (per CLAUDE.md:
schemas never import geoalchemy2).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import BusRepository, BusStatusRepository, PositionRepository
from src.schemas.bus import BusDetailRead, BusPublicRead
from src.schemas.common import LocationOut, RouteRef, StopWithEta
from src.schemas.position import PositionCreate
from src.services.geo import wkb_to_latlon


class BusService:

    def __init__(self, session: AsyncSession) -> None:
        self._bus_repo = BusRepository(session)
        self._status_repo = BusStatusRepository(session)
        self._pos_repo = PositionRepository(session)

    async def list_public(self) -> list[BusPublicRead]:
        """All active buses with live status — for GET /public/buses."""
        buses = await self._bus_repo.list_active()
        return [self._to_public_read(b) for b in buses]

    async def get_public(self, bus_id: UUID) -> BusDetailRead | None:
        """Single bus detail — for GET /public/buses/{bus_id}."""
        from app.db.models.bus import Bus  # local import — models not imported at module level
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        result = await self._bus_repo.session.execute(  # type: ignore[attr-defined]
            select(Bus)
            .where(Bus.id == bus_id, Bus.is_active.is_(True))
            .options(
                selectinload(Bus.status),
                selectinload(Bus.route),
            )
        )
        bus = result.scalar_one_or_none()
        if bus is None:
            return None

        raw_positions = await self._pos_repo.get_recent_for_bus(bus_id, limit=20)
        recent = [
            PositionCreate(
                latitude=wkb_to_latlon(p.location)[0],
                longitude=wkb_to_latlon(p.location)[1],
                speed_kmh=p.speed_kmh,
                heading=p.heading,
                recorded_at=p.recorded_at,
            )
            for p in raw_positions
        ]

        base = self._to_public_read(bus)
        return BusDetailRead(**base.model_dump(), recent_positions=recent)

    async def list_all_statuses(self) -> list[BusPublicRead]:
        """All buses including offline — used by the WebSocket broadcaster."""
        buses = await self._bus_repo.list_all()
        return [self._to_public_read(b) for b in buses]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _to_public_read(self, bus) -> BusPublicRead:  # type: ignore[override]
        status = bus.status
        now = datetime.now(tz=timezone.utc)

        location: LocationOut | None = None
        last_seen_at: datetime | None = None
        offline_since_s: int | None = None
        is_online = False
        speed_kmh: float | None = None
        current_stop = None
        next_stop = None
        terminus = None
        progress_pct: float | None = None

        if status is not None:
            last_seen_at = status.last_seen_at
            is_online = status.is_online
            speed_kmh = status.last_speed_kmh
            progress_pct = status.progress_pct

            if status.last_location is not None:
                lat, lon = wkb_to_latlon(status.last_location)
                location = LocationOut(lat=lat, lon=lon)

            if not is_online and last_seen_at is not None:
                seen = last_seen_at
                if seen.tzinfo is None:
                    seen = seen.replace(tzinfo=timezone.utc)
                offline_since_s = int((now - seen).total_seconds())

            if status.current_stop is not None:
                current_stop = StopWithEta(
                    id=status.current_stop.id,
                    name=status.current_stop.name,
                    eta_seconds=0,
                )

            if status.next_stop is not None:
                next_stop = StopWithEta(
                    id=status.next_stop.id,
                    name=status.next_stop.name,
                    eta_seconds=status.eta_next_stop_s,
                )

            # Terminus: last stop in the route (not directly on bus_status;
            # eta_terminus_s is the total ETA — we expose it on a sentinel object)
            if status.eta_terminus_s is not None:
                terminus = StopWithEta(
                    id=bus.route_id or bus.id,   # route_id as proxy; router can enrich
                    name="Terminus",
                    eta_seconds=status.eta_terminus_s,
                )

        route_ref: RouteRef | None = None
        if bus.route is not None:
            route_ref = RouteRef(id=bus.route.id, name=bus.route.name)

        return BusPublicRead(
            bus_id=bus.id,
            code=bus.code,
            route=route_ref,
            location=location,
            speed_kmh=speed_kmh,
            is_online=is_online,
            last_seen_at=last_seen_at,
            offline_since_s=offline_since_s,
            current_stop=current_stop,
            next_stop=next_stop,
            terminus=terminus,
            progress_pct=progress_pct,
        )
