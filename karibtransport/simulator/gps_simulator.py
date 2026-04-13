"""
GPS Simulator — KaribTransport
Simulates vehicles moving along simple routes and pushes GPS updates
to the backend API via PATCH /vehicles/{id}/gps.
"""

import time
import math
import random
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

# ── Route definition ──────────────────────────────────────────────────────────
# Each route is a list of (lat, lon) waypoints.
# Vehicles loop through their route indefinitely.

ROUTES = {
    "route_1": [
        (14.6037, -61.0724),  # Fort-de-France centre
        (14.6100, -61.0800),
        (14.6200, -61.0850),
        (14.6280, -61.0900),  # Schœlcher
    ],
    "route_2": [
        (14.5500, -60.9900),  # Le Lamentin
        (14.5600, -61.0100),
        (14.5800, -61.0400),
        (14.6037, -61.0724),  # Fort-de-France centre
    ],
}


class VehicleSimulator:
    def __init__(self, vehicle_id: int, route: list[tuple[float, float]], speed_kmh: float = 40.0):
        self.vehicle_id = vehicle_id
        self.route = route
        self.speed_kmh = speed_kmh
        self.waypoint_index = 0
        self.lat, self.lon = route[0]

    def _bearing(self, lat1, lon1, lat2, lon2) -> float:
        """Return compass bearing from point 1 to point 2 (degrees)."""
        d_lon = math.radians(lon2 - lon1)
        lat1, lat2 = math.radians(lat1), math.radians(lat2)
        x = math.sin(d_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
        bearing = math.degrees(math.atan2(x, y))
        return (bearing + 360) % 360

    def step(self, delta_seconds: float = 5.0):
        """Advance position toward next waypoint by one time step."""
        target_lat, target_lon = self.route[self.waypoint_index]
        bearing = self._bearing(self.lat, self.lon, target_lat, target_lon)

        # Distance covered in delta_seconds (degrees ≈ km / 111)
        distance_km = self.speed_kmh * (delta_seconds / 3600)
        distance_deg = distance_km / 111.0

        d_lat = target_lat - self.lat
        d_lon = target_lon - self.lon
        dist_to_wp = math.hypot(d_lat, d_lon)

        if dist_to_wp <= distance_deg:
            # Reached waypoint — advance to next
            self.lat, self.lon = target_lat, target_lon
            self.waypoint_index = (self.waypoint_index + 1) % len(self.route)
        else:
            ratio = distance_deg / dist_to_wp
            self.lat += d_lat * ratio
            self.lon += d_lon * ratio

        # Add a small jitter to mimic GPS noise
        self.lat += random.gauss(0, 0.00005)
        self.lon += random.gauss(0, 0.00005)

        return {
            "latitude": round(self.lat, 6),
            "longitude": round(self.lon, 6),
            "speed": round(self.speed_kmh + random.gauss(0, 2), 1),
            "heading": round(bearing, 1),
        }

    def push(self, delta_seconds: float = 5.0):
        payload = self.step(delta_seconds)
        url = f"{API_BASE}/vehicles/{self.vehicle_id}/gps"
        try:
            resp = requests.patch(url, json=payload, timeout=3)
            resp.raise_for_status()
            print(f"[vehicle {self.vehicle_id}] GPS updated → {payload}")
        except requests.RequestException as exc:
            print(f"[vehicle {self.vehicle_id}] ERROR: {exc}")


def seed_vehicles() -> list[int]:
    """Create demo vehicles if they don't exist yet. Returns list of IDs."""
    demos = [
        {"license_plate": "MA-001-TX", "vehicle_type": "minibus", "capacity": 15},
        {"license_plate": "MA-002-TX", "vehicle_type": "bus", "capacity": 40},
    ]
    ids = []
    for data in demos:
        try:
            r = requests.post(f"{API_BASE}/vehicles/", json=data, timeout=3)
            if r.status_code in (200, 201):
                ids.append(r.json()["id"])
                print(f"Created vehicle: {data['license_plate']} (id={ids[-1]})")
            elif r.status_code == 409:
                # Already exists — fetch by listing
                all_v = requests.get(f"{API_BASE}/vehicles/", timeout=3).json()
                match = next((v for v in all_v if v["license_plate"] == data["license_plate"]), None)
                if match:
                    ids.append(match["id"])
                    print(f"Vehicle already exists: {data['license_plate']} (id={match['id']})")
        except requests.RequestException as exc:
            print(f"Could not create vehicle {data['license_plate']}: {exc}")
    return ids


def main():
    print(f"Connecting to API at {API_BASE} …")
    # Wait for the API to be ready
    for attempt in range(10):
        try:
            requests.get(f"{API_BASE}/health", timeout=2).raise_for_status()
            print("API is up.")
            break
        except requests.RequestException:
            print(f"Waiting for API… attempt {attempt + 1}/10")
            time.sleep(3)
    else:
        print("Could not reach API. Exiting.")
        return

    ids = seed_vehicles()
    if len(ids) < 2:
        print("Not enough vehicles registered. Exiting.")
        return

    route_keys = list(ROUTES.keys())
    simulators = [
        VehicleSimulator(ids[0], ROUTES[route_keys[0]], speed_kmh=35),
        VehicleSimulator(ids[1], ROUTES[route_keys[1]], speed_kmh=45),
    ]

    interval = 5.0  # seconds between GPS pushes
    print(f"Simulator running — pushing GPS every {interval}s. Ctrl+C to stop.")
    try:
        while True:
            for sim in simulators:
                sim.push(delta_seconds=interval)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Simulator stopped.")


if __name__ == "__main__":
    main()
