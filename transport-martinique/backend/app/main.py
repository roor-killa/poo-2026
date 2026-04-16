from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .data import LINES, STOPS

app = FastAPI(title="Transport Martinique API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _stop_with_lines(stop_id: str):
    stop = next((item for item in STOPS if item["id"] == stop_id), None)
    if not stop:
        return None

    lines_for_stop = [
        {
            "id": line["id"],
            "code": line["code"],
            "name": line["name"],
            "direction": line["direction"],
        }
        for line in LINES
        if stop_id in line["stop_ids"]
    ]
    return {**stop, "lines": lines_for_stop}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/stops")
def get_stops(q: str = "", direction: str = ""):
    query = q.strip().lower()
    direction_query = direction.strip().lower()

    results = []
    for stop in STOPS:
        enriched = _stop_with_lines(stop["id"])
        if enriched is None:
            continue

        if not query and not direction_query:
            results.append(enriched)
            continue

        stop_match = query in enriched["name"].lower() if query else False
        line_match = False

        for line in enriched["lines"]:
            code_match = query in line["code"].lower() if query else False
            name_match = query in line["name"].lower() if query else False
            direction_match = (
                direction_query in line["direction"].lower()
                if direction_query
                else (query in line["direction"].lower() if query else False)
            )
            if code_match or name_match or direction_match:
                line_match = True
                break

        if stop_match or line_match:
            results.append(enriched)

    return {"items": results, "count": len(results)}


@app.get("/api/lines")
def get_lines(q: str = Query(default=""), direction: str = Query(default="")):
    query = q.strip().lower()
    direction_query = direction.strip().lower()

    items = []
    for line in LINES:
        code_match = query in line["code"].lower() if query else True
        name_match = query in line["name"].lower() if query else True
        direction_match = (
            direction_query in line["direction"].lower()
            if direction_query
            else True
        )

        if query and not (code_match or name_match or query in line["direction"].lower()):
            continue
        if not direction_match:
            continue

        items.append(line)

    return {"items": items, "count": len(items)}


@app.get("/api/search")
def search(q: str = Query(default=""), direction: str = Query(default="")):
    return {
        "stops": get_stops(q=q, direction=direction)["items"],
        "lines": get_lines(q=q, direction=direction)["items"],
    }
