import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from simulation.engine import simulateur
import logging

router = APIRouter(tags=["WebSocket"])
logger = logging.getLogger(__name__)


@router.websocket("/ws/positions")
async def websocket_positions(websocket: WebSocket):
    """
    WebSocket — diffuse les positions GPS de tous les bus toutes les N secondes.
    Le client reçoit automatiquement les mises à jour sans avoir à les demander.
    """
    await websocket.accept()
    simulateur.connecter_client(websocket)

    # Envoyer les positions initiales immédiatement à la connexion
    try:
        payload = json.dumps(simulateur.get_toutes_positions())
        await websocket.send_text(payload)

        # Maintenir la connexion ouverte (le simulateur se charge des broadcasts)
        while True:
            # On attend les messages du client (ping/pong ou filtres futurs)
            data = await websocket.receive_text()
            # Pour l'instant on ignore les messages entrants (extensible V2)
            logger.debug(f"[WS] Message reçu : {data}")

    except WebSocketDisconnect:
        logger.info("[WS] Déconnexion propre.")
    except Exception as e:
        logger.error(f"[WS] Erreur : {e}")
    finally:
        simulateur.deconnecter_client(websocket)
