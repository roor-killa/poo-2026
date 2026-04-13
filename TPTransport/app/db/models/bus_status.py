import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geography
from sqlalchemy import Boolean, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.bus import Bus
    from app.db.models.stop import Stop


class BusStatus(Base):
    __tablename__ = "bus_status"

    bus_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("buses.id", ondelete="CASCADE"), primary_key=True
    )
    last_location: Mapped[Optional[object]] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )
    last_speed_kmh: Mapped[Optional[float]] = mapped_column()
    last_seen_at: Mapped[Optional[datetime]] = mapped_column()
    is_online: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    current_stop_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stops.id"), nullable=True
    )
    next_stop_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stops.id"), nullable=True
    )
    eta_next_stop_s: Mapped[Optional[int]] = mapped_column(Integer)
    eta_terminus_s: Mapped[Optional[int]] = mapped_column(Integer)
    progress_pct: Mapped[Optional[float]] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    bus: Mapped["Bus"] = relationship("Bus", back_populates="status")
    current_stop: Mapped[Optional["Stop"]] = relationship(
        "Stop", foreign_keys=[current_stop_id]
    )
    next_stop: Mapped[Optional["Stop"]] = relationship(
        "Stop", foreign_keys=[next_stop_id]
    )
