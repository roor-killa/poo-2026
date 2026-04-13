from typing import Sequence
from uuid import UUID

from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from sqlalchemy import cast, select
from geoalchemy2 import Geography

from app.db.models.stop import Stop
from app.db.repositories.base import BaseRepository


class StopRepository(BaseRepository[Stop]):
    model = Stop

    async def find_within_meters(self, lon: float, lat: float, radius_m: float) -> Sequence[Stop]:
        """Return stops within radius_m metres of the given coordinates."""
        point = cast(ST_MakePoint(lon, lat), Geography)
        result = await self.session.execute(
            select(Stop).where(ST_DWithin(Stop.location, point, radius_m))
        )
        return result.scalars().all()

    async def get_stops_for_route(self, route_id: UUID) -> Sequence[Stop]:
        from app.db.models.route_stop import RouteStop

        result = await self.session.execute(
            select(Stop)
            .join(RouteStop, RouteStop.stop_id == Stop.id)
            .where(RouteStop.route_id == route_id)
            .order_by(RouteStop.stop_order)
        )
        return result.scalars().all()
