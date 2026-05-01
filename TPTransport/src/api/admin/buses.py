"""Admin bus CRUD — /api/v1/admin/buses (spec §3.3, localhost only)."""

from __future__ import annotations

import secrets
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.api.deps import LocalhostGuard, SessionDep
from src.repositories import BusRepository, PositionRepository
from src.schemas.bus import BusAdminRead, BusCreate, BusUpdate
from src.schemas.common import RouteRef

router = APIRouter(
    prefix="/api/v1/admin/buses",
    tags=["admin"],
    dependencies=[LocalhostGuard],
)

_TOKEN_BYTES = 48  # 64-char hex token


def _mask_token(token: str) -> str:
    """Return first 3 + *** + last 3 characters."""
    if len(token) <= 6:
        return "***"
    return token[:3] + "***" + token[-3:]


async def _to_admin_read(
    bus,
    session,
    *,
    expose_token: bool = False,
) -> BusAdminRead:
    pos_repo = PositionRepository(session)
    count = await pos_repo.count_last_hour(bus.id)
    status_row = bus.status
    return BusAdminRead(
        id=bus.id,
        code=bus.code,
        label=bus.label,
        route=RouteRef(id=bus.route.id, name=bus.route.name) if bus.route else None,
        api_token=bus.api_token if expose_token else _mask_token(bus.api_token),
        is_active=bus.is_active,
        created_at=bus.created_at,
        last_seen_at=status_row.last_seen_at if status_row else None,
        positions_last_hour=count,
    )


@router.get("", response_model=list[BusAdminRead], summary="List all buses (active + inactive)")
async def list_buses(session: SessionDep) -> list[BusAdminRead]:
    repo = BusRepository(session)
    buses = await repo.list_all()
    return [await _to_admin_read(b, session) for b in buses]


@router.post(
    "",
    response_model=BusAdminRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a bus — returns the API token once (plain-text)",
)
async def create_bus(body: BusCreate, session: SessionDep) -> BusAdminRead:
    from app.db.models.bus import Bus

    token = secrets.token_hex(_TOKEN_BYTES)
    bus = Bus(
        code=body.code,
        label=body.label,
        route_id=body.route_id,
        api_token=token,
    )
    repo = BusRepository(session)
    try:
        bus = await repo.add(bus)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus code already exists",
        )

    # Reload with relationships eagerly loaded (async sessions can't lazy-load)
    loaded = await repo.get_with_related(bus.id)
    if loaded is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Created bus not found")
    return await _to_admin_read(loaded, session, expose_token=True)


@router.put("/{bus_id}", response_model=BusAdminRead, summary="Update a bus")
async def update_bus(bus_id: UUID, body: BusUpdate, session: SessionDep) -> BusAdminRead:
    repo = BusRepository(session)
    bus = await repo.get_with_related(bus_id)
    if bus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")

    if body.code is not None:
        bus.code = body.code
    if body.label is not None:
        bus.label = body.label
    if body.route_id is not None:
        bus.route_id = body.route_id
    if body.is_active is not None:
        bus.is_active = body.is_active

    try:
        await session.flush()
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus code already exists",
        )

    loaded = await repo.get_with_related(bus.id)
    if loaded is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    return await _to_admin_read(loaded, session)


@router.delete(
    "/{bus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a bus and all its data",
)
async def delete_bus(bus_id: UUID, session: SessionDep) -> None:
    repo = BusRepository(session)
    bus = await repo.get(bus_id)
    if bus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    await repo.delete(bus)
    await session.commit()
