# ----------------------------
# MIXIN 1 : Accès salle recherche
# ----------------------------

# Une Mixin est une classe qui ajoute une fonctionnalité
# Elle n'est pas destinée à être utilisée seule
class AccesSalleRecherche:

    # méthode permettant d'accéder à la salle de recherche
    def acceder_salle_recherche(self):

        return f"{self.nom} accède à la salle de recherche"


# ----------------------------
# MIXIN 2 : Priorité réservation
# ----------------------------

class PrioriteReservation:

    # méthode pour réserver un document avec priorité
    def reserver_avec_priorite(self, document):

        return f"{self.nom} réserve {document} en priorité"


# ----------------------------
# Classe Etudiant (classe simple pour l'exercice)
# ----------------------------

class Etudiant:

    # constructeur
    def __init__(self, nom, prenom, id_utilisateur):

        self.nom = nom
        self.prenom = prenom
        self.id_utilisateur = id_utilisateur


# ----------------------------
# Classe Doctorant
# ----------------------------

# Héritage multiple
# Doctorant hérite de :
# - Etudiant
# - AccesSalleRecherche
# - PrioriteReservation

class Doctorant(Etudiant, AccesSalleRecherche, PrioriteReservation):

    def __init__(self, nom, prenom, id_utilisateur, directeur_these):

        # super() appelle le constructeur de la première classe parent
        # ici Etudiant
        super().__init__(nom, prenom, id_utilisateur)

        # attribut spécifique au doctorant
        self.directeur_these = directeur_these


# ----------------------------
# TEST DU PROGRAMME
# ----------------------------

# création d'un doctorant
doctorant = Doctorant("Durand", "Alice", "D001", "Prof Martin")

# test des méthodes héritées
print(doctorant.acceder_salle_recherche())

print(doctorant.reserver_avec_priorite("Livre IA"))


# afficher le MRO
print(Doctorant.__mro__)