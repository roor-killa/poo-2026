# on importe ABC pour créer une interface d'observateur
from abc import ABC, abstractmethod


# -----------------------------
# Interface Observateur
# -----------------------------

# Cette classe définit le comportement de tous les observateurs
class Observateur(ABC):

    # méthode appelée quand un événement se produit
    @abstractmethod
    def update(self, evenement):
        pass


# -----------------------------
# Journal des événements
# -----------------------------

class JournalEvenements(Observateur):

    def __init__(self):

        # liste des événements enregistrés
        self.journal = []

    def update(self, evenement):

        # ajouter l'événement au journal
        self.journal.append(evenement)

        # afficher dans la console
        print(f"[LOG] {evenement}")


# -----------------------------
# Statistiques des emprunts
# -----------------------------

class StatistiquesEmprunts(Observateur):

    def __init__(self):

        # compteur d'emprunts
        self.nb_emprunts = 0

        # compteur de retours
        self.nb_retours = 0

    def update(self, evenement):

        # vérifier si c'est un emprunt
        if "emprunté" in evenement:
            self.nb_emprunts += 1

        # vérifier si c'est un retour
        if "retourné" in evenement:
            self.nb_retours += 1

        print(f"[STATS] Emprunts: {self.nb_emprunts} | Retours: {self.nb_retours}")