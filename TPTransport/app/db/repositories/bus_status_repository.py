from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.bus_status import BusStatus
from app.db.repositories.base import BaseRepository


class BusStatusRepository(BaseRepository[BusStatus]):
    model = BusStatus

    async def get(self, bus_id: UUID) -> Optional[BusStatus]:  # type: ignore[override]
        return await self.session.get(BusStatus, bus_id)

    async def list_online(self) -> Sequence[BusStatus]:
        result = await self.session.execute(
            select(BusStatus)
            .where(BusStatus.is_online.is_(True))
            .options(
                selectinload(BusStatus.bus),
                selectinload(BusStatus.current_stop),
                selectinload(BusStatus.next_stop),
            )
        )
        return result.scalars().all()

    async def list_all(self) -> Sequence[BusStatus]:
        result = await self.session.execute(
            select(BusStatus).options(
                selectinload(BusStatus.bus),
                selectinload(BusStatus.current_stop),
                selectinload(BusStatus.next_stop),
            )
        )
        return result.scalars().all()

    async def upsert(self, status: BusStatus) -> BusStatus:
        """Insert or update a BusStatus row (merge by primary key)."""
        merged = await self.session.merge(status)
        await self.session.flush()
        return merged
