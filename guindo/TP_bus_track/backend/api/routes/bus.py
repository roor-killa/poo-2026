from fastapi import APIRouter, HTTPException
from typing import List
from simulation.engine import simulateur
from api.schemas import BusPosition

router = APIRouter(prefix="/api/bus", tags=["Bus"])


@router.get("/", response_model=List[dict])
async def get_tous_les_bus():
    """Retourne la position actuelle de tous les bus actifs."""
    return simulateur.get_toutes_positions()


@router.get("/{bus_id}", response_model=dict)
async def get_bus(bus_id: int):
    """Retourne le détail d'un bus (position, ligne, statut)."""
    bus = simulateur.bus.get(bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus introuvable")
    return bus.to_dict()
