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
    
   

    
livre1 = Livre("Test titre","Mon auteur", "12ZAZ")
print(livre1.titre)

livre1.__isbn="123" 