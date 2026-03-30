from abc import ABC, abstractmethod

class Document(ABC):
    """Classe de base pour tous les documents de la bibliothèque"""

    def __init__(self, titre: str):
        self.titre = titre
        self.disponible = True  # True si le document est empruntable

    @abstractmethod
    def calculer_duree_max_emprunt(self) -> int:
        """Retourne le nombre de jours max pour emprunt"""
        pass

    @abstractmethod
    def calculer_frais_retard(self, jours_retard: int) -> float:
        """Retourne le montant des frais de retard"""
        pass

class Livre(Document):
    def __init__(self, titre: str, auteur: str, isbn: str):
        super().__init__(titre)
        self.auteur = auteur
        self.isbn = isbn

    def calculer_duree_max_emprunt(self) -> int:
        return 30  # 30 jours pour un livre

    def calculer_frais_retard(self, jours_retard: int) -> float:
        return jours_retard * 0.5  # 0,5€ par jour


class Magazine(Document):
    def __init__(self, titre: str, editeur: str, numero: int):
        super().__init__(titre)
        self.editeur = editeur
        self.numero = numero

    def calculer_duree_max_emprunt(self) -> int:
        return 7  # 7 jours pour un magazine

    def calculer_frais_retard(self, jours_retard: int) -> float:
        return jours_retard * 0.2  # 0,2€ par jour


class DVD(Document):
    def __init__(self, titre: str, realisateur: str, duree: int):
        super().__init__(titre)
        self.realisateur = realisateur
        self.duree = duree  # durée en minutes

    def calculer_duree_max_emprunt(self) -> int:
        return 14  # 14 jours pour un DVD

    def calculer_frais_retard(self, jours_retard: int) -> float:
        return jours_retard * 1.0  # 1€ par jour


class EBook(Document):
    def __init__(self, titre: str, auteur: str, fichier: str):
        super().__init__(titre)
        self.auteur = auteur
        self.fichier = fichier  # chemin du fichier

    def calculer_duree_max_emprunt(self) -> int:
        return 21  # 21 jours pour un eBook

    def calculer_frais_retard(self, jours_retard: int) -> float:
        return 0  # pas de frais pour un eBook