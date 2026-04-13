from dataclasses import dataclass, field
from typing import List
from models.arret import Arret


@dataclass
class Ligne:
    """Représente une ligne de bus avec ses arrêts."""
    id: int
    nom: str
    couleur: str
    description: str
    arrets: List[Arret] = field(default_factory=list)

    def get_arret(self, index: int) -> Arret | None:
        """Retourne l'arrêt à l'index donné, ou None si hors limites."""
        if 0 <= index < len(self.arrets):
            return self.arrets[index]
        return None

    def nombre_arrets(self) -> int:
        return len(self.arrets)

    def __repr__(self):
        return f"Ligne(id={self.id}, nom='{self.nom}', arrets={self.nombre_arrets()})"
