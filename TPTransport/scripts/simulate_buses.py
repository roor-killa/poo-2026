#!/usr/bin/env python3
"""
Simulate bus movement along RTM Centre routes.

Creates one bus per selected route, then drives each bus along its stop
sequence at realistic speed, posting a GPS position to the API every 5 s
(matching the real embedded client behaviour).

Usage:
    python scripts/simulate_buses.py                   # 5 random buses
    python scripts/simulate_buses.py --num-buses 10    # 10 buses
    python scripts/simulate_buses.py --speed 35        # faster (km/h)
    python scripts/simulate_buses.py --keep            # don't delete on exit
    python scripts/simulate_buses.py --cleanup         # remove SIM-* buses and exit

Press Ctrl+C to stop; simulated buses are deleted automatically on exit
(unless --keep is set).
"""

import argparse
import asyncio
import json
import math
import random
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Config defaults
# ---------------------------------------------------------------------------

DEFAULT_API   = "http://127.0.0.1:8080"
TICK_S        = 5     # seconds between position posts (mirrors real client)
BUS_CODE_PFX  = "SIM"

_api_base = DEFAULT_API  # set from args in main()

# ---------------------------------------------------------------------------
# HTTP helpers (sync, run in thread pool via asyncio.to_thread)
# ---------------------------------------------------------------------------

def _post(path: str, body: dict, headers: dict | None = None) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{_api_base}{path}", data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_body": e.read().decode(errors="replace")[:300]}
    except Exception as e:
        return {"_err": str(e)}


def _get(path: str) -> list | dict:
    with urllib.request.urlopen(f"{_api_base}{path}", timeout=10) as r:
        return json.loads(r.read())


def _delete(path: str) -> int:
    req = urllib.request.Request(f"{_api_base}{path}", method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code

# ---------------------------------------------------------------------------
# Geo helpers
# ---------------------------------------------------------------------------

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a  = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x  = math.sin(dl) * math.cos(lat2)
    y  = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

# ---------------------------------------------------------------------------
# Simulated bus state
# ---------------------------------------------------------------------------

@dataclass
class SimBus:
    code:      str
    bus_id:    str
    token:     str
    stops:     list   # [{lat, lon, name}], ordered by stop_order
    stop_idx:  int   = 0    # current segment start
    fraction:  float = 0.0  # 0..1 progress within current segment
    direction: int   = 1    # +1 forward, -1 reverse (ping-pong at endpoints)

# ---------------------------------------------------------------------------
# Per-bus coroutine
# ---------------------------------------------------------------------------

async def _drive(bus: SimBus, speed_kmh: float) -> None:
    stops = bus.stops
    if len(stops) < 2:
        print(f"  [{bus.code}] Only {len(stops)} stop(s) — skipping")
        return

    speed_ms = speed_kmh * 1000 / 3600  # m/s

    # Spread buses evenly across the tick window so they don't all POST at once
    await asyncio.sleep(random.uniform(0, TICK_S))

    while True:
        # ── Current segment ──────────────────────────────────────────────
        i0  = bus.stop_idx
        i1  = max(0, min(len(stops) - 1, i0 + bus.direction))
        s0, s1 = stops[i0], stops[i1]
        seg_m   = max(1.0, _haversine_m(s0["lat"], s0["lon"], s1["lat"], s1["lon"]))

        lat = _lerp(s0["lat"], s1["lat"], bus.fraction)
        lon = _lerp(s0["lon"], s1["lon"], bus.fraction)
        hdg = _bearing(s0["lat"], s0["lon"], s1["lat"], s1["lon"])
        spd = max(0.0, speed_kmh + random.uniform(-4, 4))

        # ── POST position ─────────────────────────────────────────────────
        resp = await asyncio.to_thread(
            _post,
            "/api/v1/positions",
            {
                "latitude":    round(lat, 7),
                "longitude":   round(lon, 7),
                "speed_kmh":   round(spd, 1),
                "heading":     round(hdg, 1),
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
            {"Authorization": f"Bearer {bus.token}"},
        )
        if "_err" in resp:
            print(f"  [{bus.code}] POST error: {resp['_err']}")

        # ── Advance along route (ping-pong at endpoints) ──────────────────
        bus.fraction += (speed_ms * TICK_S) / seg_m

        while bus.fraction >= 1.0:
            bus.fraction -= 1.0
            bus.stop_idx += bus.direction

            if bus.stop_idx >= len(stops) - 1:
                bus.stop_idx = len(stops) - 1
                bus.direction = -1
            elif bus.stop_idx <= 0:
                bus.stop_idx = 0
                bus.direction = 1

            # Recalculate segment length for the new segment
            i0 = bus.stop_idx
            i1 = max(0, min(len(stops) - 1, i0 + bus.direction))
            s0, s1 = stops[i0], stops[i1]
            seg_m = max(1.0, _haversine_m(s0["lat"], s0["lon"], s1["lat"], s1["lon"]))

        await asyncio.sleep(TICK_S)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main() -> None:
    global _api_base

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api",       default=DEFAULT_API, help="API base URL (default: %(default)s)")
    parser.add_argument("--num-buses", type=int, default=5, metavar="N", help="Number of buses to simulate (default: %(default)s)")
    parser.add_argument("--speed",     type=float, default=25, metavar="KMH", help="Average speed in km/h (default: %(default)s)")
    parser.add_argument("--keep",      action="store_true", help="Keep simulated buses in DB after exit")
    parser.add_argument("--cleanup",   action="store_true", help=f"Delete all {BUS_CODE_PFX}-* buses and exit")
    args = parser.parse_args()

    _api_base = args.api.rstrip("/")

    # ── Cleanup mode ──────────────────────────────────────────────────────
    if args.cleanup:
        print(f"Fetching buses to clean up...")
        buses = await asyncio.to_thread(_get, "/api/v1/admin/buses")
        deleted = 0
        for b in buses:
            if b["code"].startswith(f"{BUS_CODE_PFX}-"):
                code = await asyncio.to_thread(_delete, f"/api/v1/admin/buses/{b['id']}")
                print(f"  Deleted {b['code']} (HTTP {code})")
                deleted += 1
        print(f"Cleaned up {deleted} bus(es).")
        return

    # ── Load routes ───────────────────────────────────────────────────────
    print("Loading routes from API...")
    try:
        routes = await asyncio.to_thread(_get, "/api/v1/admin/routes")
    except Exception as e:
        sys.exit(f"ERROR: Could not reach API at {_api_base} — {e}\nIs the app running?")

    routes = [
        r for r in routes
        if r.get("is_active") and r.get("route_stops") and len(r["route_stops"]) >= 2
    ]
    if not routes:
        sys.exit("No active routes with stops found. Run import_gtfs.py first.")

    num = min(args.num_buses, len(routes))
    chosen = random.sample(routes, num)
    print(f"  {len(routes)} routes available — simulating {num}")

    # ── Delete any pre-existing SIM buses (stale from a previous run) ─────
    print("Cleaning up stale simulated buses...")
    existing = await asyncio.to_thread(_get, "/api/v1/admin/buses")
    stale    = [b for b in existing if b["code"].startswith(f"{BUS_CODE_PFX}-")]
    for b in stale:
        await asyncio.to_thread(_delete, f"/api/v1/admin/buses/{b['id']}")
    if stale:
        print(f"  Removed {len(stale)} stale bus(es)")

    # ── Create buses ──────────────────────────────────────────────────────
    print(f"\nCreating {num} simulated bus(es)...")
    sim_buses: list[SimBus] = []

    for r in chosen:
        stops = [
            {"lat": rs["stop"]["lat"], "lon": rs["stop"]["lon"], "name": rs["stop"]["name"]}
            for rs in sorted(r["route_stops"], key=lambda x: x["stop_order"])
        ]
        code = f"{BUS_CODE_PFX}-{r['name']}"
        resp = await asyncio.to_thread(_post, "/api/v1/admin/buses", {
            "code":     code,
            "label":    f"Simulation — {r.get('description') or r['name']}",
            "route_id": r["id"],
        })
        if "_err" in resp:
            print(f"  WARN {code}: {resp['_err']} — {resp.get('_body','')}")
            continue

        # Scatter buses randomly along their routes
        start_idx  = random.randint(0, max(0, len(stops) - 2))
        start_frac = random.random()

        sim_buses.append(SimBus(
            code=resp["code"], bus_id=resp["id"], token=resp["api_token"],
            stops=stops, stop_idx=start_idx, fraction=start_frac,
        ))
        print(f"  + {resp['code']:<14}  Ligne {r['name']:<6}  {len(stops):3d} arrêts  token={resp['api_token'][:8]}…")

    if not sim_buses:
        sys.exit("No simulated buses created.")

    # ── Run ───────────────────────────────────────────────────────────────
    print(f"\n{len(sim_buses)} bus(es) running at ~{args.speed} km/h — Ctrl+C to stop\n")
    tasks = [asyncio.create_task(_drive(b, args.speed)) for b in sim_buses]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        if not args.keep:
            print("\nDeleting simulated buses...")
            for b in sim_buses:
                status = await asyncio.to_thread(_delete, f"/api/v1/admin/buses/{b.bus_id}")
                print(f"  Deleted {b.code} (HTTP {status})")
        else:
            print(f"\nBuses kept in DB (run with --cleanup to remove them later)")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
