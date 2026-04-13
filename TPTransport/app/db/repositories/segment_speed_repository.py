from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.models.segment_speed import SegmentSpeed
from app.db.repositories.base import BaseRepository

DEFAULT_SPEED_KMH = 20.0
EMA_ALPHA = 0.1


class SegmentSpeedRepository(BaseRepository[SegmentSpeed]):
    model = SegmentSpeed

    async def get(  # type: ignore[override]
        self,
        route_id: UUID,
        from_order: int,
        to_order: int,
        hour_bucket: int,
        day_type: str,
    ) -> Optional[SegmentSpeed]:
        result = await self.session.execute(
            select(SegmentSpeed).where(
                SegmentSpeed.route_id == route_id,
                SegmentSpeed.from_stop_order == from_order,
                SegmentSpeed.to_stop_order == to_order,
                SegmentSpeed.hour_bucket == hour_bucket,
                SegmentSpeed.day_type == day_type,
            )
        )
        return result.scalar_one_or_none()

    async def get_speed_kmh(
        self,
        route_id: UUID,
        from_order: int,
        to_order: int,
        hour_bucket: int,
        day_type: str,
    ) -> float:
        """Return avg_speed_kmh or DEFAULT_SPEED_KMH when no sample exists."""
        row = await self.get(route_id, from_order, to_order, hour_bucket, day_type)
        if row is None or row.sample_count == 0:
            return DEFAULT_SPEED_KMH
        return row.avg_speed_kmh

    async def upsert_ema(
        self,
        route_id: UUID,
        from_order: int,
        to_order: int,
        hour_bucket: int,
        day_type: str,
        observed_speed_kmh: float,
    ) -> SegmentSpeed:
        """Insert or update using exponential moving average (α=0.1)."""
        row = await self.get(route_id, from_order, to_order, hour_bucket, day_type)
        if row is None:
            row = SegmentSpeed(
                route_id=route_id,
                from_stop_order=from_order,
                to_stop_order=to_order,
                hour_bucket=hour_bucket,
                day_type=day_type,
                avg_speed_kmh=observed_speed_kmh,
                sample_count=1,
            )
            self.session.add(row)
        else:
            row.avg_speed_kmh = EMA_ALPHA * observed_speed_kmh + (1 - EMA_ALPHA) * row.avg_speed_kmh
            row.sample_count += 1
        await self.session.flush()
        return row
