import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.bus import Bus
    from app.db.models.route_stop import RouteStop
    from app.db.models.segment_speed import SegmentSpeed


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    route_stops: Mapped[List["RouteStop"]] = relationship(
        "RouteStop", back_populates="route", cascade="all, delete-orphan",
        order_by="RouteStop.stop_order",
    )
    buses: Mapped[List["Bus"]] = relationship("Bus", back_populates="route")
    segment_speeds: Mapped[List["SegmentSpeed"]] = relationship(
        "SegmentSpeed", back_populates="route", cascade="all, delete-orphan"
    )
