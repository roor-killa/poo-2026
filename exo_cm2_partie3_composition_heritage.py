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

# Utilisation
auteur1 = Auteur("Orwell", "George", "Britannique")
editeur1 = Editeur("Gallimard", "Paris")
livre1 = Livre("1984", auteur1, editeur1, "978-2070368228")

print(livre1.afficher_info())

