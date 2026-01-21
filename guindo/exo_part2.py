class Livre:
    # Attribut de classe (protégé)
    _nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance (privés pour titre/auteur, protégés pour les autres)
        self.__titre = titre
        self.__auteur = auteur
        self._isbn = isbn
        self._disponible = True
        Livre._nombre_total += 1
    
    # Méthode d'instance
    def emprunter(self):
        if self._disponible:
            self._disponible = False
            return True
        return False
    
    def retourner(self):
        self._disponible = True
    
    # Méthode pour affichage
    def __str__(self):
        statut = "Disponible" if self._disponible else "Emprunté"
        return f"{self.__titre} par {self.__auteur} est {statut}"

livre1 = Livre("1984", "George Orwell", "1234567890")
livre2 = Livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", "0987654321")

livre1.emprunter()
livre2.emprunter()
print(livre1)
print(livre2)

livre1.retourner()

print(livre1)
