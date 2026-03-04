from datetime import datetime, timedelta
from modeles.documents import Document
from modeles.utilisateurs import Utilisateur

class Emprunt:
    def __init__(self, utilisateur: Utilisateur, document: Document):
        self.utilisateur = utilisateur
        self.document = document
        self.date_emprunt = datetime.now()
        self.date_retour: datetime | None = None

    def est_en_retard(self) -> bool:
        duree_max = self.document.calculer_duree_max_emprunt()
        date_limite = self.date_emprunt + timedelta(days=duree_max)
        return datetime.now() > date_limite

    def calculer_frais(self) -> float:
        if self.date_retour is None:
            # retour non effectué, calcul sur la durée écoulée
            jours_retard = max((datetime.now() - self.date_emprunt).days - self.document.calculer_duree_max_emprunt(), 0)
        else:
            jours_retard = max((self.date_retour - self.date_emprunt).days - self.document.calculer_duree_max_emprunt(), 0)
        return self.document.calculer_frais_retard(jours_retard)