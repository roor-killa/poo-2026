from abc import ABC, abstractmethod

class Utilisateur(ABC):
    """Classe de base pour tous les utilisateurs de la bibliothèque"""

    def __init__(self, nom: str, prenom: str, identifiant: str):
        self.nom = nom
        self.prenom = prenom
        self.identifiant = identifiant
        self.emprunts_en_cours = []

    @abstractmethod
    def nombre_max_emprunts(self) -> int:
        """Retourne le nombre maximum de documents que l'utilisateur peut emprunter"""
        pass

class Etudiant(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 5  # max 5 documents pour un étudiant


class Enseignant(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 10  # max 10 documents pour un enseignant


class Personnel(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 7  # max 7 documents pour le personnel