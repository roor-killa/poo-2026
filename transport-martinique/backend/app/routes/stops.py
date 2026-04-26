from fastapi import APIRouter
from .lignes import get_gtfs_zip, read_csv

router = APIRouter()


@router.get("/stops")
async def get_stops():
    """Returns all stops from stops.txt."""
    try:
        z = await get_gtfs_zip()
        return read_csv(z, "stops.txt")
    except Exception as e:
        return {"error": str(e)}


@router.get("/stops/{stop_id}")
async def get_stop(stop_id: str):
    """Returns a single stop by stop_id."""
    try:
        z = await get_gtfs_zip()
        stops = read_csv(z, "stops.txt")
        stop = next((s for s in stops if s["stop_id"] == stop_id), None)
        if not stop:
            return {"error": "Stop not found"}
        return stop
    except Exception as e:
        return {"error": str(e)}