from abc import ABC, abstractmethod


# -----------------------------
# Interface Observateur
# -----------------------------

# Classe abstraite représentant un observateur
# Tous les observateurs doivent implémenter la méthode update()
class Observateur(ABC):

    @abstractmethod
    def update(self, evenement):
        pass


# -----------------------------
# Observateur 1 : Journal
# -----------------------------

class JournalEvenements(Observateur):

    def __init__(self):

        # liste qui stocke tous les événements
        self.journal = []

    def update(self, evenement):

        # on ajoute l'événement dans le journal
        self.journal.append(evenement)

        print(f"[LOG] {evenement}")


# -----------------------------
# Observateur 2 : Statistiques
# -----------------------------

class StatistiquesEmprunts(Observateur):

    def __init__(self):

        # compteur des emprunts
        self.nb_emprunts = 0

        # compteur des retours
        self.nb_retours = 0

    def update(self, evenement):

        # si le message contient "emprunté"
        if "emprunté" in evenement:
            self.nb_emprunts += 1

        # si le message contient "retourné"
        if "retourné" in evenement:
            self.nb_retours += 1

        print(f"[STATS] Emprunts: {self.nb_emprunts} | Retours: {self.nb_retours}")


# -----------------------------
# Observateur 3 : Notification utilisateurs
# -----------------------------

class NotificateurUtilisateurs(Observateur):

    def update(self, evenement):

        print(f"[NOTIFICATION] {evenement}")


# -----------------------------
# Classe observable
# -----------------------------

class DocumentObservable:

    def __init__(self, titre):

        # titre du document
        self.titre = titre

        # liste des observateurs
        self._observateurs = []

    # ajouter un observateur
    def ajouter_observateur(self, obs):

        self._observateurs.append(obs)

    # retirer un observateur
    def retirer_observateur(self, obs):

        self._observateurs.remove(obs)

    # notifier tous les observateurs
    def notifier_observateurs(self, evenement):

        for obs in self._observateurs:
            obs.update(evenement)

    # méthode pour emprunter un document
    def emprunter(self, utilisateur):

        evenement = f"{utilisateur} a emprunté '{self.titre}'"

        # notifier tous les observateurs
        self.notifier_observateurs(evenement)

    # méthode pour retourner un document
    def retourner(self, utilisateur):

        evenement = f"{utilisateur} a retourné '{self.titre}'"

        self.notifier_observateurs(evenement)


# -----------------------------
# TEST DU PROGRAMME
# -----------------------------

# création du document
livre = DocumentObservable("Python Avancé")

# création des observateurs
journal = JournalEvenements()
stats = StatistiquesEmprunts()
notif = NotificateurUtilisateurs()

# ajout des observateurs
livre.ajouter_observateur(journal)
livre.ajouter_observateur(stats)
livre.ajouter_observateur(notif)

# simulation d'événements
livre.emprunter("Marie")
livre.retourner("Marie")