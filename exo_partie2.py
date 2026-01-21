class Livre:
    # Attribut de classe
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1
    
    # Méthode d'instance
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def retourner(self):
        self.disponible = True
    
    # Méthode pour affichage
    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self.titre} par {self.auteur} - {statut}"

livre1 = Livre("Peau noir et masque blanc", "Fanon", "E129N")
print(livre1)