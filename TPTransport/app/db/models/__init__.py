# Import all models so that Base.metadata is fully populated (needed by Alembic autogenerate)
from app.db.models.bus import Bus
from app.db.models.bus_status import BusStatus
from app.db.models.position import Position
from app.db.models.route import Route
from app.db.models.route_stop import RouteStop
from app.db.models.segment_speed import SegmentSpeed
from app.db.models.stop import Stop

__all__ = [
    "Bus",
    "BusStatus",
    "Position",
    "Route",
    "RouteStop",
    "SegmentSpeed",
    "Stop",
]
