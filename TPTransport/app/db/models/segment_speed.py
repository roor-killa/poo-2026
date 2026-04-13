import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, SmallInteger, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.route import Route


class SegmentSpeed(Base):
    __tablename__ = "segment_speeds"
    __table_args__ = (
        UniqueConstraint("route_id", "from_stop_order", "to_stop_order", "hour_bucket", "day_type"),
        CheckConstraint("hour_bucket BETWEEN 0 AND 23", name="ck_hour_bucket"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False
    )
    from_stop_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    to_stop_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    hour_bucket: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    day_type: Mapped[str] = mapped_column(String(10), nullable=False, default="weekday")
    avg_speed_kmh: Mapped[float] = mapped_column(nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    route: Mapped["Route"] = relationship("Route", back_populates="segment_speeds")
