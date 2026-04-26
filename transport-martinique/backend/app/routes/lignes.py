from fastapi import APIRouter
import httpx
import csv
import io
import zipfile
import tempfile
import time

router = APIRouter()

# --- Simple in-memory cache for the GTFS ZIP ---
_gtfs_cache = {"data": None, "fetched_at": 0}
CACHE_TTL = 300  # seconds (5 minutes)

ZIP_URL = "https://static.data.gouv.fr/resources/gtfs-urbain-de-la-zone-centre/20260305-184002/gtfs-centre-rtm.zip"

async def get_gtfs_zip() -> zipfile.ZipFile:
    """
    Downloads and caches the GTFS ZIP in memory.
    Returns a ZipFile object. Re-fetches if older than CACHE_TTL seconds.
    """
    now = time.time()
    if _gtfs_cache["data"] is not None and (now - _gtfs_cache["fetched_at"]) < CACHE_TTL:
        return zipfile.ZipFile(io.BytesIO(_gtfs_cache["data"]))

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(ZIP_URL)
        resp.raise_for_status()
        _gtfs_cache["data"] = resp.content
        _gtfs_cache["fetched_at"] = now
        return zipfile.ZipFile(io.BytesIO(resp.content))


def read_csv_from_zip(z: zipfile.ZipFile, filename: str) -> list[dict]:
    with z.open(filename) as f:
        return list(csv.DictReader(io.StringIO(f.read().decode("utf-8"))))


@router.get("/lignes")
async def get_lignes():
    try:
        z = await get_gtfs_zip()
        lignes = read_csv_from_zip(z, "routes.txt")
        return lignes
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/lignes/{line_id}/stops")
async def get_stops_for_line(line_id: str):
    try:
        z = await get_gtfs_zip()
        trips = read_csv_from_zip(z, "trips.txt")
        stop_times = read_csv_from_zip(z, "stop_times.txt")
        stops = read_csv_from_zip(z, "stops.txt")

        trip_ids = {t["trip_id"] for t in trips if t["route_id"] == line_id}
        if not trip_ids:
            return {"error": "No trips found for this line_id"}

        stop_id_set = set()
        stop_id_order = []
        for st in stop_times:
            if st["trip_id"] in trip_ids:
                sid = st["stop_id"]
                if sid not in stop_id_set:
                    stop_id_set.add(sid)
                    stop_id_order.append((int(st["stop_sequence"]), sid))

        stop_id_order.sort()
        ordered_stop_ids = [sid for _, sid in stop_id_order]
        stop_dict = {s["stop_id"]: s for s in stops}

        return [stop_dict[sid] for sid in ordered_stop_ids if sid in stop_dict]
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/lignes/{line_id}/shape")
async def get_shape_for_line(line_id: str):
    try:
        z = await get_gtfs_zip()
        trips = read_csv_from_zip(z, "trips.txt")
        shapes = read_csv_from_zip(z, "shapes.txt")

        trip = next((t for t in trips if t["route_id"] == line_id), None)
        if not trip:
            return {"error": "No trip found for this line_id"}

        shape_id = trip["shape_id"]
        shape_points = sorted(
            [s for s in shapes if s["shape_id"] == shape_id],
            key=lambda s: int(s["shape_pt_sequence"])
        )
        return [
            {"lat": float(s["shape_pt_lat"]), "lon": float(s["shape_pt_lon"])}
            for s in shape_points
        ]
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/lignes/{line_id}/buses")
async def get_simulated_buses_for_line(line_id: str, n_buses: int = 2):
    try:
        z = await get_gtfs_zip()
        trips = read_csv_from_zip(z, "trips.txt")
        shapes = read_csv_from_zip(z, "shapes.txt")

        trip = next((t for t in trips if t["route_id"] == line_id), None)
        if not trip:
            return {"error": "No trip found for this line_id"}

        shape_id = trip["shape_id"]
        shape_points = sorted(
            [s for s in shapes if s["shape_id"] == shape_id],
            key=lambda s: int(s["shape_pt_sequence"])
        )
        polyline = [
            {"lat": float(s["shape_pt_lat"]), "lon": float(s["shape_pt_lon"])}
            for s in shape_points
        ]
        if not polyline:
            return {"error": "No shape points found for this line_id"}

        now = int(time.time())
        buses = []
        n = len(polyline)
        for i in range(n_buses):
            idx = (now // 5 + i * (n // max(n_buses, 1))) % n
            pos = polyline[idx]
            buses.append({
                "bus_id": f"bus_{line_id}_{i + 1}",
                "lat": pos["lat"],
                "lon": pos["lon"],
                "progress": idx / (n - 1),
                "timestamp": now
            })
        return buses
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}