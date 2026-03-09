# On importe ABC et abstractmethod pour créer une classe abstraite
# Une classe abstraite est une classe qui ne peut pas être instanciée directement
from abc import ABC, abstractmethod


# Classe de base Utilisateur
# Elle hérite de ABC pour devenir une classe abstraite
class Utilisateur(ABC):

    # Constructeur de la classe
    # Il initialise les informations communes à tous les utilisateurs
    def __init__(self, nom, prenom, id_utilisateur):

        # nom de l'utilisateur
        self.nom = nom

        # prenom de l'utilisateur
        self.prenom = prenom

        # identifiant unique dans la bibliothèque
        self.id_utilisateur = id_utilisateur

        # liste qui contient les documents actuellement empruntés
        self.emprunts_actifs = []

    # méthode permettant d'emprunter un document
    def emprunter(self, document):

        # on vérifie que l'utilisateur n'a pas dépassé la limite d'emprunts
        if len(self.emprunts_actifs) < self.nombre_max_emprunts():

            # on ajoute le document dans la liste
            self.emprunts_actifs.append(document)

            print(f"{self.nom} emprunte {document}")

        else:

            # si la limite est atteinte
            print("Limite d'emprunts atteinte")

    # méthode pour retourner un document
    def retourner(self, document):

        # on vérifie que le document est bien dans la liste
        if document in self.emprunts_actifs:

            # on retire le document de la liste
            self.emprunts_actifs.remove(document)

            print(f"{self.nom} retourne {document}")

    # méthode abstraite
    # chaque sous-classe doit définir combien de livres elle peut emprunter
    @abstractmethod
    def nombre_max_emprunts(self):
        pass

    # méthode abstraite
    # chaque sous-classe doit définir la durée maximale d'emprunt
    @abstractmethod
    def duree_max_emprunt(self):
        pass


# Classe Etudiant qui hérite de Utilisateur
class Etudiant(Utilisateur):

    # constructeur
    # super() appelle le constructeur de la classe parent Utilisateur
    def __init__(self, nom, prenom, id_utilisateur):

        # permet d'initialiser les attributs du parent
        super().__init__(nom, prenom, id_utilisateur)

    # nombre maximum d'emprunts pour un étudiant
    def nombre_max_emprunts(self):

        return 5

    # durée maximale d'emprunt
    def duree_max_emprunt(self):

        return 21

    # méthode spéciale pour afficher l'objet
    def __str__(self):

        return f"Etudiant : {self.prenom} {self.nom}"


# Classe Enseignant qui hérite de Utilisateur
class Enseignant(Utilisateur):

    def __init__(self, nom, prenom, id_utilisateur):

        super().__init__(nom, prenom, id_utilisateur)

    # un enseignant peut emprunter plus de documents
    def nombre_max_emprunts(self):

        return 10

    # durée d'emprunt plus longue
    def duree_max_emprunt(self):

        return 60

    def __str__(self):

        return f"Enseignant : {self.prenom} {self.nom}"


# Classe Personnel qui hérite de Utilisateur
class Personnel(Utilisateur):

    def __init__(self, nom, prenom, id_utilisateur):

        super().__init__(nom, prenom, id_utilisateur)

    # limite d'emprunts pour le personnel
    def nombre_max_emprunts(self):

        return 7

    # durée maximale d'emprunt
    def duree_max_emprunt(self):

        return 30

    def __str__(self):

        return f"Personnel : {self.prenom} {self.nom}"


# ------------------------------
# TEST DU PROGRAMME
# ------------------------------

# création d'un étudiant
etudiant = Etudiant("Dupont", "Marie", "E12345")

# création d'un enseignant
enseignant = Enseignant("Martin", "Paul", "T001")

# afficher le nombre maximum d'emprunts
print(etudiant.nombre_max_emprunts())

# afficher la durée maximale
print(enseignant.duree_max_emprunt())

# l'étudiant emprunte un livre
etudiant.emprunter("Livre Python")

# afficher combien de documents sont empruntés
print(len(etudiant.emprunts_actifs))