#!/usr/bin/env python3
"""
Import GTFS Centre RTM data into the bus tracking system.

Usage (API must be running):
    python scripts/import_gtfs.py
    python scripts/import_gtfs.py --api http://localhost:8000 --gtfs ./gtfs-centre-rtm

For each GTFS route the script picks the direction-0 trip with the most stops
as the canonical stop sequence, then computes haversine distances between
consecutive stops.
"""

import argparse
import csv
import json
import math
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def api_post(base: str, path: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{base}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return {"_error": exc.code, "_body": exc.read().decode(errors="replace")}


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def progress(current: int, total: int, label: str) -> None:
    if current % 100 == 0 or current == total:
        pct = current * 100 // total
        print(f"  [{pct:3d}%] {current}/{total} {label}", flush=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api",  default="http://127.0.0.1:8080", help="Base URL of the running API")
    parser.add_argument("--gtfs", default="./gtfs-centre-rtm",    help="Path to the GTFS directory")
    args = parser.parse_args()

    api  = args.api.rstrip("/")
    gtfs = args.gtfs

    for fname in ("stops.txt", "routes.txt", "trips.txt", "stop_times.txt"):
        if not os.path.exists(os.path.join(gtfs, fname)):
            sys.exit(f"ERROR: {os.path.join(gtfs, fname)} not found")

    # ── Step 1: Import stops ─────────────────────────────────────────────────
    print("\n=== Step 1/3: Importing stops ===")
    raw_stops = read_csv(os.path.join(gtfs, "stops.txt"))

    # Only physical stops (location_type 0 or blank); skip parent stations (1)
    stops_to_import = [
        s for s in raw_stops
        if (s.get("location_type") or "0") == "0"
    ]
    skipped = len(raw_stops) - len(stops_to_import)
    print(f"  {len(stops_to_import)} physical stops to create ({skipped} parent stations skipped)")

    gtfs_to_uuid: dict[str, str] = {}   # GTFS stop_id  → API UUID
    stop_coords:  dict[str, tuple]  = {}   # API UUID      → (lat, lon)
    stop_errors = 0

    for i, s in enumerate(stops_to_import, 1):
        resp = api_post(api, "/api/v1/admin/stops", {
            "name": s["stop_name"].strip()[:120],
            "lat":  float(s["stop_lat"]),
            "lon":  float(s["stop_lon"]),
        })
        if "_error" in resp:
            print(f"  WARN stop {s['stop_id']} ({s['stop_name']}): HTTP {resp['_error']}")
            stop_errors += 1
        else:
            gtfs_to_uuid[s["stop_id"]] = resp["id"]
            stop_coords[resp["id"]] = (float(s["stop_lat"]), float(s["stop_lon"]))
        progress(i, len(stops_to_import), "stops")

    print(f"  Result: {len(gtfs_to_uuid)} created, {stop_errors} failed")

    # ── Step 2: Index stop_times by trip ─────────────────────────────────────
    print("\n=== Step 2/3: Indexing stop_times ===")
    trip_stops: dict[str, list] = defaultdict(list)   # trip_id → [(seq, stop_id)]

    raw_stop_times = read_csv(os.path.join(gtfs, "stop_times.txt"))
    for row in raw_stop_times:
        trip_stops[row["trip_id"]].append((int(row["stop_sequence"]), row["stop_id"]))

    for tid in trip_stops:
        trip_stops[tid].sort()

    print(f"  {len(trip_stops)} trips indexed from {len(raw_stop_times)} stop_time rows")

    # ── Step 3: Import routes ────────────────────────────────────────────────
    print("\n=== Step 3/3: Importing routes ===")
    routes_raw = read_csv(os.path.join(gtfs, "routes.txt"))
    trips_raw  = read_csv(os.path.join(gtfs, "trips.txt"))

    # Group trips by route_id
    route_trips: dict[str, list] = defaultdict(list)
    for t in trips_raw:
        route_trips[t["route_id"]].append(t)

    created_routes = 0
    route_errors   = 0

    for i, route in enumerate(routes_raw, 1):
        rid   = route["route_id"]
        trips = route_trips.get(rid, [])

        if not trips:
            print(f"  SKIP route {rid}: no trips found")
            continue

        # Prefer direction_id=0; pick the trip with the longest stop sequence
        dir0 = [t for t in trips if t.get("direction_id", "0") == "0"] or trips
        best = max(dir0, key=lambda t: len(trip_stops.get(t["trip_id"], [])))
        raw_seq = trip_stops.get(best["trip_id"], [])

        # Build stop sequence using only stops we successfully created
        stop_seq = []
        prev_lat = prev_lon = None
        for _, gtfs_sid in raw_seq:
            uuid = gtfs_to_uuid.get(gtfs_sid)
            if uuid is None:
                continue
            lat, lon = stop_coords[uuid]
            dist = round(haversine_m(prev_lat, prev_lon, lat, lon), 1) if prev_lat is not None else None
            stop_seq.append({
                "stop_id":              uuid,
                "stop_order":           len(stop_seq) + 1,
                "distance_from_prev_m": dist,
            })
            prev_lat, prev_lon = lat, lon

        short = (route.get("route_short_name") or "").strip()
        long_ = (route.get("route_long_name")  or "").strip()
        name  = (short or long_ or rid)[:120]
        desc  = long_ if long_ != name else None

        resp = api_post(api, "/api/v1/admin/routes", {
            "name":        name,
            "description": desc,
            "is_active":   True,
            "stops":       stop_seq,
        })

        if "_error" in resp:
            print(f"  WARN route {rid} ({name}): HTTP {resp['_error']} — {resp['_body'][:200]}")
            route_errors += 1
        else:
            print(f"  + [{i:2d}] Ligne {name:<6} — {long_:<55} {len(stop_seq):3d} stops")
            created_routes += 1

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"""
=== Import complete ===
  Stops  : {len(gtfs_to_uuid):4d} created  |  {stop_errors} failed
  Routes : {created_routes:4d} created  |  {route_errors} failed
""")


if __name__ == "__main__":
    main()
