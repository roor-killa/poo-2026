
class Livre:
    def __init__(self, titre, auteur, isbn):
        self._titre = titre
        self._auteur = auteur
        self.__isbn = isbn  # Privé
        self._disponible = True
    
    @property
    def isbn(self):
        return self.__isbn
    
    @property
    def titre(self):
        return self._titre
    
    @titre.setter
    def titre(self, nouveau_titre):
        if len(nouveau_titre) > 0:
            self._titre = nouveau_titre
        else:
            raise ValueError("Le titre ne peut pas être vide")
        


livre1 = Livre('Harry Potter','Jsp',123456789)

# ISBN
print(livre1.isbn) # Afficher 123456789
# print(livre1.__isbn)   Attribute error : l'attribut existe pas dans la class Livre
# livre1.isbn = 9  Attribute Error, comme il y a pas de setter

# Auteur
print(livre1._auteur) # Afficher Jsp
livre1._auteur = "Chanteuse" # Change _auteur a "Chanteuse"
print(livre1._auteur)

#titre
print(livre1._titre) # Tjr accessible a cause du
print(livre1.titre) # Tjr accessible
livre1._titre = "Mission Inclota" # Change le titre grace au setters
print(livre1.titre)
livre1.titre = "Mission Nothing" # Change le titre grace au setters p
print(livre1.titre)