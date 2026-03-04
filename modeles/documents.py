from abc import ABC, abstractmethod

class Document(ABC):
    def __init__(self, titre):
        self.titre = titre
        self.disponible = True

    @abstractmethod
    def calculer_duree_max_emprunt(self):
        pass

    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass