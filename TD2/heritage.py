from abc import ABC, abstractmethod

class Utilisateur(ABC):
    def __init__(self, nom, prenom, id_utilisateur):
        self.nom = nom
        self.prenom = prenom
        self.id_utilisateur = id_utilisateur
        self.emprunts_actifs = []  # liste des documents empruntés

    def emprunter(self, document):
        if len(self.emprunts_actifs) >= self.nombre_max_emprunts():
            raise ValueError("Limite d'emprunts atteinte.")
        self.emprunts_actifs.append(document)       # bloque si on dépasse la limite

    def retourner(self, document):
        if document not in self.emprunts_actifs:
            raise ValueError("Ce document n'est pas dans les emprunts actifs.")
        self.emprunts_actifs.remove(document)      # retire le document s'il est présent

    @abstractmethod
    def nombre_max_emprunts(self):
        pass

    @abstractmethod
    def duree_max_emprunt(self):
        pass
