from fastapi import APIRouter, HTTPException
from typing import List
from simulation.engine import simulateur
from api.schemas import LigneRead, ArretRead

router = APIRouter(prefix="/api/lignes", tags=["Lignes"])


@router.get("/", response_model=List[dict])
async def get_lignes():
    """Retourne toutes les lignes avec leurs arrêts."""
    return [
        {
            "id": l.id,
            "nom": l.nom,
            "couleur": l.couleur,
            "description": l.description,
            "nombre_arrets": l.nombre_arrets(),
            "arrets": [
                {"id": a.id, "nom": a.nom, "latitude": a.latitude, "longitude": a.longitude, "ordre": a.ordre}
                for a in l.arrets
            ],
        }
        for l in simulateur.lignes.values()
    ]


@router.get("/{ligne_id}", response_model=dict)
async def get_ligne(ligne_id: int):
    """Retourne le détail d'une ligne avec ses arrêts."""
    ligne = simulateur.lignes.get(ligne_id)
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne introuvable")
    return {
        "id": ligne.id,
        "nom": ligne.nom,
        "couleur": ligne.couleur,
        "description": ligne.description,
        "arrets": [
            {
                "id": a.id,
                "nom": a.nom,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "ordre": a.ordre,
            }
            for a in ligne.arrets
        ],
        "bus": simulateur.get_bus_par_ligne(ligne_id),
    }
