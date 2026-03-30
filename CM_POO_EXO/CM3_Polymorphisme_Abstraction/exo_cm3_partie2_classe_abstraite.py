from abc import ABC, abstractmethod
from datetime import datetime

class Document(ABC):
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.date_emprunt = None
    
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        """Retourne la durée maximale d'emprunt en jours"""
        pass
    
    @abstractmethod
    def calculer_frais_retard(self, jours_retard):
        """Calcule les frais de retard"""
        pass
    
    def emprunter(self):
        self.date_emprunt = datetime.now()
    
    def est_en_retard(self):
        if self.date_emprunt is None:
            return False
        jours_emprunt = (datetime.now() - self.date_emprunt).days
        return jours_emprunt > self.calculer_duree_max_emprunt()

class Livre(Document):
    def calculer_duree_max_emprunt(self):
        return 21  # 3 semaines
    
    def calculer_frais_retard(self, jours_retard):
        return jours_retard * 0.50

class Magazine(Document):
    def calculer_duree_max_emprunt(self):
        return 7  # 1 semaine
    
    def calculer_frais_retard(self, jours_retard):
        return jours_retard * 0.20