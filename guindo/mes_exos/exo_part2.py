class Livre:
    # Attribut de classe
    _nombre_total = 0  # protégé (_)
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance
        self.__titre = titre        # privé (__)
        self.__auteur = auteur      # privé (__)
        self._isbn = isbn           # protégé (_)
        self._disponible = True     # protégé (_)
        Livre._nombre_total += 1
    
    # Propriétés (getters et setters)
    @property
    def titre(self):  # getter pour __titre
        return self.__titre
    
    @titre.setter
    def titre(self, nouveau_titre):
        if not nouveau_titre or not isinstance(nouveau_titre, str):
            raise ValueError("Le titre doit être une chaîne de caractères non vide")
        self.__titre = nouveau_titre
    
    @property
    def auteur(self):  # getter pour __auteur
        return self.__auteur
    
    @auteur.setter
    def auteur(self, nouvel_auteur):
        if not nouvel_auteur or not isinstance(nouvel_auteur, str):
            raise ValueError("L'auteur doit être une chaîne de caractères non vide")
        self.__auteur = nouvel_auteur
    
    @property
    def isbn(self):  # getter pour _isbn
        return self._isbn
    
    @isbn.setter
    def isbn(self, nouvel_isbn):
        if not isinstance(nouvel_isbn, str):
            raise ValueError("L'ISBN doit être une chaîne de caractères")
        if len(nouvel_isbn) != 10 and len(nouvel_isbn) != 13:
            raise ValueError("L'ISBN doit contenir 10 ou 13 caractères")
        self._isbn = nouvel_isbn
    
    @property
    def disponible(self):  # getter pour _disponible
        return self._disponible
    
    @disponible.setter
    def disponible(self, statut):
        if not isinstance(statut, bool):
            raise ValueError("Le statut de disponibilité doit être un booléen")
        self._disponible = statut
    
    @classmethod
    def get_nombre_total(cls):  # getter pour _nombre_total (attribut de classe)
        return cls._nombre_total
    
    # Méthode d'instance
    def emprunter(self):
        if self._disponible:
            self._disponible = False
            return True
        return False
    
    def retourner(self):
        self._disponible = True
    
    # Méthode pour affichage
    def __str__(self):
        statut = "Disponible" if self._disponible else "Emprunté"
        return f"{self.__titre} par {self.__auteur} est {statut}"

livre1 = Livre("1984", "George Orwell", "1234567890")
livre2 = Livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", "0987654321")

livre1.emprunter()
livre2.emprunter()
print(livre1)
print(livre2)

livre1.retourner()

livre1.titre = "1984 (nouvelle édition)"
livre1.auteur = "George Orwell"
livre1.isbn = "1234567890"
livre1.disponible = True

print(livre1)
