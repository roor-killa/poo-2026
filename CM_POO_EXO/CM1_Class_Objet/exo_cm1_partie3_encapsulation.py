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
#       les attributes self.auteur et self.disponible ne sont pas encapsuler par rapport a self.titre et self.isbn
#       car ils sont pas dans leur propre @property qui leurs rend exclusives a la class.
# - Pourquoi l'encapsulation est cruciale dans de gros projets
#       pour evité l'utilisation de mauvaise variables liée a des class inattendue
# - Pourquoi isbn est pivé ?
#       isbn est privée car elle se trouve sous un @property qui la rend privée et exclusive a la class livre.
# - Comment je teste ma fonction titre ?