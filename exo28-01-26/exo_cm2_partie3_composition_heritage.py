class Auteur:
    def __init__(self, nom, prenom, nationalite):
        self.nom = nom
        self.prenom = prenom
        self.nationalite = nationalite
    
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

class Editeur:
    def __init__(self, nom, ville):
        self.nom = nom
        self.ville = ville

class Livre:
    def __init__(self, titre, auteur, editeur, isbn):
        self.titre = titre
        self.auteur = auteur  # Composition : Livre "a un" Auteur
        self.editeur = editeur  # Composition : Livre "a un" Editeur
        self.isbn = isbn
    
    def afficher_info(self):
        return f"{self.titre} par {self.auteur.nom_complet()}, édité par {self.editeur.nom}"


#test

# Création d'un auteur
auteur1 = Auteur("Orwell", "George", "Britannique")

# Test de la méthode nom_complet
print("Nom complet de l'auteur :", auteur1.nom_complet())

print("\n---\n")

# Création d'un éditeur
editeur1 = Editeur("Gallimard", "Paris")

# Vérification des informations de l'éditeur
print("Éditeur :", editeur1.nom)
print("Ville :", editeur1.ville)

print("\n---\n")

# Création d'un livre (composition Auteur + Editeur)
livre1 = Livre("1984", auteur1, editeur1, "978-2070368228")

# Affichage des informations du livre
print(livre1.afficher_info())

# Vérification de l'accès aux objets composés
print("Auteur du livre :", livre1.auteur.nom_complet())
print("Éditeur du livre :", livre1.editeur.nom)