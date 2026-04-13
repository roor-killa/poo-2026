from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ── Arrêt ─────────────────────────────────────────────────────────────────────
class ArretBase(BaseModel):
    nom: str
    latitude: float
    longitude: float
    ordre: int

class ArretRead(ArretBase):
    id: int
    ligne_id: int
    model_config = {"from_attributes": True}


# ── Ligne ─────────────────────────────────────────────────────────────────────
class LigneBase(BaseModel):
    nom: str
    couleur: str = "#2E75B6"
    description: Optional[str] = None

class LigneRead(LigneBase):
    id: int
    actif: bool
    arrets: List[ArretRead] = []
    model_config = {"from_attributes": True}


# ── Bus ───────────────────────────────────────────────────────────────────────
class BusPosition(BaseModel):
    id: int
    nom: str
    ligne_id: int
    ligne_nom: str
    ligne_couleur: str
    latitude: float
    longitude: float
    vitesse: float
    statut: str
    arret_courant: Optional[str]
    prochain_arret: Optional[str]


# ── WebSocket ─────────────────────────────────────────────────────────────────
class WSMessage(BaseModel):
    type: str = "positions"
    data: List[BusPosition]


# ── Push Subscription ─────────────────────────────────────────────────────────
class PushSubscriptionCreate(BaseModel):
    endpoint: str
    p256dh: str
    auth: str

class PushSubscriptionRead(PushSubscriptionCreate):
    id: int
    model_config = {"from_attributes": True}


# ── Health ────────────────────────────────────────────────────────────────────
class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    bus_actifs: int
    clients_ws: int
