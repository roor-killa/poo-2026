class Bibliotheque: 
    def __init__(self, nom): 
        self.nom = nom
        self.catalogue = []
        self.utilisateurs = []
        self.emprunts_actifs = []
        self.historique = []

    
    def ajouter_document(self, document):
        # ...
        pass
    
    def emprunter(self, utilisateur, document):
        # Vérifier disponibilité
        # Vérifier limites utilisateur
        # Créer emprunt
        # Notifier observateurs
        pass
    
    def retourner(self, emprunt):
        # Calculer frais
        # Mettre à jour statuts
        # Notifier observateurs
        pass
    
    def rechercher_document(self, critere):
        # ...
        pass
    
    def statistiques(self):
        # Documents par type
        # Emprunts par utilisateur
        # Taux d'utilisation
        pass