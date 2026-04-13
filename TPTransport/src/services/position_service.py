"""Position ingest service — the core server-side pipeline triggered by
POST /api/v1/positions.

Pipeline per incoming position fix (spec §§5.1-5.5):
  1. Authenticate bus by Bearer token.
  2. Persist the raw Position row.
  3. Detect whether the bus is within 100 m of a route stop (§5.1).
  4. Detect stop-to-stop segment completion and trigger EMA update (§5.5).
  5. Compute ETA to next stop and terminus (§5.2).
  6. Compute progress_pct along the route (§5.3).
  7. Upsert bus_status.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import UUID

from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from sqlalchemy import cast, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.bus import Bus
from app.db.models.bus_status import BusStatus
from app.db.models.position import Position
from app.db.models.route_stop import RouteStop
from app.db.models.stop import Stop
from src.repositories import (
    BusRepository,
    BusStatusRepository,
    PositionRepository,
    SegmentSpeedRepository,
)
from src.schemas.position import PositionCreate, PositionResponse
from src.services.eta import (
    SegmentInfo,
    compute_eta_next_stop,
    compute_eta_terminus,
    compute_progress_pct,
)
from src.services.geo import haversine_m, latlon_to_wkt, wkb_to_latlon

logger = logging.getLogger(__name__)

# Geography cast helper — used for ST_DWithin calls
from geoalchemy2 import Geography as _Geo


def _geo_point(lon: float, lat: float):
    """Return a cast-able GEOGRAPHY POINT expression."""
    return cast(ST_MakePoint(lon, lat), _Geo)


class AuthError(Exception):
    """Raised when the Bearer token does not match any active bus."""


class PositionService:
    """Stateless service; instantiate once per request with a live session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._bus_repo = BusRepository(session)
        self._pos_repo = PositionRepository(session)
        self._status_repo = BusStatusRepository(session)
        self._speed_repo = SegmentSpeedRepository(session)

    # ------------------------------------------------------------------
    # Public entry-point
    # ------------------------------------------------------------------

    async def ingest(
        self, token: str, payload: PositionCreate
    ) -> PositionResponse:
        """Full ingest pipeline. Raises AuthError on bad token."""
        bus = await self._authenticate(token)

        position = await self._persist_position(bus, payload)
        await self._update_bus_status(bus, payload, position)

        return PositionResponse(
            bus_id=bus.id,
            server_time=datetime.now(tz=timezone.utc),
        )

    # ------------------------------------------------------------------
    # Step 1 — authentication
    # ------------------------------------------------------------------

    async def _authenticate(self, token: str) -> Bus:
        bus = await self._bus_repo.get_by_token(token)
        if bus is None:
            raise AuthError("Invalid or inactive token")
        return bus

    # ------------------------------------------------------------------
    # Step 2 — persist raw GPS fix
    # ------------------------------------------------------------------

    async def _persist_position(
        self, bus: Bus, payload: PositionCreate
    ) -> Position:
        wkt = latlon_to_wkt(payload.latitude, payload.longitude)
        position = Position(
            bus_id=bus.id,
            location=wkt,
            speed_kmh=payload.speed_kmh,
            heading=payload.heading,
            recorded_at=payload.recorded_at,
        )
        return await self._pos_repo.add(position)

    # ------------------------------------------------------------------
    # Steps 3-7 — stop detection, ETA, progress, status upsert
    # ------------------------------------------------------------------

    async def _update_bus_status(
        self, bus: Bus, payload: PositionCreate, position: Position
    ) -> None:
        if bus.route_id is None:
            # Bus has no assigned route — just record last-seen
            await self._upsert_no_route(bus, payload)
            return

        route_stops = await self._load_route_stops(bus.route_id)
        if not route_stops:
            await self._upsert_no_route(bus, payload)
            return

        prev_status = await self._status_repo.get(bus.id)

        # Step 3 — stop detection (ST_DWithin 100 m)
        current_stop, current_order = await self._detect_current_stop(
            payload.latitude, payload.longitude, route_stops
        )

        # Step 5 — segment EMA (must happen before status is overwritten)
        if prev_status is not None:
            await self._maybe_update_segment_ema(
                bus=bus,
                route_stops=route_stops,
                prev_status=prev_status,
                current_stop=current_stop,
                current_order=current_order,
                now=payload.recorded_at,
            )

        # Determine next stop in sequence
        next_stop, next_order = self._next_stop(current_order, route_stops)

        # Step 4 — ETA
        hour_bucket = payload.recorded_at.hour
        day_type = (
            "weekend"
            if payload.recorded_at.weekday() >= 5
            else "weekday"
        )

        eta_next_s, eta_terminus_s = await self._compute_etas(
            lat=payload.latitude,
            lon=payload.longitude,
            speed_kmh=payload.speed_kmh,
            route_id=bus.route_id,
            route_stops=route_stops,
            next_stop=next_stop,
            next_order=next_order,
            hour_bucket=hour_bucket,
            day_type=day_type,
        )

        # Step 6 — progress_pct
        d_to_next_m = (
            haversine_m(
                payload.latitude, payload.longitude,
                *wkb_to_latlon(next_stop.location),
            )
            if next_stop is not None
            else 0.0
        )
        distances = [rs.distance_from_prev_m for rs in route_stops]
        progress = compute_progress_pct(distances, current_order, d_to_next_m)

        # Step 7 — upsert bus_status
        wkt = latlon_to_wkt(payload.latitude, payload.longitude)
        status = BusStatus(
            bus_id=bus.id,
            last_location=wkt,
            last_speed_kmh=payload.speed_kmh,
            last_seen_at=datetime.now(tz=timezone.utc),
            is_online=True,
            current_stop_id=current_stop.id if current_stop else None,
            next_stop_id=next_stop.id if next_stop else None,
            eta_next_stop_s=eta_next_s,
            eta_terminus_s=eta_terminus_s,
            progress_pct=round(progress, 2),
        )
        await self._status_repo.upsert(status)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _load_route_stops(self, route_id: UUID) -> list[RouteStop]:
        """Ordered list of RouteStop rows with their Stop eagerly loaded."""
        result = await self._session.execute(
            select(RouteStop)
            .where(RouteStop.route_id == route_id)
            .options(selectinload(RouteStop.stop))
            .order_by(RouteStop.stop_order)
        )
        return list(result.scalars().all())

    async def _detect_current_stop(
        self,
        lat: float,
        lon: float,
        route_stops: list[RouteStop],
    ) -> tuple[Stop | None, int | None]:
        """Return the Stop and its 1-based stop_order if bus ≤ 100 m away."""
        point = _geo_point(lon, lat)
        result = await self._session.execute(
            select(Stop)
            .where(ST_DWithin(Stop.location, point, 100.0))
            .where(Stop.id.in_([rs.stop_id for rs in route_stops]))
        )
        nearby: list[Stop] = list(result.scalars().all())
        if not nearby:
            return None, None

        # Among nearby stops choose the one with the smallest stop_order
        order_map = {rs.stop_id: (rs.stop_order, rs.stop) for rs in route_stops}
        best_order = min(order_map[s.id][0] for s in nearby if s.id in order_map)
        best_stop = order_map[
            next(s.id for s in nearby if order_map.get(s.id, (None,))[0] == best_order)
        ][1]
        return best_stop, best_order

    def _next_stop(
        self,
        current_order: int | None,
        route_stops: list[RouteStop],
    ) -> tuple[Stop | None, int | None]:
        """Return (next Stop, next stop_order) after current_order.

        If current_order is None the next stop is the first one (order 1).
        Returns (None, None) when at terminus.
        """
        if not route_stops:
            return None, None

        if current_order is None:
            rs = route_stops[0]
            return rs.stop, rs.stop_order

        for rs in route_stops:
            if rs.stop_order > current_order:
                return rs.stop, rs.stop_order
        # At terminus
        return None, None

    async def _compute_etas(
        self,
        lat: float,
        lon: float,
        speed_kmh: float | None,
        route_id: UUID,
        route_stops: list[RouteStop],
        next_stop: Stop | None,
        next_order: int | None,
        hour_bucket: int,
        day_type: str,
    ) -> tuple[int | None, int]:
        """Return (eta_next_stop_s, eta_terminus_s).

        eta_next_stop_s is None when at terminus; eta_terminus_s is 0 there.
        """
        if next_stop is None:
            # At terminus
            return None, 0

        # Distance bus → next stop
        next_lat, next_lon = wkb_to_latlon(next_stop.location)
        d_to_next = haversine_m(lat, lon, next_lat, next_lon)

        # Historical speed for current segment
        # current segment: from the stop just before next_stop to next_stop
        from_order = (next_order - 1) if next_order and next_order > 1 else 1
        v_avg = await self._speed_repo.get_speed_kmh(
            route_id, from_order, next_order, hour_bucket, day_type
        )

        eta_next = compute_eta_next_stop(d_to_next, v_avg, speed_kmh)

        # Remaining segments from next_stop to terminus
        remaining: list[SegmentInfo] = []
        for rs in route_stops:
            if rs.stop_order <= (next_order or 0):
                continue
            seg_v_avg = await self._speed_repo.get_speed_kmh(
                route_id,
                rs.stop_order - 1,
                rs.stop_order,
                hour_bucket,
                day_type,
            )
            remaining.append(
                SegmentInfo(
                    distance_m=rs.distance_from_prev_m or 0.0,
                    avg_speed_kmh=seg_v_avg,
                )
            )

        eta_term = compute_eta_terminus(eta_next, remaining)
        return eta_next, eta_term

    async def _maybe_update_segment_ema(
        self,
        bus: Bus,
        route_stops: list[RouteStop],
        prev_status: BusStatus,
        current_stop: Stop | None,
        current_order: int | None,
        now: datetime,
    ) -> None:
        """Trigger §5.5 EMA update when the bus has crossed a segment boundary.

        A segment is considered completed when prev_status had a current_stop
        (stop N) and the new position reveals a different current_stop (stop N+1)
        that is the immediate successor.
        """
        prev_stop_id = prev_status.current_stop_id
        prev_last_seen = prev_status.last_seen_at

        if current_stop is None or prev_stop_id is None or current_order is None:
            return
        if current_stop.id == prev_stop_id:
            return  # still at the same stop

        # Find the previous stop's order
        prev_order: int | None = None
        for rs in route_stops:
            if rs.stop_id == prev_stop_id:
                prev_order = rs.stop_order
                break

        if prev_order is None or current_order != prev_order + 1:
            return  # non-consecutive stops — skip (bus was offline or skipped)

        # Find the RouteStop entry for the destination (current) stop to get distance
        seg_distance_m: float | None = None
        for rs in route_stops:
            if rs.stop_order == current_order:
                seg_distance_m = rs.distance_from_prev_m
                break

        if not seg_distance_m or seg_distance_m <= 0:
            return

        if prev_last_seen is None:
            return

        # Ensure both datetimes are timezone-aware before subtracting
        prev_ts = prev_last_seen
        if prev_ts.tzinfo is None:
            prev_ts = prev_ts.replace(tzinfo=timezone.utc)
        curr_ts = now
        if curr_ts.tzinfo is None:
            curr_ts = curr_ts.replace(tzinfo=timezone.utc)

        elapsed_s = (curr_ts - prev_ts).total_seconds()
        if elapsed_s <= 0:
            return

        observed_speed = (seg_distance_m / elapsed_s) * 3.6  # m/s → km/h

        hour_bucket = curr_ts.hour
        day_type = "weekend" if curr_ts.weekday() >= 5 else "weekday"

        await self._speed_repo.upsert_ema(
            route_id=bus.route_id,
            from_order=prev_order,
            to_order=current_order,
            hour_bucket=hour_bucket,
            day_type=day_type,
            observed_speed_kmh=observed_speed,
        )

    async def _upsert_no_route(self, bus: Bus, payload: PositionCreate) -> None:
        """Minimal status update for buses with no assigned route."""
        wkt = latlon_to_wkt(payload.latitude, payload.longitude)
        status = BusStatus(
            bus_id=bus.id,
            last_location=wkt,
            last_speed_kmh=payload.speed_kmh,
            last_seen_at=datetime.now(tz=timezone.utc),
            is_online=True,
        )
        await self._status_repo.upsert(status)
