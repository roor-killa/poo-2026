from abc import ABC, abstractmethod
from datetime import datetime

# Creer une classe abstraite Document
class Document(ABC):
    # Initialise l'attribue titre, auteur et date_emprunt
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.date_emprunt = None
    
    # Creer une methodeo abstraite qui calcule la duree m ax dun emprunt
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        """Retourne la durée maximale d'emprunt en jours"""
        pass
    
    # Creer une methodeo abstraite qui calcule le frais de retard
    @abstractmethod
    def calculer_frais_retard(self, jours_retard):
        """Calcule les frais de retard"""
        pass
    
    # Methode qui permet d'emprunter et donne l'heure
    def emprunter(self):
        self.date_emprunt = datetime.now()
    
    # Methode qui retourne Vrai si le document est remis en retard ou non si c'est le cas contraire
    def est_en_retard(self):
        if self.date_emprunt is None:
            return False
        jours_emprunt = (datetime.now() - self.date_emprunt).days
        return jours_emprunt > self.calculer_duree_max_emprunt()


# Creer une classe Livre qui herite les proprietes de la classe Document
class Livre(Document):
    def calculer_duree_max_emprunt(self): # Modifie la methode abstraite de document 
        return 21  # 3 semaines
    
    def calculer_frais_retard(self, jours_retard): # Modifie la methode abstraite de document 
        return jours_retard * 0.50

# Creer une classe Magazine qui herite les proprietes de la classe Document
class Magazine(Document):
    def calculer_duree_max_emprunt(self): # Modifie la methode abstraite de document 
        return 7  # 1 semaine
    
    def calculer_frais_retard(self, jours_retard): # Modifie la methode abstraite de document 
        return jours_retard * 0.20
    

# document = Document()  Erreur parce que on peut pas instanciée un classe abstraite 
livre = Livre("Mon Livre","Franglish")
livre.emprunter()
print(livre.date_emprunt)
print(livre.calculer_duree_max_emprunt())
print(livre.calculer_frais_retard(5))
print(livre.est_en_retard())

magazine = Magazine("Mon Magazine","Magazish")
magazine.emprunter()
print(magazine.date_emprunt)
print(magazine.calculer_duree_max_emprunt())
print(magazine.calculer_frais_retard(5))
print(magazine.est_en_retard())