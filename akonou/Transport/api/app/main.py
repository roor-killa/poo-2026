from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import Any

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import SessionLocal, init_db
from .models import AIQueryRequest, AIQueryResponse, AlertCreate, KPIResponse, PositionGPS
from .repository import count_open_alerts, persist_alert, seed_reference_data
from .services import bus_position_payload, compute_eta_for_stop, compute_kpis, handle_ai_query
from .store import store


class LiveConnectionManager:
    def __init__(self) -> None:
        self._line_connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, line_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._line_connections[line_id].add(websocket)

    def disconnect(self, line_id: str, websocket: WebSocket) -> None:
        if line_id in self._line_connections:
            self._line_connections[line_id].discard(websocket)
            if not self._line_connections[line_id]:
                del self._line_connections[line_id]

    async def broadcast_line_update(self, line_id: str, payload: dict[str, Any]) -> None:
        sockets = list(self._line_connections.get(line_id, set()))
        for ws in sockets:
            try:
                await ws.send_json(payload)
            except Exception:
                self.disconnect(line_id, ws)


app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
live_manager = LiveConnectionManager()


@app.on_event("startup")
async def startup_event() -> None:
    init_db()
    db = SessionLocal()
    try:
        seed_reference_data(db)
    finally:
        db.close()
    asyncio.create_task(_simulate_positions())


async def _simulate_positions() -> None:
    """Déplace les bus simulés d'un waypoint toutes les 4 secondes et broadcast."""
    while True:
        await asyncio.sleep(4)
        updates = store.advance_simulation()
        for line_id, position in updates:
            if line_id:
                await live_manager.broadcast_line_update(line_id, bus_position_payload(position))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get(f"{settings.api_prefix}/buses")
async def list_buses() -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for bus in store.buses.values():
        position = store.positions.get(bus.id)
        payload.append(
            {
                **bus.model_dump(),
                "last_position": position.model_dump() if position else None,
            }
        )
    return payload


@app.get(f"{settings.api_prefix}/buses/{{bus_id}}/position")
async def get_bus_position(bus_id: str) -> dict[str, Any]:
    position = store.positions.get(bus_id)
    if position is None:
        raise HTTPException(status_code=404, detail="Position not found for this bus")
    return position.model_dump()


@app.get(f"{settings.api_prefix}/lines")
async def list_lines() -> list[dict[str, Any]]:
    return store.serialize_lines()


@app.get(f"{settings.api_prefix}/stops/{{stop_id}}/arrivals")
async def stop_arrivals(stop_id: str) -> list[dict[str, Any]]:
    if stop_id not in store.stops:
        raise HTTPException(status_code=404, detail="Stop not found")
    return [item.model_dump() for item in compute_eta_for_stop(stop_id)]


@app.post(f"{settings.api_prefix}/alerts")
async def create_alert(payload: AlertCreate) -> dict[str, Any]:
    if payload.bus_id not in store.buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    alert = store.add_alert(payload.type, payload.bus_id, payload.message)

    db = SessionLocal()
    try:
        persist_alert(db, alert)
    finally:
        db.close()

    return alert.model_dump()


@app.get(f"{settings.api_prefix}/analytics/kpi", response_model=KPIResponse)
async def analytics_kpi() -> KPIResponse:
    kpi = compute_kpis()

    db = SessionLocal()
    try:
        kpi.open_alerts = count_open_alerts(db)
    finally:
        db.close()

    return kpi


@app.post(f"{settings.api_prefix}/ai/query", response_model=AIQueryResponse)
async def ai_query(payload: AIQueryRequest) -> AIQueryResponse:
    result = handle_ai_query(payload.query)
    return AIQueryResponse(**result)


@app.websocket("/ws/live/{line_id}")
async def ws_live(line_id: str, websocket: WebSocket) -> None:
    await live_manager.connect(line_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        live_manager.disconnect(line_id, websocket)


@app.websocket("/ws/agent/{bus_id}")
async def ws_agent(
    bus_id: str,
    websocket: WebSocket,
    token: str = Query(default=""),
) -> None:
    if token != settings.agent_token:
        await websocket.close(code=4401)
        return

    if bus_id not in store.buses:
        await websocket.close(code=4404)
        return

    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()
            payload = json.loads(raw)
            payload["bus_id"] = bus_id
            position = PositionGPS(**payload)
            store.upsert_position(position)

            bus_payload = bus_position_payload(position)
            line_id = store.buses[bus_id].line_id
            if line_id:
                await live_manager.broadcast_line_update(line_id, bus_payload)

            await websocket.send_json({"ok": True, "received": bus_payload})
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await websocket.send_json({"ok": False, "error": str(exc)})
