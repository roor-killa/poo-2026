from datetime import datetime, timedelta, timezone
from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.models.position import Position
from app.db.repositories.base import BaseRepository


class PositionRepository(BaseRepository[Position]):
    model = Position

    async def get_recent_for_bus(
        self, bus_id: UUID, limit: int = 20
    ) -> Sequence[Position]:
        result = await self.session.execute(
            select(Position)
            .where(Position.bus_id == bus_id)
            .order_by(Position.recorded_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def count_last_hour(self, bus_id: UUID) -> int:
        from sqlalchemy import func

        cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        result = await self.session.execute(
            select(func.count()).where(
                Position.bus_id == bus_id, Position.received_at >= cutoff
            )
        )
        return result.scalar_one()
