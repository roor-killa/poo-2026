from fastapi import APIRouter
import httpx
import csv
import io
import zipfile
import time
from zoneinfo import ZoneInfo

MARTINIQUE_TZ = ZoneInfo("America/Martinique")

router = APIRouter()

# ── In-memory GTFS cache ──────────────────────────────────────────────────────
_gtfs_cache: dict = {"data": None, "fetched_at": 0}
CACHE_TTL = 300  # 5 minutes

ZIP_URL = "https://static.data.gouv.fr/resources/gtfs-urbain-de-la-zone-centre/20260305-184002/gtfs-centre-rtm.zip"


async def get_gtfs_zip() -> zipfile.ZipFile:
    now = time.time()
    if _gtfs_cache["data"] and (now - _gtfs_cache["fetched_at"]) < CACHE_TTL:
        return zipfile.ZipFile(io.BytesIO(_gtfs_cache["data"]))
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(ZIP_URL)
        resp.raise_for_status()
        _gtfs_cache["data"] = resp.content
        _gtfs_cache["fetched_at"] = now
        return zipfile.ZipFile(io.BytesIO(resp.content))


def read_csv(z: zipfile.ZipFile, filename: str) -> list[dict]:
    with z.open(filename) as f:
        return list(csv.DictReader(io.StringIO(f.read().decode("utf-8"))))


# ── /lignes ───────────────────────────────────────────────────────────────────
@router.get("/lignes")
async def get_lignes():
    try:
        z = await get_gtfs_zip()
        return read_csv(z, "routes.txt")
    except Exception as e:
        return {"error": str(e)}


# ── /search ───────────────────────────────────────────────────────────────────
@router.get("/search")
async def search(q: str):
    """
    Full-text search across stops (stop_name) and lines (route_short_name /
    route_long_name). Returns { stops: [...], lines: [...] }.
    """
    if len(q.strip()) < 2:
        return {"stops": [], "lines": []}
    try:
        z = await get_gtfs_zip()
        stops = read_csv(z, "stops.txt")
        routes = read_csv(z, "routes.txt")
        q_low = q.strip().lower()

        matched_stops = [
            {**s, "type": "stop"} for s in stops
            if q_low in s.get("stop_name", "").lower()
        ][:12]

        matched_lines = [
            {**r, "type": "line"} for r in routes
            if q_low in r.get("route_short_name", "").lower()
            or q_low in r.get("route_long_name", "").lower()
        ][:8]

        return {"stops": matched_stops, "lines": matched_lines}
    except Exception as e:
        return {"error": str(e)}


# ── /lignes/{line_id}/directions ──────────────────────────────────────────────
@router.get("/lignes/{line_id}/directions")
async def get_directions(line_id: str):
    """
    Returns the two directions available for a line, deduped by direction_id,
    with the representative trip_headsign for each.
    """
    try:
        z = await get_gtfs_zip()
        trips = read_csv(z, "trips.txt")

        seen: dict = {}
        for t in trips:
            if t["route_id"] != line_id:
                continue
            d = t.get("direction_id", "0")
            if d not in seen:
                seen[d] = {
                    "direction_id": d,
                    "headsign": t.get("trip_headsign", f"Direction {d}"),
                    "shape_id": t.get("shape_id", ""),
                }
        return list(seen.values())
    except Exception as e:
        return {"error": str(e)}


# ── /lignes/{line_id}/stops ───────────────────────────────────────────────────
@router.get("/lignes/{line_id}/stops")
async def get_stops_for_line(line_id: str, direction_id: str = "0"):
    """
    Returns the ordered list of stops for a line in a given direction.
    Falls back to the first available trip if no match for direction_id.
    """
    try:
        z = await get_gtfs_zip()
        trips = read_csv(z, "trips.txt")
        stop_times = read_csv(z, "stop_times.txt")
        stops = read_csv(z, "stops.txt")

        # Pick a representative trip for this direction
        trip = next(
            (t for t in trips if t["route_id"] == line_id and t.get("direction_id", "0") == direction_id),
            None
        ) or next((t for t in trips if t["route_id"] == line_id), None)

        if not trip:
            return {"error": "No trip found for this line_id"}

        trip_stops = sorted(
            [st for st in stop_times if st["trip_id"] == trip["trip_id"]],
            key=lambda st: int(st["stop_sequence"])
        )
        stop_dict = {s["stop_id"]: s for s in stops}
        return [stop_dict[st["stop_id"]] for st in trip_stops if st["stop_id"] in stop_dict]
    except Exception as e:
        return {"error": str(e)}


# ── /lignes/{line_id}/shape ───────────────────────────────────────────────────
@router.get("/lignes/{line_id}/shape")
async def get_shape_for_line(line_id: str, direction_id: str = "0"):
    """
    Returns the ordered polyline (list of {lat, lon}) for a line / direction.
    """
    try:
        z = await get_gtfs_zip()
        trips = read_csv(z, "trips.txt")
        shapes = read_csv(z, "shapes.txt")

        trip = next(
            (t for t in trips if t["route_id"] == line_id and t.get("direction_id", "0") == direction_id),
            None
        ) or next((t for t in trips if t["route_id"] == line_id), None)

        if not trip:
            return {"error": "No trip found for this line_id"}

        pts = sorted(
            [s for s in shapes if s["shape_id"] == trip["shape_id"]],
            key=lambda s: int(s["shape_pt_sequence"])
        )
        return [{"lat": float(s["shape_pt_lat"]), "lon": float(s["shape_pt_lon"])} for s in pts]
    except Exception as e:
        return {"error": str(e)}


# ── /stops/{stop_id}/next-departures ─────────────────────────────────────────
@router.get("/stops/{stop_id}/next-departures")
async def get_next_departures(stop_id: str, limit: int = 12):
    """
    Scans stop_times for departures at this stop that are still in the future
    relative to the current wall-clock time. Returns at most `limit` results
    sorted by minutes until departure.

    MVP note: ignores calendar.txt / calendar_dates.txt — all service patterns
    are treated as active. In production you would filter by today's service_id.
    """
    try:
        z = await get_gtfs_zip()
        stop_times = read_csv(z, "stop_times.txt")
        trips = read_csv(z, "trips.txt")
        routes = read_csv(z, "routes.txt")

        trip_dict = {t["trip_id"]: t for t in trips}
        route_dict = {r["route_id"]: r for r in routes}

        # Always use Martinique local time (UTC-4) regardless of server timezone
        from datetime import datetime
        now_mq = datetime.now(MARTINIQUE_TZ)
        current_sec = now_mq.hour * 3600 + now_mq.minute * 60 + now_mq.second

        # Build a lookup of stop_times for this stop only
        stop_entries = [st for st in stop_times if st["stop_id"] == stop_id]

        departures = []
        for st in stop_entries:
            try:
                # GTFS allows hours >= 24 for post-midnight trips (e.g. "25:10:00")
                parts = st["departure_time"].split(":")
                h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
                dep_sec = h * 3600 + m * 60 + s
            except Exception:
                continue

            # Treat post-midnight trips (h >= 24) as belonging to the same service day
            # so they always appear after all normal-day trips
            if dep_sec < current_sec:
                continue

            trip = trip_dict.get(st["trip_id"], {})
            route = route_dict.get(trip.get("route_id", ""), {})
            # Format display time — clamp hours >= 24 back to HH:MM
            display_h = h % 24
            display_time = f"{display_h:02d}:{m:02d}"
            departures.append({
                "departure_time": display_time,
                "minutes_until": (dep_sec - current_sec) // 60,
                "trip_headsign": trip.get("trip_headsign", ""),
                "direction_id": trip.get("direction_id", "0"),
                "route_id": trip.get("route_id", ""),
                "route_short_name": route.get("route_short_name", ""),
                "route_long_name": route.get("route_long_name", ""),
                "route_color": route.get("route_color", "0074D9"),
                "route_text_color": route.get("route_text_color", "FFFFFF"),
            })

        departures.sort(key=lambda x: x["minutes_until"])
        return departures[:limit]
    except Exception as e:
        return {"error": str(e)}


# ── /lignes/{line_id}/buses ───────────────────────────────────────────────────
@router.get("/lignes/{line_id}/buses")
async def get_simulated_buses(line_id: str, n_buses: int = 3, direction_id: str = "0"):
    """
    Simulates n_buses moving along the route polyline.
    Positions advance every 5 s and are spread evenly across the shape.
    """
    try:
        z = await get_gtfs_zip()
        trips = read_csv(z, "trips.txt")
        shapes = read_csv(z, "shapes.txt")

        trip = next(
            (t for t in trips if t["route_id"] == line_id and t.get("direction_id", "0") == direction_id),
            None
        ) or next((t for t in trips if t["route_id"] == line_id), None)

        if not trip:
            return {"error": "No trip found"}

        pts = sorted(
            [s for s in shapes if s["shape_id"] == trip["shape_id"]],
            key=lambda s: int(s["shape_pt_sequence"])
        )
        polyline = [{"lat": float(s["shape_pt_lat"]), "lon": float(s["shape_pt_lon"])} for s in pts]
        if not polyline:
            return {"error": "No shape points found"}

        now = int(time.time())
        n = len(polyline)
        buses = []
        for i in range(n_buses):
            idx = (now // 5 + i * (n // max(n_buses, 1))) % n
            pos = polyline[idx]
            buses.append({
                "bus_id": f"bus_{line_id}_d{direction_id}_{i + 1}",
                "lat": pos["lat"],
                "lon": pos["lon"],
                "progress": round(idx / max(n - 1, 1), 3),
                "timestamp": now,
            })
        return buses
    except Exception as e:
        return {"error": str(e)}