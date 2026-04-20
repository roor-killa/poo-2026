from fastapi import APIRouter
import httpx
import csv
import io

router = APIRouter()


@router.get("/stops")
async def get_stops():
    url = "https://transport.data.gouv.fr/gtfs/urbain/urbain-zone-centre/stops.txt"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        f = io.StringIO(resp.text)
        reader = csv.DictReader(f)
        stops = [row for row in reader]
        return stops
