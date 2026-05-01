from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.route import Route
from app.db.models.route_stop import RouteStop
from app.db.repositories.base import BaseRepository


class RouteRepository(BaseRepository[Route]):
    model = Route

    async def list_active(self) -> Sequence[Route]:
        result = await self.session.execute(
            select(Route)
            .where(Route.is_active.is_(True))
            .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
        )
        return result.scalars().all()

    async def get_with_stops(self, route_id: UUID) -> Optional[Route]:
        result = await self.session.execute(
            select(Route)
            .where(Route.id == route_id)
            .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
        )
        return result.scalar_one_or_none()

    async def deactivate(self, route_id: UUID) -> Optional[Route]:
        route = await self.get(route_id)
        if route:
            route.is_active = False
            await self.session.flush()
        return route
