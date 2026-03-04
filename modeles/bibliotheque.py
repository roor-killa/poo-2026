# modeles/bibliotheque.py
from modeles.documents import Document
from modeles.utilisateurs import Utilisateur
from modeles.emprunt import Emprunt
from typing import List, Optional

class Bibliotheque:
    def __init__(self, nom: str):
        self.nom = nom
        self.catalogue: List[Document] = []
        self.utilisateurs: List[Utilisateur] = []
        self.emprunts_actifs: List[Emprunt] = []
        self.historique: List[Emprunt] = []
        self.observateurs = []

    def ajouter_document(self, document: Document):
        self.catalogue.append(document)

    def ajouter_utilisateur(self, utilisateur: Utilisateur):
        self.utilisateurs.append(utilisateur)

    def ajouter_observateur(self, observateur):
        """Ajoute un observateur pour notifications (pattern Observer)"""
        self.observateurs.append(observateur)

    def notifier(self, message: str):
        for obs in self.observateurs:
            obs.update(message)

    def rechercher_document(self, titre: str) -> Optional[Document]:
        for doc in self.catalogue:
            if doc.titre == titre:
                return doc
        return None

    def emprunter(self, utilisateur: Utilisateur, document: Document):
        if not document.disponible:
            print(f"Le document '{document.titre}' n'est pas disponible.")
            return

        # Vérifie la limite d'emprunt de l'utilisateur
        emprunts_user = [e for e in self.emprunts_actifs if e.utilisateur == utilisateur]
        if len(emprunts_user) >= utilisateur.nombre_max_emprunts():
            print(f"{utilisateur.nom} a atteint sa limite d'emprunt.")
            return

        # Crée l'emprunt
        emprunt = Emprunt(utilisateur, document)
        self.emprunts_actifs.append(emprunt)
        document.disponible = False
        self.notifier(f"{utilisateur.nom} a emprunté '{document.titre}'.")

    def retourner(self, emprunt: Emprunt):
        if emprunt not in self.emprunts_actifs:
            print("Emprunt non trouvé.")
            return

        frais = emprunt.calculer_frais()
        emprunt.document.disponible = True
        self.emprunts_actifs.remove(emprunt)
        self.historique.append(emprunt)
        self.notifier(f"{emprunt.utilisateur.nom} a retourné '{emprunt.document.titre}'. Frais: {frais:.2f}€")

    def afficher_statistiques(self):
        print("=== Statistiques Bibliothèque ===")
        print(f"Documents total: {len(self.catalogue)}")
        print(f"Emprunts actifs: {len(self.emprunts_actifs)}")
        print(f"Historique: {len(self.historique)}")