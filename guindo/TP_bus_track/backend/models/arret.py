from dataclasses import dataclass


@dataclass
class Arret:
    """Représente un arrêt de bus sur une ligne."""
    id: int
    nom: str
    latitude: float
    longitude: float
    ordre: int

    def __repr__(self):
        return f"Arret(id={self.id}, nom='{self.nom}', pos=({self.latitude:.4f}, {self.longitude:.4f}))"
