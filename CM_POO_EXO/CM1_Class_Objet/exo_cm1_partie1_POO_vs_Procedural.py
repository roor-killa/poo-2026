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
#       Pour 1000 livres on a 3000 ligne de code ce qui rend illisible le code.
# - Comment gérer la cohérence des données ?
#       Grace a la programmation object Orienté on a des outils qui nous permet de diminué 3000 ligne de code en 1005 (1000ajoute de livre si on part de l'exemple)
