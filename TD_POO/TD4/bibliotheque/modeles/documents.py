from abc import ABC, abstractmethod


# -----------------------------
# Classe abstraite Document
# -----------------------------

# Cette classe sert de modèle pour tous les types de documents
class Document(ABC):

    def __init__(self, titre):

        # titre du document
        self.titre = titre

        # indique si le document est disponible
        self.disponible = True


    # durée maximale d'emprunt
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        pass


    # calcul des frais de retard
    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass


# -----------------------------
# Classe Livre
# -----------------------------

class Livre(Document):

    def __init__(self, titre, auteur, isbn):

        super().__init__(titre)

        self.auteur = auteur
        self.isbn = isbn


    # durée maximale pour un livre
    def calculer_duree_max_emprunt(self):

        return 21


    # frais de retard par jour
    def calculer_frais_retard(self, jours):

        return jours * 0.5


# -----------------------------
# Classe Magazine
# -----------------------------

class Magazine(Document):

    def __init__(self, titre, editeur, numero):

        super().__init__(titre)

        self.editeur = editeur
        self.numero = numero


    def calculer_duree_max_emprunt(self):

        return 7


    def calculer_frais_retard(self, jours):

        return jours * 0.3


# -----------------------------
# Classe DVD
# -----------------------------

class DVD(Document):

    def __init__(self, titre, realisateur, duree):

        super().__init__(titre)

        self.realisateur = realisateur
        self.duree = duree


    def calculer_duree_max_emprunt(self):

        return 5


    def calculer_frais_retard(self, jours):

        return jours * 1


# -----------------------------
# Classe EBook
# -----------------------------

class EBook(Document):

    def __init__(self, titre, auteur, format):

        super().__init__(titre)

        self.auteur = auteur
        self.format = format


    def calculer_duree_max_emprunt(self):

        return 30


    def calculer_frais_retard(self, jours):

        return jours * 0.1