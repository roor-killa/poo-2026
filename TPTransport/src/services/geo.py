"""Geographic helpers used by the service layer.

Keeps all geoalchemy2 / shapely imports in one place so other services stay
clean.  Nothing here touches the DB directly; callers pass WKB elements they
already have from ORM rows.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from geoalchemy2.shape import to_shape  # WKBElement → shapely geometry

if TYPE_CHECKING:
    from geoalchemy2 import WKBElement


def wkb_to_latlon(wkb: "WKBElement") -> tuple[float, float]:
    """Return (lat, lon) from a geoalchemy2 WKBElement (GEOGRAPHY POINT)."""
    point = to_shape(wkb)
    return point.y, point.x  # shapely: x=lon, y=lat


def latlon_to_wkt(lat: float, lon: float) -> str:
    """Build a WKT POINT string accepted by PostGIS GEOGRAPHY columns."""
    return f"SRID=4326;POINT({lon} {lat})"


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two WGS-84 points."""
    R = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))
