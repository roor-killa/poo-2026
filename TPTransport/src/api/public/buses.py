"""GET /api/v1/public/buses — public bus endpoints (spec §3.2)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from src.api.deps import PUBLIC_RATE, SessionDep, limiter
from src.schemas.bus import BusDetailRead, BusPublicRead
from src.services.bus_service import BusService

router = APIRouter(prefix="/api/v1/public/buses", tags=["public"])


@router.get(
    "",
    response_model=list[BusPublicRead],
    summary="List all active buses with live position and ETA",
)
@limiter.limit(PUBLIC_RATE)
async def list_buses(request: Request, session: SessionDep) -> list[BusPublicRead]:
    return await BusService(session).list_public()


@router.get(
    "/{bus_id}",
    response_model=BusDetailRead,
    summary="Get a single bus with position history",
)
@limiter.limit(PUBLIC_RATE)
async def get_bus(request: Request, bus_id: UUID, session: SessionDep) -> BusDetailRead:
    result = await BusService(session).get_public(bus_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    return result
