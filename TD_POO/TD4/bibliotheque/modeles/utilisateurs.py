# On importe ABC et abstractmethod pour créer une classe abstraite
from abc import ABC, abstractmethod


# -----------------------------
# Classe abstraite Utilisateur
# -----------------------------

# Cette classe représente un utilisateur générique de la bibliothèque
# Elle sert de base pour les autres types d'utilisateurs
class Utilisateur(ABC):

    def __init__(self, nom, prenom, id_utilisateur):

        # nom de l'utilisateur
        self.nom = nom

        # prénom de l'utilisateur
        self.prenom = prenom

        # identifiant unique
        self.id_utilisateur = id_utilisateur

        # liste des emprunts actifs
        self.emprunts = []


    # méthode abstraite : chaque type d'utilisateur a une limite différente
    @abstractmethod
    def nombre_max_emprunts(self):
        pass


    # méthode qui vérifie si l'utilisateur peut emprunter
    def peut_emprunter(self):

        # on compare le nombre d'emprunts actifs avec la limite
        return len(self.emprunts) < self.nombre_max_emprunts()


    # affichage lisible de l'utilisateur
    def __str__(self):

        return f"{self.prenom} {self.nom} ({self.id_utilisateur})"



# -----------------------------
# Classe Etudiant
# -----------------------------

# Hérite de Utilisateur
class Etudiant(Utilisateur):

    def __init__(self, nom, prenom, id_utilisateur):

        # appel du constructeur parent
        super().__init__(nom, prenom, id_utilisateur)


    # limite d'emprunt pour un étudiant
    def nombre_max_emprunts(self):

        return 5



# -----------------------------
# Classe Enseignant
# -----------------------------

class Enseignant(Utilisateur):

    def __init__(self, nom, prenom, id_utilisateur):

        super().__init__(nom, prenom, id_utilisateur)


    # les enseignants peuvent emprunter plus
    def nombre_max_emprunts(self):

        return 10



# -----------------------------
# Classe Personnel
# -----------------------------

class Personnel(Utilisateur):

    def __init__(self, nom, prenom, id_utilisateur):

        super().__init__(nom, prenom, id_utilisateur)


    # limite intermédiaire
    def nombre_max_emprunts(self):

        return 7