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


## QUESTIONS ##
# - Montrer du code généré par IA qui n'encapsule pas correctement
# - Pourquoi l'encapsulation est cruciale dans de gros projets
# - Pourquoi isbn est pivé ?
# - Comment je teste ma fonction titre ?