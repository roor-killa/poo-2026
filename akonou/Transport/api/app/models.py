from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BusStatus(str, Enum):
    in_service = "in_service"
    out_of_service = "out_of_service"
    incident = "incident"


class AlertStatus(str, Enum):
    open = "open"
    closed = "closed"


class Role(str, Enum):
    admin = "admin"
    operator = "operator"
    reader = "reader"


class Bus(BaseModel):
    id: str
    immatriculation: str
    modele: str
    capacite: int
    statut: BusStatus
    line_id: str | None = None
    depot: str | None = None


class Line(BaseModel):
    id: str
    numero: str
    nom: str
    couleur: str
    direction_aller: str
    direction_retour: str


class Stop(BaseModel):
    id: str
    nom: str
    latitude: float
    longitude: float
    line_id: str


class Driver(BaseModel):
    id: str
    nom: str
    prenom: str
    telephone: str
    bus_id: str | None = None


class Agent(BaseModel):
    id: str
    bus_id: str
    version: str
    dernier_ping: int
    token_jwt: str


class PositionGPS(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bus_id: str
    lat: float
    lng: float
    speed: float = Field(ge=0)
    heading: int = Field(ge=0, le=360)
    ts: int
    sig: str


class AlertCreate(BaseModel):
    type: str
    bus_id: str
    message: str


class Alert(BaseModel):
    id: str
    type: str
    bus_id: str
    message: str
    timestamp: int
    statut: AlertStatus


class User(BaseModel):
    id: str
    email: str
    role: Role
    hash_mdp: str
    date_creation: int


class ETAItem(BaseModel):
    bus_id: str
    stop_id: str
    eta_minutes: int
    distance_km: float


class KPIResponse(BaseModel):
    active_buses: int
    total_buses: int
    open_alerts: int
    coverage_ratio: float


class AIQueryRequest(BaseModel):
    query: str


class AIQueryResponse(BaseModel):
    answer: str
    data_points: dict[str, Any]
