class Livre:
    def __init__(self, titre, auteur, isbn):
        self._titre = titre
        self._auteur = auteur
        self.isbn = isbn  # Privé
        self._disponible = True
    
    #@property
    #def isbn(self):
    #    return self.__isbn
    
    @property
    def titre(self):
        return self._titre
    
    @titre.setter
    def titre(self, nouveau_titre):
        if len(nouveau_titre) > 0:
            self._titre = nouveau_titre
        else:
            raise ValueError("Le titre ne peut pas être vide")

    
livre1 = Livre("Test titre","Mon auteur", "12ZAZ")
print(livre1.titre)

livre1.__isbn="123" 