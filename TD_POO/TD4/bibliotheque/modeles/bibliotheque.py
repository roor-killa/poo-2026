# on importe la classe Emprunt
from modeles.emprunt import Emprunt


# -----------------------------
# Classe Bibliotheque
# -----------------------------

class Bibliotheque:

    def __init__(self, nom):

        # nom de la bibliothèque
        self.nom = nom

        # catalogue de documents
        self.catalogue = []

        # liste des utilisateurs
        self.utilisateurs = []

        # emprunts en cours
        self.emprunts_actifs = []

        # historique des emprunts terminés
        self.historique = []

        # liste des observateurs (pattern Observer)
        self._observateurs = []


    # -----------------------------
    # ajouter un document
    # -----------------------------
    def ajouter_document(self, document):

        self.catalogue.append(document)


    # -----------------------------
    # ajouter un utilisateur
    # -----------------------------
    def ajouter_utilisateur(self, utilisateur):

        self.utilisateurs.append(utilisateur)


    # -----------------------------
    # ajouter un observateur
    # -----------------------------
    def ajouter_observateur(self, obs):

        self._observateurs.append(obs)


    # -----------------------------
    # notifier les observateurs
    # -----------------------------
    def notifier(self, evenement):

        for obs in self._observateurs:
            obs.update(evenement)


    # -----------------------------
    # rechercher un document
    # -----------------------------
    def rechercher_document(self, titre):

        for doc in self.catalogue:

            if doc.titre == titre:
                return doc

        return None


    # -----------------------------
    # emprunter un document
    # -----------------------------
    def emprunter(self, utilisateur, document):

        # vérifier disponibilité
        if not document.disponible:
            print("Document déjà emprunté")
            return

        # vérifier limite utilisateur
        if not utilisateur.peut_emprunter():
            print("Limite d'emprunts atteinte")
            return

        # créer un emprunt
        emprunt = Emprunt(utilisateur, document)

        # rendre document indisponible
        document.disponible = False

        # ajouter emprunt
        self.emprunts_actifs.append(emprunt)

        # ajouter à l'utilisateur
        utilisateur.emprunts.append(emprunt)

        # notifier les observateurs
        self.notifier(f"{utilisateur.nom} a emprunté {document.titre}")

        return emprunt


    # -----------------------------
    # retourner un document
    # -----------------------------
    def retourner(self, emprunt):

        # enregistrer le retour
        emprunt.retourner()

        # calcul des frais
        frais = emprunt.calculer_frais()

        # retirer de la liste active
        self.emprunts_actifs.remove(emprunt)

        # ajouter à l'historique
        self.historique.append(emprunt)

        # notifier observateurs
        self.notifier(f"{emprunt.utilisateur.nom} a retourné {emprunt.document.titre}")

        if frais > 0:
            print(f"Frais de retard : {frais} €")


    # -----------------------------
    # statistiques simples
    # -----------------------------
    def afficher_statistiques(self):

        print("----- Statistiques -----")

        print("Documents :", len(self.catalogue))

        print("Utilisateurs :", len(self.utilisateurs))

        print("Emprunts actifs :", len(self.emprunts_actifs))

        print("Historique emprunts :", len(self.historique))