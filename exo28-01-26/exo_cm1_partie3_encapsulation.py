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

    
#test


# Création d'un livre
livre1 = Livre("Test titre", "Mon auteur", "12ZAZ")

# Accès au titre via le getter
print(livre1.titre)  # Doit afficher "Test titre"

# Modification du titre via le setter
livre1.titre = "Nouveau titre"
print(livre1.titre)  # Doit afficher "Nouveau titre"

# Tentative de modification avec un titre vide (doit lever une erreur)
try:
    livre1.titre = ""
except ValueError as e:
    print("Erreur :", e)

# Accès direct à l'attribut isbn (il est public ici)
print(livre1.isbn)

# Tentative de modification d'un attribut __isbn
# Cela ne modifie PAS l'attribut réel de l'objet
livre1.__isbn = "123"

# Vérification : l'attribut isbn original n'a pas changé
print(livre1.isbn)

# Affichage du dictionnaire interne de l'objet
# Permet de voir que __isbn est un nouvel attribut
print(livre1.__dict__)