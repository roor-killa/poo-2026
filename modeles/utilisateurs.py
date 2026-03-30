from abc import ABC, abstractmethod

class Utilisateur(ABC):
    """Classe de base abstraite pour tous les utilisateurs de la bibliothèque"""

    def __init__(self, nom: str, prenom: str, identifiant: str):
        self.nom = nom
        self.prenom = prenom
        self.identifiant = identifiant
        self.emprunts_actifs = []  # liste des documents empruntés actuellement

    @abstractmethod
    def nombre_max_emprunts(self) -> int:
        """Retourne le nombre maximum d'emprunts autorisés pour cet utilisateur"""
        pass

    def peut_emprunter(self) -> bool:
        """Vérifie si l'utilisateur peut encore emprunter un document"""
        return len(self.emprunts_actifs) < self.nombre_max_emprunts()

    def ajouter_emprunt(self, document):
        """Ajoute un document à la liste des emprunts actifs"""
        if self.peut_emprunter():
            self.emprunts_actifs.append(document)
        else:
            raise Exception(f"{self.prenom} {self.nom} a atteint le nombre maximum d'emprunts.")

    def retourner_emprunt(self, document):
        """Retire un document des emprunts actifs"""
        if document in self.emprunts_actifs:
            self.emprunts_actifs.remove(document)
        else:
            raise Exception("Ce document n'est pas dans la liste des emprunts actifs.")

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.identifiant})"


# --- Classes concrètes ---

class Etudiant(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 5  # par exemple, un étudiant peut emprunter 5 documents max


class Enseignant(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 10  # un enseignant peut emprunter 10 documents max


class Personnel(Utilisateur):
    def nombre_max_emprunts(self) -> int:
        return 7  # personnel administratif par exemple

# --- Exemple de mixin pour privilège ---
class PrivilègePremiumMixin:
    """Mixin donnant droit à des emprunts prolongés"""
    def nombre_max_emprunts(self) -> int:
        return super().nombre_max_emprunts() + 3  # +3 documents