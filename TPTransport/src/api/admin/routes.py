"""Admin route CRUD — /api/v1/admin/routes (spec §3.3, localhost only)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import selectinload

from app.db.models.route import Route
from app.db.models.route_stop import RouteStop
from src.api.deps import LocalhostGuard, SessionDep
from src.repositories import RouteRepository
from src.schemas.route import RouteCreate, RouteDetailRead, RouteStopRead, RouteUpdate
from src.schemas.stop import StopRead
from src.services.geo import wkb_to_latlon

router = APIRouter(
    prefix="/api/v1/admin/routes",
    tags=["admin"],
    dependencies=[LocalhostGuard],
)


def _build_detail(route: Route) -> RouteDetailRead:
    return RouteDetailRead(
        id=route.id,
        name=route.name,
        description=route.description,
        is_active=route.is_active,
        created_at=route.created_at,
        updated_at=route.updated_at,
        route_stops=[
            RouteStopRead(
                id=rs.id,
                stop_order=rs.stop_order,
                distance_from_prev_m=rs.distance_from_prev_m,
                stop=StopRead(
                    id=rs.stop.id,
                    name=rs.stop.name,
                    lat=wkb_to_latlon(rs.stop.location)[0],
                    lon=wkb_to_latlon(rs.stop.location)[1],
                    created_at=rs.stop.created_at,
                ),
            )
            for rs in route.route_stops
        ],
    )


@router.get("", response_model=list[RouteDetailRead], summary="List all routes (active + inactive)")
async def list_routes(session: SessionDep) -> list[RouteDetailRead]:
    from sqlalchemy import select

    result = await session.execute(
        select(Route).options(
            selectinload(Route.route_stops).selectinload(RouteStop.stop)
        )
    )
    routes = result.scalars().all()
    return [_build_detail(r) for r in routes]


@router.post(
    "",
    response_model=RouteDetailRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a route with an initial stop sequence",
)
async def create_route(body: RouteCreate, session: SessionDep) -> RouteDetailRead:
    from sqlalchemy import select

    route = Route(
        name=body.name,
        description=body.description,
        is_active=body.is_active,
    )
    session.add(route)
    await session.flush()  # get route.id

    for s in body.stops:
        rs = RouteStop(
            route_id=route.id,
            stop_id=s.stop_id,
            stop_order=s.stop_order,
            distance_from_prev_m=s.distance_from_prev_m,
        )
        session.add(rs)

    await session.commit()

    # Reload with relationships
    result = await session.execute(
        select(Route)
        .where(Route.id == route.id)
        .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
    )
    route = result.scalar_one()
    return _build_detail(route)


@router.put("/{route_id}", response_model=RouteDetailRead, summary="Update a route")
async def update_route(
    route_id: UUID, body: RouteUpdate, session: SessionDep
) -> RouteDetailRead:
    from sqlalchemy import select, delete

    result = await session.execute(
        select(Route)
        .where(Route.id == route_id)
        .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
    )
    route = result.scalar_one_or_none()
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")

    if body.name is not None:
        route.name = body.name
    if body.description is not None:
        route.description = body.description
    if body.is_active is not None:
        route.is_active = body.is_active

    if body.stops is not None:
        # Replace stop sequence entirely
        await session.execute(
            delete(RouteStop).where(RouteStop.route_id == route_id)
        )
        for s in body.stops:
            session.add(
                RouteStop(
                    route_id=route_id,
                    stop_id=s.stop_id,
                    stop_order=s.stop_order,
                    distance_from_prev_m=s.distance_from_prev_m,
                )
            )

    await session.commit()

    result = await session.execute(
        select(Route)
        .where(Route.id == route_id)
        .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
    )
    route = result.scalar_one()
    return _build_detail(route)


@router.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate a route (soft delete)",
)
async def deactivate_route(route_id: UUID, session: SessionDep) -> None:
    repo = RouteRepository(session)
    route = await repo.deactivate(route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    await session.commit()
