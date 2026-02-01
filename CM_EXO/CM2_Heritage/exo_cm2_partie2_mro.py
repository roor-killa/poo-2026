class Livre:
    # Attribut de classe
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Creer les attributs tire, auteur, isbn, disponible + ajoute 1 a l'attribut nombre_total
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1

# Creer une Classe Empruntable
class Empruntable:
    # Creer l'attribue emprunte_par
    def __init__(self):
        self.emprunte_par = None
    
    # Creer une methode pour emprunter 
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return True
        return False

# Creer une Classe Reservable
class Reservable:
    # Creer une liste de reservatiosn
    def __init__(self):
        self.reservations = []
    
    # Creer une methode Reserver qui garde une historique de tous les personnes qui ont reserver
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)

# Creer une classe qui heritel es attributs et methodes de Livre, Empruntable, Reservable + ajoute l'attribut format_fichier
class LivreNumerique(Livre, Empruntable, Reservable):
    def __init__(self, titre, auteur, isbn, format_fichier):
        Livre.__init__(self, titre, auteur, isbn)
        Empruntable.__init__(self)
        Reservable.__init__(self)
        self.format_fichier = format_fichier

# Vérifier le MRO
print(LivreNumerique.__mro__) # Afficher (<class '__main__.LivreNumerique'>, <class '__main__.Livre'>, <class '__main__.Empruntable'>, <class '__main__.Reservable'>, <class 'object'>)

livre = LivreNumerique("Peau noire, masques blancs","Frantz Fanon","978-2-02-000000-0","PDF")
print(livre.reservations) # Renvoie listre vide
livre.emprunter('Randi')
print(livre.emprunte_par)
livre.reserver('Randi')
print(livre.reservations)