class Livre:
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        self._titre = titre
        self._auteur = auteur
        self.__isbn = isbn #privé
        self._disponible = True
        Livre.nombre_total += 1
    
    @property
    def auteur(self):
        return self._titre
    
    @property
    def auteur(self):
        return self._auteur
    
    @property
    def isbn(self):
        return self.__isbn
    
    @property
    def disponible(self):
        return self._disponible
    
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def retourner(self):
        self.disponible = True
        
    #Méthode pour affichage
    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self._titre} par {self._auteur} - {statut}"
    
#Création d'objet
livre1 = Livre("titre", "auteur", "ISBN")
print(livre1)