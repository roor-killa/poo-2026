"""Pure ETA and progress calculations — no DB calls (spec §5.2, §5.3).

All inputs are plain Python values; callers (position_service) fetch the
required data from repositories before calling these functions.
"""

from __future__ import annotations

from dataclasses import dataclass

# Spec §5.2 configurable weights
V_AVG_WEIGHT: float = 0.7
V_INSTANT_WEIGHT: float = 0.3
V_EFFECTIVE_MIN_KMH: float = 2.0   # below this, ignore instant speed
DEFAULT_SPEED_KMH: float = 20.0    # fallback when sample_count == 0


@dataclass(frozen=True)
class SegmentInfo:
    """Enough data about one route segment to compute an ETA contribution."""

    distance_m: float          # distance_from_prev_m of the *destination* stop
    avg_speed_kmh: float       # from segment_speeds (may be DEFAULT_SPEED_KMH)


def effective_speed(v_avg: float, v_instant: float | None) -> float:
    """Blend historical and instantaneous speed per spec §5.2.

    If the blend falls below V_EFFECTIVE_MIN_KMH, fall back to v_avg alone.
    """
    if v_instant is None:
        return v_avg if v_avg >= V_EFFECTIVE_MIN_KMH else DEFAULT_SPEED_KMH

    v_eff = V_AVG_WEIGHT * v_avg + V_INSTANT_WEIGHT * v_instant
    if v_eff < V_EFFECTIVE_MIN_KMH:
        return v_avg if v_avg >= V_EFFECTIVE_MIN_KMH else DEFAULT_SPEED_KMH
    return v_eff


def eta_seconds(distance_m: float, speed_kmh: float) -> int:
    """Seconds to cover distance_m at speed_kmh (km/h → m/s conversion)."""
    speed_ms = speed_kmh / 3.6
    if speed_ms <= 0:
        return 0
    return max(0, int(distance_m / speed_ms))


def compute_eta_next_stop(
    d_remaining_m: float,
    v_avg_kmh: float,
    v_instant_kmh: float | None,
) -> int:
    """ETA to the next stop in seconds (spec §5.2)."""
    v_eff = effective_speed(v_avg_kmh, v_instant_kmh)
    return eta_seconds(d_remaining_m, v_eff)


def compute_eta_terminus(
    eta_next_s: int,
    remaining_segments: list[SegmentInfo],
) -> int:
    """ETA to terminus in seconds (spec §5.2).

    remaining_segments: ordered list of segments *after* the next stop up to
    and including the terminus stop.  Each entry supplies the segment distance
    and its historical average speed.
    """
    total = eta_next_s
    for seg in remaining_segments:
        v = seg.avg_speed_kmh if seg.avg_speed_kmh >= V_EFFECTIVE_MIN_KMH else DEFAULT_SPEED_KMH
        total += eta_seconds(seg.distance_m, v)
    return total


def compute_progress_pct(
    route_stops_distances: list[float | None],  # distance_from_prev_m, index=stop_order-1
    current_stop_order: int | None,             # 1-based; None = before first stop
    d_to_next_m: float,                         # distance bus→next stop
) -> float:
    """Progression percentage along the route (spec §5.3).

    route_stops_distances: list aligned to stop_order (index 0 = stop_order 1).
      distance_from_prev_m for stop_order 1 is None/0 (start of route).

    Returns a value in [0.0, 100.0].
    """
    # Replace None distances with 0
    distances = [d if d is not None else 0.0 for d in route_stops_distances]
    total_distance = sum(distances)
    if total_distance <= 0:
        return 0.0

    # Sum up distances for stops already passed
    if current_stop_order is None:
        # Bus hasn't reached the first stop yet
        covered = 0.0
        # next stop is stop_order 1; distance to it is distances[0] minus d_to_next
        next_seg_total = distances[0] if distances else 0.0
        covered += max(0.0, next_seg_total - d_to_next_m)
    else:
        # distances[0..current_stop_order-1] are fully covered
        covered = sum(distances[:current_stop_order])
        # partial progress within the current segment toward next stop
        next_idx = current_stop_order  # 0-based index for the *next* stop
        if next_idx < len(distances):
            seg_len = distances[next_idx]
            covered += max(0.0, seg_len - d_to_next_m)

    return min(100.0, covered / total_distance * 100.0)
