
from fastapi import APIRouter
import httpx
import csv
import io
import zipfile
import tempfile

# Router must be defined before any route decorators
router = APIRouter()

@router.get("/lignes")
async def get_lignes():
    # Download the GTFS ZIP file
    zip_url = "https://static.data.gouv.fr/resources/gtfs-urbain-de-la-zone-centre/20260305-184002/gtfs-centre-rtm.zip"
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(zip_url)
            resp.raise_for_status()
            # Write ZIP to a temp file
            with tempfile.NamedTemporaryFile(delete=True) as tmp_zip:
                tmp_zip.write(resp.content)
                tmp_zip.flush()
                with zipfile.ZipFile(tmp_zip.name) as z:
                    with z.open("routes.txt") as lignes_file:
                        text = lignes_file.read().decode("utf-8")
                        f = io.StringIO(text)
                        reader = csv.DictReader(f)
                        lignes = [row for row in reader]
                        print("First 3 lignes:", lignes[:3])
                        return lignes
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


# New endpoint: Get stops for a specific line
@router.get("/lignes/{line_id}/stops")
async def get_stops_for_line(line_id: str):
    """
    Returns the stops for a given line (route_id from routes.txt)
    """
    zip_url = "https://static.data.gouv.fr/resources/gtfs-urbain-de-la-zone-centre/20260305-184002/gtfs-centre-rtm.zip"
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(zip_url)
            resp.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=True) as tmp_zip:
                tmp_zip.write(resp.content)
                tmp_zip.flush()
                with zipfile.ZipFile(tmp_zip.name) as z:
                    # Load all relevant GTFS files
                    with z.open("routes.txt") as routes_file:
                        routes = list(csv.DictReader(io.StringIO(routes_file.read().decode("utf-8"))))
                    with z.open("trips.txt") as trips_file:
                        trips = list(csv.DictReader(io.StringIO(trips_file.read().decode("utf-8"))))
                    with z.open("stop_times.txt") as stop_times_file:
                        stop_times = list(csv.DictReader(io.StringIO(stop_times_file.read().decode("utf-8"))))
                    with z.open("stops.txt") as stops_file:
                        stops = list(csv.DictReader(io.StringIO(stops_file.read().decode("utf-8"))))

                    # 1. Find all trip_ids for the given line_id (route_id)
                    trip_ids = set([trip['trip_id'] for trip in trips if trip['route_id'] == line_id])
                    if not trip_ids:
                        return {"error": "No trips found for this line_id"}

                    # 2. Find all stop_ids for those trips (in order)
                    stop_id_set = set()
                    stop_id_order = []
                    for st in stop_times:
                        if st['trip_id'] in trip_ids:
                            sid = st['stop_id']
                            if sid not in stop_id_set:
                                stop_id_set.add(sid)
                                stop_id_order.append((int(st['stop_sequence']), sid))
                    stop_id_order.sort()
                    ordered_stop_ids = [sid for _, sid in stop_id_order]

                    # 3. Get stop details for those stop_ids
                    stop_dict = {stop['stop_id']: stop for stop in stops}
                    stops_for_line = [stop_dict[sid] for sid in ordered_stop_ids if sid in stop_dict]

                    return stops_for_line
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


@router.get("/lignes/{line_id}/shape")
async def get_shape_for_line(line_id: str):
    """
    Returns the polyline (list of lat/lon) for a given line (route_id) using shapes.txt
    """
    zip_url = "https://static.data.gouv.fr/resources/gtfs-urbain-de-la-zone-centre/20260305-184002/gtfs-centre-rtm.zip"
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(zip_url)
            resp.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=True) as tmp_zip:
                tmp_zip.write(resp.content)
                tmp_zip.flush()
                with zipfile.ZipFile(tmp_zip.name) as z:
                    # Load trips.txt and shapes.txt
                    with z.open("trips.txt") as trips_file:
                        trips = list(csv.DictReader(io.StringIO(trips_file.read().decode("utf-8"))))
                    with z.open("shapes.txt") as shapes_file:
                        shapes = list(csv.DictReader(io.StringIO(shapes_file.read().decode("utf-8"))))

                    # 1. Find a trip for the given line_id (route_id)
                    trip = next((t for t in trips if t['route_id'] == line_id), None)
                    if not trip:
                        return {"error": "No trip found for this line_id"}
                    shape_id = trip['shape_id']

                    # 2. Get all shape points for this shape_id, ordered by shape_pt_sequence
                    shape_points = [s for s in shapes if s['shape_id'] == shape_id]
                    shape_points.sort(key=lambda s: int(s['shape_pt_sequence']))
                    polyline = [
                        {"lat": float(s['shape_pt_lat']), "lon": float(s['shape_pt_lon'])}
                        for s in shape_points
                    ]
                    return polyline
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}