"""gpsd interface — thin wrapper around gpsd-py3.

Returns a ``GpsFix`` dataclass when a valid 2-D or 3-D fix is available,
or ``None`` when the GPS has no lock (MODE < 2).

gpsd-py3 docs: https://github.com/MartijnBraam/gpsd-py3
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

import gpsd  # gpsd-py3

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class GpsFix:
    latitude: float
    longitude: float
    speed_kmh: float | None   # gpsd reports speed in m/s; converted here
    heading: float | None     # track angle in degrees (0–360)
    recorded_at: datetime     # UTC timestamp from GPS (falls back to system time)


def read_fix(host: str, port: int) -> GpsFix | None:
    """Connect to gpsd, read one fix, and return it.

    Returns ``None`` if:
    - gpsd is unreachable
    - GPS mode < 2 (no valid fix)
    - latitude or longitude is NaN / None

    A new connection is made on every call (stateless, tolerates gpsd restarts).
    """
    try:
        gpsd.connect(host=host, port=port)
        packet = gpsd.get_current()
    except Exception as exc:
        log.warning("gpsd unreachable: %s", exc)
        return None

    # gpsd mode: 0=unknown, 1=no fix, 2=2D, 3=3D
    if packet.mode < 2:
        log.debug("No GPS fix (mode=%d)", packet.mode)
        return None

    lat = getattr(packet, "lat", None)
    lon = getattr(packet, "lon", None)
    if lat is None or lon is None:
        return None

    # Speed: gpsd gives m/s — convert to km/h
    speed_ms: float | None = getattr(packet, "hspeed", None) or getattr(packet, "speed", None)
    speed_kmh = speed_ms * 3.6 if speed_ms is not None else None

    heading: float | None = getattr(packet, "track", None)  # degrees true

    # Timestamp: prefer GPS time, fall back to system UTC
    gps_time: float | None = getattr(packet, "time", None)
    if gps_time:
        try:
            recorded_at = datetime.fromtimestamp(gps_time, tz=timezone.utc)
        except (OSError, OverflowError, ValueError):
            recorded_at = datetime.now(tz=timezone.utc)
    else:
        recorded_at = datetime.now(tz=timezone.utc)

    return GpsFix(
        latitude=float(lat),
        longitude=float(lon),
        speed_kmh=round(speed_kmh, 2) if speed_kmh is not None else None,
        heading=round(heading % 360, 1) if heading is not None else None,
        recorded_at=recorded_at,
    )
