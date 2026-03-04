from datetime import datetime, timedelta

class Emprunt:
    """Représente un emprunt d'un document par un utilisateur"""
    
    def __init__(self, utilisateur, document, date_emprunt=None):
        self.utilisateur = utilisateur
        self.document = document
        self.date_emprunt = date_emprunt or datetime.now()
        self.date_retour = self.date_emprunt + timedelta(days=document.calculer_duree_max_emprunt())
        self.retourne = False
    
    def est_en_retard(self):
        """Retourne True si le document est en retard"""
        if self.retourne:
            return False
        return datetime.now() > self.date_retour
    
    def calculer_frais(self):
        """Calcule les frais si l'emprunt est en retard"""
        if self.est_en_retard():
            jours_retard = (datetime.now() - self.date_retour).days
            return self.document.calculer_frais_retard(jours_retard)
        return 0.0
    
    def marquer_retour(self):
        """Marque l'emprunt comme retourné"""
        self.retourne = True