"""GET /api/v1/public/stops/{stop_id}/arrivals (spec §3.2)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.bus import Bus
from app.db.models.bus_status import BusStatus
from src.api.deps import PUBLIC_RATE, SessionDep, limiter
from src.repositories import StopRepository
from src.schemas.stop import ArrivalRead, RouteRefInArrival, StopRead
from src.services.geo import wkb_to_latlon

router = APIRouter(prefix="/api/v1/public/stops", tags=["public"])


@router.get("", response_model=list[StopRead], summary="List all stops")
@limiter.limit(PUBLIC_RATE)
async def list_stops(request: Request, session: SessionDep) -> list[StopRead]:
    repo = StopRepository(session)
    stops = await repo.list()
    return [
        StopRead(
            id=s.id,
            name=s.name,
            lat=wkb_to_latlon(s.location)[0],
            lon=wkb_to_latlon(s.location)[1],
            created_at=s.created_at,
        )
        for s in stops
    ]


@router.get(
    "/{stop_id}/arrivals",
    response_model=list[ArrivalRead],
    summary="Upcoming buses for a stop, ordered by ETA",
)
@limiter.limit(PUBLIC_RATE)
async def stop_arrivals(
    request: Request, stop_id: UUID, session: SessionDep
) -> list[ArrivalRead]:
    # Verify stop exists
    stop_repo = StopRepository(session)
    stop = await stop_repo.get(stop_id)
    if stop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")

    # Find all buses whose next_stop_id == stop_id and have a route
    result = await session.execute(
        select(BusStatus)
        .where(BusStatus.next_stop_id == stop_id)
        .options(
            selectinload(BusStatus.bus).selectinload(Bus.route),
        )
    )
    statuses = result.scalars().all()

    arrivals: list[ArrivalRead] = []
    for s in statuses:
        bus = s.bus
        if bus is None or not bus.is_active:
            continue
        route_ref = (
            RouteRefInArrival(id=bus.route.id, name=bus.route.name)
            if bus.route is not None
            else RouteRefInArrival(id=bus.id, name="—")
        )
        arrivals.append(
            ArrivalRead(
                bus_id=bus.id,
                bus_code=bus.code,
                route=route_ref,
                eta_seconds=s.eta_next_stop_s,
                is_online=s.is_online,
            )
        )

    # Sort by ETA: online buses with known ETA first, offline last
    arrivals.sort(
        key=lambda a: (
            not a.is_online,
            a.eta_seconds if a.eta_seconds is not None else 10**9,
        )
    )
    return arrivals
