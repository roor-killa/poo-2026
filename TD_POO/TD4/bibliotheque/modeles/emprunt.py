# on importe datetime pour gérer les dates
from datetime import datetime, timedelta


# -----------------------------
# Classe Emprunt
# -----------------------------

class Emprunt:

    def __init__(self, utilisateur, document, date_emprunt=None):

        # utilisateur qui emprunte le document
        self.utilisateur = utilisateur

        # document emprunté
        self.document = document

        # si aucune date n'est donnée on prend la date actuelle
        self.date_emprunt = date_emprunt if date_emprunt else datetime.now()

        # calcul de la date limite
        # on ajoute la durée maximale d'emprunt du document
        duree = document.calculer_duree_max_emprunt()

        self.date_retour_prevue = self.date_emprunt + timedelta(days=duree)

        # date réelle de retour (None tant que le document n'est pas rendu)
        self.date_retour = None


    # -----------------------------
    # vérifier si l'emprunt est en retard
    # -----------------------------
    def est_en_retard(self):

        # si le document n'est pas encore retourné
        if self.date_retour is None:

            return datetime.now() > self.date_retour_prevue

        # si déjà retourné
        return self.date_retour > self.date_retour_prevue


    # -----------------------------
    # calcul des frais de retard
    # -----------------------------
    def calculer_frais(self):

        # si pas de retard → aucun frais
        if not self.est_en_retard():
            return 0

        # calcul du nombre de jours de retard
        if self.date_retour is None:

            jours_retard = (datetime.now() - self.date_retour_prevue).days

        else:

            jours_retard = (self.date_retour - self.date_retour_prevue).days

        # utiliser la méthode du document pour calculer les frais
        return self.document.calculer_frais_retard(jours_retard)


    # -----------------------------
    # retourner le document
    # -----------------------------
    def retourner(self):

        # enregistrer la date de retour
        self.date_retour = datetime.now()

        # rendre le document disponible
        self.document.disponible = True


    # affichage lisible
    def __str__(self):

        return f"{self.utilisateur.nom} a emprunté '{self.document.titre}'"