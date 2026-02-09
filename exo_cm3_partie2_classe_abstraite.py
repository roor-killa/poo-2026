from abc import ABC, abstractmethod
from datetime import datetime

class Document(ABC):
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.date_emprunt = None
    
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        """Retourne la durée maximale d'emprunt en jours"""
        pass
    
    @abstractmethod
    def calculer_frais_retard(self, jours_retard):
        """Calcule les frais de retard"""
        pass
    
    def emprunter(self):
        self.date_emprunt = datetime.now()
    
    def est_en_retard(self):
        if self.date_emprunt is None:
            return False
        jours_emprunt = (datetime.now() - self.date_emprunt).days
        return jours_emprunt > self.calculer_duree_max_emprunt()
    
    def calculer_jours_retard(self):
        """Calcule le nombre de jours de retard"""
        if self.date_emprunt is None:
            return 0
        jours_emprunt = (datetime.now() - self.date_emprunt).days
        duree_max = self.calculer_duree_max_emprunt()
        return max(0, jours_emprunt - duree_max)
    
    def afficher_frais_retard(self):
        """Affiche les frais de retard si applicable"""
        jours_retard = self.calculer_jours_retard()
        if jours_retard > 0:
            frais = self.calculer_frais_retard(jours_retard)
            print(f"Frais de retard pour '{self.titre}': {frais:.2f}€ ({jours_retard} jours)")
        else:
            print(f"'{self.titre}': pas de frais de retard")

class Livre(Document):
    def calculer_duree_max_emprunt(self):
        return 21  # 3 semaines
    
    def calculer_frais_retard(self, jours_retard):
        return jours_retard * 0.50

class Magazine(Document):
    def calculer_duree_max_emprunt(self):
        return 7  # 1 semaine
    
    def calculer_frais_retard(self, jours_retard):
        return jours_retard * 0.20

# Utilisation
print("=== Démonstration de la gestion des emprunts ===\n")

# Création de documents
documents = [
    Livre("Le Petit Prince", "Saint-Exupéry"), 
    Magazine("National Geographic", "Divers"),
    Livre("1984", "George Orwell"),
    Magazine("Courrier International", "Collectif")
]

# Emprunt et affichage des informations
print("1. État des emprunts (tous empruntés maintenant):")
for doc in documents:
    doc.emprunter()
    print(f"   - {doc.__class__.__name__}: '{doc.titre}' par {doc.auteur}")
    print(f"     Durée max: {doc.calculer_duree_max_emprunt()} jours")

print("\n2. Vérification des retards:")
for doc in documents:
    if doc.est_en_retard():
        print(f"   ⚠️  Le document '{doc.titre}' est en retard.")
        doc.afficher_frais_retard()
    else:
        print(f"   ✓ Le document '{doc.titre}' est à l'heure.")

print("\n3. Calcul des frais de retard simulés (3 jours de retard):")
jours_retard = 3
for doc in documents:
    frais = doc.calculer_frais_retard(jours_retard)
    print(f"   - '{doc.titre}': {frais:.2f}€ ({jours_retard} jours retard)")

