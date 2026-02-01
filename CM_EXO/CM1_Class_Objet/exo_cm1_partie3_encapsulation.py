class Livre:
    # Definit les attributs titre, auteur, isbn, disponible
    def __init__(self, titre, auteur, isbn):
        self._titre = titre
        self._auteur = auteur
        self.__isbn = isbn  # Privé
        self._disponible = True
    
    #Permet d'acceder a l'attributs isbn
    @property
    def isbn(self):
       return self.__isbn
    
    #Permet d'acceder a l'attributs isbn (on peut aussi l'acceder avec sans utiliser cette function comme il y a que un underscore)
    @property
    def titre(self):
        return self._titre
    
    #Permet de changer l'attribut titre
    @titre.setter
    def titre(self, nouveau_titre):
        if len(nouveau_titre) > 0:
            self._titre = nouveau_titre
        else:
            raise ValueError("Le titre ne peut pas être vide")

    
livre1 = Livre("Test titre","Mon auteur", "12ZAZ")

# print(livre1.__isbn)  Erreur d'Attribut, l'attribut n'existe pas car elle est privée
livre1.__isbn="123" # Sa change pas l'attribut __isbn mais creer une nouvellle attribut avec __isbn
print(livre1.__isbn) # Renvoie 123
print(livre1.isbn) # Renvoie 12ZAZ
# livre1.isbn = '12345'   Erreur d'Attribut, l'attribut n'existe pas

print(livre1._titre)
livre1._titre = 'Nouveau Titre' # On peut modifier _titre prc l'attribut n'est pas privée 
print(livre1._titre)
livre1.titre = 'Deuxieme nouveau Titre' # On modifier avec le @titre.setter
print(livre1._titre)