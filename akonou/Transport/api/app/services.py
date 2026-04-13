from __future__ import annotations

import math
from typing import Any

from .config import settings
from .models import ETAItem, KPIResponse, PositionGPS
from .store import store


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def compute_eta_for_stop(stop_id: str) -> list[ETAItem]:
    stop = store.stops.get(stop_id)
    if stop is None:
        return []

    candidates: list[ETAItem] = []
    for bus in store.buses.values():
        if bus.line_id != stop.line_id:
            continue

        position = store.positions.get(bus.id)
        if position is None:
            continue

        distance_km = haversine_km(position.lat, position.lng, stop.latitude, stop.longitude)
        kmh = position.speed if position.speed > 0 else settings.eta_default_kmh
        eta_minutes = max(1, int((distance_km / max(kmh, 1)) * 60))

        candidates.append(
            ETAItem(
                bus_id=bus.id,
                stop_id=stop_id,
                eta_minutes=eta_minutes,
                distance_km=round(distance_km, 2),
            )
        )

    return sorted(candidates, key=lambda item: item.eta_minutes)


def compute_kpis() -> KPIResponse:
    total = len(store.buses)
    active = sum(1 for bus in store.buses.values() if bus.statut == "in_service")
    ratio = (active / total) if total else 0
    return KPIResponse(
        active_buses=active,
        total_buses=total,
        open_alerts=store.open_alerts_count(),
        coverage_ratio=round(ratio, 3),
    )


def handle_ai_query(query: str) -> dict[str, Any]:
    lowered = query.lower().strip()
    kpis = compute_kpis().model_dump()

    if "retard" in lowered:
        answer = "MVP IA: detection de retard activee. Utilisez /api/v1/analytics/kpi pour plus de details."
    elif "ligne" in lowered:
        answer = "MVP IA: je peux analyser les lignes actives et la couverture en cours."
    elif "incident" in lowered or "alerte" in lowered:
        answer = "MVP IA: je vois les alertes ouvertes."
    else:
        answer = "MVP IA: endpoint pret. Branchez Claude API pour des reponses enrichies."

    return {
        "answer": answer,
        "data_points": {
            "kpis": kpis,
            "known_lines": [line.model_dump() for line in store.lines.values()],
            "last_positions_count": len(store.positions),
        },
    }


def bus_position_payload(position: PositionGPS) -> dict[str, Any]:
    bus = store.buses.get(position.bus_id)
    return {
        "bus_id": position.bus_id,
        "line_id": bus.line_id if bus else None,
        "lat": position.lat,
        "lng": position.lng,
        "speed": position.speed,
        "heading": position.heading,
        "ts": position.ts,
    }
