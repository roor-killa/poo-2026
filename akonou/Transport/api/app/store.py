from __future__ import annotations

import threading
import time
from typing import Any

from .models import Alert, AlertStatus, Bus, BusStatus, Driver, Line, PositionGPS, Stop


class InMemoryStore:
    def __init__(self) -> None:
        self._lock = threading.RLock()

        self.buses: dict[str, Bus] = {}
        self.lines: dict[str, Line] = {}
        self.stops: dict[str, Stop] = {}
        self.drivers: dict[str, Driver] = {}
        self.positions: dict[str, PositionGPS] = {}
        self.alerts: dict[str, Alert] = {}
        self.position_history: list[PositionGPS] = []

        self._seed()

    def _seed(self) -> None:
        # ── Lignes réseau CFTU Martinique ─────────────────────────────────────
        line_1 = Line(
            id="LINE-001",
            numero="1",
            nom="Fort-de-France / Lamentin",
            couleur="#EF4444",
            direction_aller="Fort-de-France -> Lamentin",
            direction_retour="Lamentin -> Fort-de-France",
        )
        line_2 = Line(
            id="LINE-002",
            numero="2",
            nom="Fort-de-France / Schoelcher",
            couleur="#3B82F6",
            direction_aller="Fort-de-France -> Schoelcher",
            direction_retour="Schoelcher -> Fort-de-France",
        )

        self.lines[line_1.id] = line_1
        self.lines[line_2.id] = line_2

        # ── Arrêts avec coordonnées GPS réelles Martinique ────────────────────
        seeded_stops = [
            # Ligne 1 – axe Fort-de-France ↔ Lamentin
            Stop(id="STOP-001", nom="Pointe Simon",     latitude=14.6039, longitude=-61.0795, line_id="LINE-001"),
            Stop(id="STOP-002", nom="Cluny",            latitude=14.6078, longitude=-61.0583, line_id="LINE-001"),
            Stop(id="STOP-003", nom="ZAC Californie",   latitude=14.6082, longitude=-61.0368, line_id="LINE-001"),
            Stop(id="STOP-004", nom="Croix Rivail",     latitude=14.6085, longitude=-61.0128, line_id="LINE-001"),
            Stop(id="STOP-005", nom="Lamentin Centre",  latitude=14.6023, longitude=-60.9981, line_id="LINE-001"),
            # Ligne 2 – axe Fort-de-France ↔ Schoelcher
            Stop(id="STOP-006", nom="Pointe Simon",     latitude=14.6039, longitude=-61.0795, line_id="LINE-002"),
            Stop(id="STOP-007", nom="Dillon",           latitude=14.5987, longitude=-61.0908, line_id="LINE-002"),
            Stop(id="STOP-008", nom="Fond Lahaye",      latitude=14.6124, longitude=-61.0985, line_id="LINE-002"),
            Stop(id="STOP-009", nom="Gondeau",          latitude=14.6201, longitude=-61.1032, line_id="LINE-002"),
            Stop(id="STOP-010", nom="Schoelcher Centre",latitude=14.6239, longitude=-61.1048, line_id="LINE-002"),
        ]
        for stop in seeded_stops:
            self.stops[stop.id] = stop

        seeded_buses = [
            Bus(id="BUS-001", immatriculation="MAR-001", modele="Yutong ZK6125",      capacite=80, statut=BusStatus.in_service,     line_id="LINE-001", depot="Depot Pointe Simon"),
            Bus(id="BUS-002", immatriculation="MAR-002", modele="Yutong ZK6125",      capacite=80, statut=BusStatus.in_service,     line_id="LINE-001", depot="Depot Pointe Simon"),
            Bus(id="BUS-101", immatriculation="MAR-101", modele="King Long XMQ6127",  capacite=70, statut=BusStatus.in_service,     line_id="LINE-002", depot="Depot Pointe Simon"),
            Bus(id="BUS-102", immatriculation="MAR-102", modele="King Long XMQ6127",  capacite=70, statut=BusStatus.out_of_service, line_id="LINE-002", depot="Depot Pointe Simon"),
        ]
        for bus in seeded_buses:
            self.buses[bus.id] = bus

        seeded_drivers = [
            Driver(id="DRV-001", nom="Lerus",     prenom="Marcel",    telephone="+59661200001", bus_id="BUS-001"),
            Driver(id="DRV-002", nom="Beauville", prenom="Sandra",    telephone="+59661200002", bus_id="BUS-002"),
            Driver(id="DRV-003", nom="Cyrille",   prenom="Jean-Paul", telephone="+59661200003", bus_id="BUS-101"),
        ]
        for driver in seeded_drivers:
            self.drivers[driver.id] = driver

        # ── Waypoints de simulation (trajectoires interpolées entre arrêts) ──
        self._waypoints: dict[str, list[tuple[float, float]]] = {
            "BUS-001": [
                (14.6039, -61.0795), (14.6055, -61.0700), (14.6078, -61.0583),
                (14.6079, -61.0476), (14.6082, -61.0368), (14.6083, -61.0248),
                (14.6085, -61.0128), (14.6054, -61.0054), (14.6023, -60.9981),
            ],
            "BUS-002": [
                (14.6023, -60.9981), (14.6054, -61.0054), (14.6085, -61.0128),
                (14.6083, -61.0248), (14.6082, -61.0368), (14.6079, -61.0476),
                (14.6078, -61.0583), (14.6055, -61.0700), (14.6039, -61.0795),
            ],
            "BUS-101": [
                (14.6039, -61.0795), (14.6013, -61.0851), (14.5987, -61.0908),
                (14.6055, -61.0946), (14.6124, -61.0985), (14.6162, -61.1008),
                (14.6201, -61.1032), (14.6220, -61.1040), (14.6239, -61.1048),
            ],
        }
        self._wp_index: dict[str, int] = {"BUS-001": 1, "BUS-002": 4, "BUS-101": 3}

        # ── Positions initiales (visibles immédiatement sur la carte) ─────────
        ts = int(time.time())
        for bus_id, wps in self._waypoints.items():
            idx = self._wp_index[bus_id]
            lat, lng = wps[idx]
            self.positions[bus_id] = PositionGPS(
                bus_id=bus_id, lat=lat, lng=lng, speed=28, heading=90, ts=ts, sig="sim"
            )

    def advance_simulation(self) -> list[tuple[str, PositionGPS]]:
        """Avance chaque bus simulé d'un cran sur sa trajectoire (boucle)."""
        updated: list[tuple[str, PositionGPS]] = []
        ts = int(time.time())
        with self._lock:
            for bus_id, wps in self._waypoints.items():
                bus = self.buses.get(bus_id)
                if bus is None or bus.statut != BusStatus.in_service:
                    continue
                idx = (self._wp_index[bus_id] + 1) % len(wps)
                self._wp_index[bus_id] = idx
                lat, lng = wps[idx]
                pos = PositionGPS(
                    bus_id=bus_id, lat=lat, lng=lng, speed=28, heading=90, ts=ts, sig="sim"
                )
                self.positions[bus_id] = pos
                updated.append((bus.line_id or "", pos))
        return updated

    def upsert_position(self, position: PositionGPS) -> None:
        with self._lock:
            self.positions[position.bus_id] = position
            self.position_history.append(position)

    def add_alert(self, alert_type: str, bus_id: str, message: str) -> Alert:
        with self._lock:
            alert_id = f"ALT-{len(self.alerts) + 1:04d}"
            alert = Alert(
                id=alert_id,
                type=alert_type,
                bus_id=bus_id,
                message=message,
                timestamp=int(time.time()),
                statut=AlertStatus.open,
            )
            self.alerts[alert_id] = alert
            return alert

    def open_alerts_count(self) -> int:
        with self._lock:
            return sum(1 for alert in self.alerts.values() if alert.statut == AlertStatus.open)

    def serialize_lines(self) -> list[dict[str, Any]]:
        with self._lock:
            grouped_stops: dict[str, list[Stop]] = {}
            for stop in self.stops.values():
                grouped_stops.setdefault(stop.line_id, []).append(stop)

            payload: list[dict[str, Any]] = []
            for line in self.lines.values():
                payload.append(
                    {
                        **line.model_dump(),
                        "stops": [s.model_dump() for s in grouped_stops.get(line.id, [])],
                    }
                )
            return payload


store = InMemoryStore()
