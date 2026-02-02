# Approche procédurale
livre1_titre = "1984"
livre1_auteur = "George Orwell"
livre1_disponible = True

# VS Approche objet
class Livre:
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.disponible = True

livre1 = Livre("1984", "George Orwell")


## QUESTIONS ##
# - Que se passe-t-il si on a 1000 livres en procédural ?
# - Comment gérer la cohérence des données ?