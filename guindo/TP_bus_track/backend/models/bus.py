import math
from dataclasses import dataclass, field
from typing import Optional
from models.arret import Arret
from models.ligne import Ligne


@dataclass
class Bus:
    """
    Représente un bus en circulation sur une ligne.
    Contient toute la logique de déplacement GPS (POO).
    """
    id: int
    nom: str
    ligne: Ligne
    latitude: float
    longitude: float
    vitesse: float = 40.0          # km/h
    statut: str = "en_service"     # en_service | a_larret | hors_service
    arret_courant_idx: int = 0
    direction: int = 1             # 1 = aller, -1 = retour (fait l'aller-retour)

    # Progression entre deux arrêts (0.0 → 1.0)
    progression: float = field(default=0.0, repr=False)

    def prochain_arret(self) -> Optional[Arret]:
        """Retourne le prochain arrêt cible."""
        idx = self.arret_courant_idx + self.direction
        return self.ligne.get_arret(idx)

    def arret_courant(self) -> Optional[Arret]:
        return self.ligne.get_arret(self.arret_courant_idx)

    def avancer(self, delta_secondes: float) -> None:
        """
        Fait avancer le bus sur sa trajectoire.
        Interpolation linéaire entre l'arrêt courant et le suivant.
        """
        if self.statut != "en_service":
            return

        prochain = self.prochain_arret()
        courant = self.arret_courant()

        if courant is None or prochain is None:
            # Fin de ligne : inverser la direction
            self.direction *= -1
            return

        # Distance entre les deux arrêts (en km)
        distance_km = self._haversine(
            courant.latitude, courant.longitude,
            prochain.latitude, prochain.longitude
        )

        if distance_km == 0:
            self._atteindre_prochain()
            return

        # Progression en fraction de segment par seconde
        fraction_par_seconde = (self.vitesse / 3600) / distance_km
        self.progression += fraction_par_seconde * delta_secondes

        # Interpolation de la position GPS
        t = min(self.progression, 1.0)
        self.latitude  = courant.latitude  + t * (prochain.latitude  - courant.latitude)
        self.longitude = courant.longitude + t * (prochain.longitude - courant.longitude)

        # Si on a atteint le prochain arrêt
        if self.progression >= 1.0:
            self._atteindre_prochain()

    def _atteindre_prochain(self) -> None:
        """Passe au segment suivant ou inverse la direction en bout de ligne."""
        prochain_idx = self.arret_courant_idx + self.direction
        self.progression = 0.0

        # Vérification des bornes → inversion de direction AVANT de bouger
        if prochain_idx >= self.ligne.nombre_arrets():
            self.direction = -1
            self.arret_courant_idx = self.ligne.nombre_arrets() - 1
        elif prochain_idx < 0:
            self.direction = 1
            self.arret_courant_idx = 0
        else:
            self.arret_courant_idx = prochain_idx

        # Mise à jour position exacte sur l'arrêt atteint
        arret = self.arret_courant()
        if arret:
            self.latitude = arret.latitude
            self.longitude = arret.longitude

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Distance en km entre deux coordonnées GPS (formule Haversine)."""
        R = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "ligne_id": self.ligne.id,
            "ligne_nom": self.ligne.nom,
            "ligne_couleur": self.ligne.couleur,
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6),
            "vitesse": self.vitesse,
            "statut": self.statut,
            "arret_courant": self.arret_courant().nom if self.arret_courant() else None,
            "prochain_arret": self.prochain_arret().nom if self.prochain_arret() else None,
        }

    def __repr__(self):
        return f"Bus(id={self.id}, nom='{self.nom}', ligne='{self.ligne.nom}', pos=({self.latitude:.4f}, {self.longitude:.4f}))"
