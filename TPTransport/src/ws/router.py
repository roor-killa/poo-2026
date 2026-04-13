"""WebSocket endpoint definitions (spec §4).

Public channel:  ws://host/ws/buses
Admin channel:   ws://localhost:8080/ws/admin  (localhost guard)
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.api.deps import require_localhost
from src.ws.broadcaster import Broadcaster, get_broadcaster

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/buses")
async def ws_buses(
    websocket: WebSocket,
    broadcaster: Broadcaster = Depends(get_broadcaster),
) -> None:
    """Public real-time bus feed — snapshot every 5 s, bus_offline events."""
    await broadcaster.connect_public(websocket)
    try:
        # Keep the connection alive; we don't expect client → server messages
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await broadcaster.disconnect_public(websocket)


@router.websocket("/ws/admin")
async def ws_admin(websocket: WebSocket) -> None:
    """Admin real-time feed — same as public + token_masked, is_active, counts.

    Enforces localhost restriction before accepting the handshake.
    """
    # Manual localhost guard — require_localhost raises HTTPException which
    # FastAPI converts to a 403 before the WS handshake completes.
    require_localhost(websocket)  # type: ignore[arg-type]  Request ≈ WebSocket here

    broadcaster = get_broadcaster()
    await broadcaster.connect_admin(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await broadcaster.disconnect_admin(websocket)
