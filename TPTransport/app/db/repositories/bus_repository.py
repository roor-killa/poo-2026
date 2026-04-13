from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.bus import Bus
from app.db.repositories.base import BaseRepository


class BusRepository(BaseRepository[Bus]):
    model = Bus

    async def get_with_related(self, bus_id) -> Optional[Bus]:
        result = await self.session.execute(
            select(Bus)
            .where(Bus.id == bus_id)
            .options(selectinload(Bus.status), selectinload(Bus.route))
        )
        return result.scalar_one_or_none()

    async def get_by_token(self, token: str) -> Optional[Bus]:
        result = await self.session.execute(
            select(Bus).where(Bus.api_token == token, Bus.is_active.is_(True))
        )
        return result.scalar_one_or_none()

    async def list_active(self) -> Sequence[Bus]:
        result = await self.session.execute(
            select(Bus)
            .where(Bus.is_active.is_(True))
            .options(selectinload(Bus.status), selectinload(Bus.route))
        )
        return result.scalars().all()

    async def list_all(self) -> Sequence[Bus]:
        result = await self.session.execute(
            select(Bus).options(selectinload(Bus.status), selectinload(Bus.route))
        )
        return result.scalars().all()

    async def deactivate(self, bus_id) -> Optional[Bus]:
        bus = await self.get(bus_id)
        if bus:
            bus.is_active = False
            await self.session.flush()
        return bus
