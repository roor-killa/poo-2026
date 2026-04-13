import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from geoalchemy2 import Geography
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.route_stop import RouteStop


class Stop(Base):
    __tablename__ = "stops"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # GEOGRAPHY(POINT, 4326) — stored as WKB; use geoalchemy2.shape.to_shape() to get shapely Point
    location: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

    route_stops: Mapped[List["RouteStop"]] = relationship(
        "RouteStop", back_populates="stop"
    )
