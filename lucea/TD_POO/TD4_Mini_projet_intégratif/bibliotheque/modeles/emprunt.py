from datetime import datetime # Importation de la classe datetime pour gérer les dates et les calculs de durée
from TD4_Mini_projet_intégratif.bibliotheque.modeles.documents import Livre, DVD, Magazine, Ebook # Importation des classes de documents spécifiques pour pouvoir typer l'objet emprunt


class Emprunt:
    def __init__(self, utilisateur, document, date_emprunt): # Méthode constructeur : initialise un emprunt avec l'utilisateur, le document et la date d'emprunt
        self.utilisateur = utilisateur
        self.document = document
        self.date_emprunt = date_emprunt
        self.date_retour = None # date_retour est initialisée à None car le document n'est pas encore rendu


    def est_en_retard(self, date_retour): # Méthode pour vérifier si un emprunt est en retard
        self.nb_jours = (date_retour - self.date_emprunt).days
        if self.nb_jours > self.document.calculer_duree_max_emprunt():
            return True
        else:
            return False

    
    def calculer_frais(self): # Méthode pour calculer les frais de retard, vérifie si le document est rendu en retard par rapport a la date actuelle
        if self.est_en_retard(datetime.now()):
            return f"Frais de retard : {self.document.calculer_frais_retard()} €"
        else:
            return "Aucun frais de retard"