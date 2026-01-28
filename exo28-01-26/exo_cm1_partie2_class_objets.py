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




#test


# Création d'un livre
livre1 = Livre("Peau noire, masques blancs", "Fanon", "E129N")

# Affichage du livre (doit être disponible)
print(livre1)

# Test de l'emprunt
if livre1.emprunter():
    print("Emprunt réussi")
else:
    print("Emprunt impossible")

# Affichage après emprunt
print(livre1)

# Test d'un second emprunt (doit échouer)
if livre1.emprunter():
    print("Emprunt réussi")
else:
    print("Emprunt impossible")

# Retour du livre
livre1.retourner()

# Affichage après retour
print(livre1)

# Affichage du nombre total de livres créés
print("Nombre total de livres :", Livre.nombre_total)