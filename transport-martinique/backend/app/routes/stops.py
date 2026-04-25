from fastapi import APIRouter
import httpx
import csv
import io
import zipfile
import tempfile

router = APIRouter()


@router.get("/stops")
async def get_stops():
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
                    with z.open("stops.txt") as stops_file:
                        text = stops_file.read().decode("utf-8")
                        f = io.StringIO(text)
                        reader = csv.DictReader(f)
                        stops = [row for row in reader]
                        print("First 3 stops:", stops[:3])
                        return stops
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}
