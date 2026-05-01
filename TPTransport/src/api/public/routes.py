"""GET /api/v1/public/routes — public route endpoints (spec §3.2)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from src.api.deps import PUBLIC_RATE, SessionDep, limiter
from src.repositories import RouteRepository
from src.schemas.route import RouteDetailRead, RouteRead
from src.schemas.stop import StopRead
from src.schemas.route import RouteStopRead
from src.services.geo import wkb_to_latlon

router = APIRouter(prefix="/api/v1/public/routes", tags=["public"])


def _stop_read(stop) -> StopRead:
    lat, lon = wkb_to_latlon(stop.location)
    return StopRead(id=stop.id, name=stop.name, lat=lat, lon=lon, created_at=stop.created_at)


def _route_stop_read(rs) -> RouteStopRead:
    return RouteStopRead(
        id=rs.id,
        stop_order=rs.stop_order,
        distance_from_prev_m=rs.distance_from_prev_m,
        stop=_stop_read(rs.stop),
    )


def _route_detail(route) -> RouteDetailRead:
    return RouteDetailRead(
        id=route.id,
        name=route.name,
        description=route.description,
        is_active=route.is_active,
        created_at=route.created_at,
        updated_at=route.updated_at,
        route_stops=[_route_stop_read(rs) for rs in route.route_stops],
    )


@router.get(
    "",
    response_model=list[RouteDetailRead],
    summary="List all active routes with their ordered stop sequences",
)
@limiter.limit(PUBLIC_RATE)
async def list_routes(request: Request, session: SessionDep) -> list[RouteDetailRead]:
    repo = RouteRepository(session)
    routes = await repo.list_active()
    return [_route_detail(r) for r in routes]


@router.get(
    "/{route_id}",
    response_model=RouteDetailRead,
    summary="Get a route with its ordered stops",
)
@limiter.limit(PUBLIC_RATE)
async def get_route(request: Request, route_id: UUID, session: SessionDep) -> RouteDetailRead:
    repo = RouteRepository(session)
    route = await repo.get_with_stops(route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return _route_detail(route)
