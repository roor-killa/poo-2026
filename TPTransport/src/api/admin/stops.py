"""Admin stop CRUD — /api/v1/admin/stops (spec §3.3, localhost only)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.db.models.stop import Stop
from src.api.deps import LocalhostGuard, SessionDep
from src.repositories import StopRepository
from src.schemas.stop import StopCreate, StopRead, StopUpdate
from src.services.geo import latlon_to_wkt, wkb_to_latlon

router = APIRouter(
    prefix="/api/v1/admin/stops",
    tags=["admin"],
    dependencies=[LocalhostGuard],
)


def _to_read(stop: Stop) -> StopRead:
    lat, lon = wkb_to_latlon(stop.location)
    return StopRead(id=stop.id, name=stop.name, lat=lat, lon=lon, created_at=stop.created_at)


@router.post(
    "",
    response_model=StopRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a stop",
)
async def create_stop(body: StopCreate, session: SessionDep) -> StopRead:
    stop = Stop(name=body.name, location=latlon_to_wkt(body.lat, body.lon))
    repo = StopRepository(session)
    stop = await repo.add(stop)
    await session.commit()
    await session.refresh(stop)
    return _to_read(stop)


@router.put("/{stop_id}", response_model=StopRead, summary="Update a stop")
async def update_stop(stop_id: UUID, body: StopUpdate, session: SessionDep) -> StopRead:
    repo = StopRepository(session)
    stop = await repo.get(stop_id)
    if stop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")

    if body.name is not None:
        stop.name = body.name
    if body.lat is not None or body.lon is not None:
        # Need both coords; fall back to current values for the unchanged one
        cur_lat, cur_lon = wkb_to_latlon(stop.location)
        new_lat = body.lat if body.lat is not None else cur_lat
        new_lon = body.lon if body.lon is not None else cur_lon
        stop.location = latlon_to_wkt(new_lat, new_lon)

    await session.flush()
    await session.commit()
    await session.refresh(stop)
    return _to_read(stop)


@router.delete(
    "/{stop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a stop (hard delete — cascades route_stops)",
)
async def delete_stop(stop_id: UUID, session: SessionDep) -> None:
    repo = StopRepository(session)
    stop = await repo.get(stop_id)
    if stop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")
    await repo.delete(stop)
    await session.commit()
