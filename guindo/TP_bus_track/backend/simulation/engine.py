import asyncio
import json
import logging
from typing import Dict, List
from models.bus import Bus
from models.ligne import Ligne
from models.arret import Arret
from core.config import settings

logger = logging.getLogger(__name__)


# ── Données des lignes Martinique (simulées) ──────────────────────────────────
LIGNES_DATA = [
    {
        "id": 1,
        "nom": "Ligne 1 — Fort-de-France → Le Lamentin",
        "couleur": "#E74C3C",
        "description": "Ligne principale reliant le centre-ville au Lamentin via la N1",
        "arrets": [
            {"id": 1,  "nom": "Fort-de-France — La Savane",     "latitude": 14.6019, "longitude": -61.0608, "ordre": 0},
            {"id": 2,  "nom": "Terreville",                     "latitude": 14.5985, "longitude": -61.0490, "ordre": 1},
            {"id": 3,  "nom": "Mangot-Vulcin",                  "latitude": 14.5963, "longitude": -61.0310, "ordre": 2},
            {"id": 4,  "nom": "Acajou",                         "latitude": 14.5950, "longitude": -61.0100, "ordre": 3},
            {"id": 5,  "nom": "Le Lamentin — Centre",           "latitude": 14.5973, "longitude": -60.9941, "ordre": 4},
        ],
    },
    {
        "id": 2,
        "nom": "Ligne 2 — Fort-de-France → Schoelcher",
        "couleur": "#2ECC71",
        "description": "Liaison Fort-de-France / Schoelcher via le littoral nord",
        "arrets": [
            {"id": 8,  "nom": "Fort-de-France — Pointe Simon",  "latitude": 14.6037, "longitude": -61.0631, "ordre": 0},
            {"id": 9,  "nom": "Fort-de-France — Bord de Mer",   "latitude": 14.6058, "longitude": -61.0659, "ordre": 1},
            {"id": 10, "nom": "Plateau Fofo",                   "latitude": 14.6121, "longitude": -61.0712, "ordre": 2},
            {"id": 11, "nom": "Fond Lahaye",                    "latitude": 14.6198, "longitude": -61.0768, "ordre": 3},
            {"id": 12, "nom": "Schoelcher — Mairie",            "latitude": 14.6254, "longitude": -61.0831, "ordre": 4},
        ],
    },
    {
        "id": 3,
        "nom": "Ligne 3 — Fort-de-France → Le François",
        "couleur": "#3498DB",
        "description": "Liaison transversale vers la côte atlantique via N1",
        "arrets": [
            {"id": 13, "nom": "Fort-de-France — La Savane",    "latitude": 14.6019, "longitude": -61.0608, "ordre": 0},
            {"id": 14, "nom": "Le Lamentin — Centre",          "latitude": 14.5973, "longitude": -60.9941, "ordre": 1},
            {"id": 15, "nom": "Le Gros-Morne",                 "latitude": 14.6440, "longitude": -60.9620, "ordre": 2},
            {"id": 16, "nom": "Le Robert — Bourg",             "latitude": 14.6812, "longitude": -60.9312, "ordre": 3},
            {"id": 17, "nom": "Le François — Centre",          "latitude": 14.6218, "longitude": -60.8983, "ordre": 4},
        ],
    },
]


class SimulateurGPS:
    """
    Moteur de simulation GPS — tourne en tâche de fond (BackgroundTask).
    Maintient l'état de tous les bus en mémoire et notifie les clients WebSocket.
    """

    def __init__(self):
        self.lignes: Dict[int, Ligne] = {}
        self.bus: Dict[int, Bus] = {}
        self.ws_clients: List = []  # liste des WebSocket connectés
        self._running = False
        self._initialiser_lignes()
        self._initialiser_bus()

    def _initialiser_lignes(self) -> None:
        for data in LIGNES_DATA:
            arrets = [Arret(**a) for a in data["arrets"]]
            ligne = Ligne(
                id=data["id"],
                nom=data["nom"],
                couleur=data["couleur"],
                description=data["description"],
                arrets=arrets,
            )
            self.lignes[ligne.id] = ligne
        logger.info(f"[Simulation] {len(self.lignes)} lignes initialisées.")

    def _initialiser_bus(self) -> None:
        bus_id = 1
        for ligne in self.lignes.values():
            # 2 bus par ligne, démarrant à des positions différentes
            for i, depart_idx in enumerate([0, len(ligne.arrets) // 2]):
                arret_depart = ligne.arrets[depart_idx]
                bus = Bus(
                    id=bus_id,
                    nom=f"Bus {ligne.id}-{'A' if i == 0 else 'B'}",
                    ligne=ligne,
                    latitude=arret_depart.latitude,
                    longitude=arret_depart.longitude,
                    arret_courant_idx=depart_idx,
                    direction=1 if i == 0 else -1,
                )
                self.bus[bus.id] = bus
                bus_id += 1
        logger.info(f"[Simulation] {len(self.bus)} bus initialisés.")

    def get_toutes_positions(self) -> List[dict]:
        return [b.to_dict() for b in self.bus.values()]

    def get_bus_par_ligne(self, ligne_id: int) -> List[dict]:
        return [b.to_dict() for b in self.bus.values() if b.ligne.id == ligne_id]

    def connecter_client(self, websocket) -> None:
        self.ws_clients.append(websocket)
        logger.info(f"[WS] Client connecté. Total: {len(self.ws_clients)}")

    def deconnecter_client(self, websocket) -> None:
        self.ws_clients = [c for c in self.ws_clients if c != websocket]
        logger.info(f"[WS] Client déconnecté. Total: {len(self.ws_clients)}")

    async def _diffuser_positions(self) -> None:
        """Envoie les positions à tous les clients WebSocket connectés."""
        if not self.ws_clients:
            return
        payload = json.dumps(self.get_toutes_positions())
        clients_a_supprimer = []
        for ws in self.ws_clients:
            try:
                await ws.send_text(payload)
            except Exception:
                clients_a_supprimer.append(ws)
        for ws in clients_a_supprimer:
            self.deconnecter_client(ws)

    async def demarrer(self) -> None:
        """Boucle principale de simulation — appelée en BackgroundTask."""
        self._running = True
        interval = settings.SIMULATION_INTERVAL
        logger.info(f"[Simulation] Démarrage — intervalle {interval}s.")
        while self._running:
            for bus in self.bus.values():
                bus.avancer(delta_secondes=float(interval))
            await self._diffuser_positions()
            await asyncio.sleep(interval)

    def arreter(self) -> None:
        self._running = False
        logger.info("[Simulation] Arrêt du moteur.")


# Instance globale partagée
simulateur = SimulateurGPS()
