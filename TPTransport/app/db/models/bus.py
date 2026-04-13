import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.bus_status import BusStatus
    from app.db.models.position import Position
    from app.db.models.route import Route


class Bus(Base):
    __tablename__ = "buses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    label: Mapped[Optional[str]] = mapped_column(String(80))
    route_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id", ondelete="SET NULL"), nullable=True
    )
    api_token: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

    route: Mapped[Optional["Route"]] = relationship("Route", back_populates="buses")
    positions: Mapped[List["Position"]] = relationship(
        "Position", back_populates="bus", cascade="all, delete-orphan"
    )
    status: Mapped[Optional["BusStatus"]] = relationship(
        "BusStatus", back_populates="bus", uselist=False, cascade="all, delete-orphan"
    )
