from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        pass
    
    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass


class Livre(Document): #classe qui représente un livre avec des attributs tels que le titre, l'auteur, l'ISBN et le nombre de pages
    def __init__(self, titre, auteur, isbn, nb_pages):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.nb_pages = nb_pages

    def calculer_duree_max_emprunt(self):
        return 30  # Durée maximale d'emprunt pour un livre en jours

    def calculer_frais_retard(self, jours):
        return jours * 0.5  # Frais de retard pour un livre en euros par jour de retard


class Magazine(Document): #classe qui représente un magazine avec des attributs tels que le titre, l'éditeur, le numéro et le mois de publication
    def __init__(self, titre, editeur, numero, mois):
        self.titre = titre
        self.editeur = editeur
        self.numero = numero
        self.mois = mois

    def calculer_duree_max_emprunt(self):
        return 15  # Durée maximale d'emprunt pour un magazine en jours

    def calculer_frais_retard(self, jours):
        return jours * 0.25  # Frais de retard pour un magazine en euros par jour de retard


class DVD(Document): #classe qui représente un DVD avec des attributs tels que le titre, le réalisateur et la durée
    def __init__(self, titre, realisateur, duree):
        self.titre = titre
        self.realisateur = realisateur
        self.duree = duree

    def calculer_duree_max_emprunt(self):
        return 21  # Durée maximale d'emprunt pour un DVD en jours

    def calculer_frais_retard(self, jours):
        return jours * 0.75  # Frais de retard pour un DVD en euros par jour de retard


class Ebook(Document): #classe qui représente un ebook avec des attributs tels que le titre, l'auteur, le format et la taille en Mo
    def __init__(self, titre, auteur, format, taille_mo):
        self.titre = titre
        self.auteur = auteur
        self.format = format
        self.taille_mo = taille_mo

    def calculer_duree_max_emprunt(self):
        return 30  # Durée maximale d'emprunt pour un ebook en jours

    def calculer_frais_retard(self, jours):
        return jours * 0.25  # Frais de retard pour un ebook en euros par jour de retard