from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.bus import Bus
from app.db.models.bus_status import BusStatus
from app.db.repositories.base import BaseRepository


class BusRepository(BaseRepository[Bus]):
    model = Bus

    def _status_opts(self):
        return selectinload(Bus.status).options(
            selectinload(BusStatus.current_stop),
            selectinload(BusStatus.next_stop),
        )

    async def get_with_related(self, bus_id) -> Optional[Bus]:
        result = await self.session.execute(
            select(Bus)
            .where(Bus.id == bus_id)
            .options(self._status_opts(), selectinload(Bus.route))
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
            .options(self._status_opts(), selectinload(Bus.route))
        )
        return result.scalars().all()

    async def list_all(self) -> Sequence[Bus]:
        result = await self.session.execute(
            select(Bus).options(self._status_opts(), selectinload(Bus.route))
        )
        return result.scalars().all()

    async def deactivate(self, bus_id) -> Optional[Bus]:
        bus = await self.get(bus_id)
        if bus:
            bus.is_active = False
            await self.session.flush()
        return bus
