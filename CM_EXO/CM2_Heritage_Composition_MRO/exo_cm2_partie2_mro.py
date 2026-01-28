class Livre:
    # Attribut de classe
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1

class Empruntable:
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return True
        return False

class Reservable:
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)

class LivreNumerique(Livre, Empruntable, Reservable):
    def __init__(self, titre, auteur, isbn, format_fichier):
        Livre.__init__(self, titre, auteur, isbn, 0)
        Empruntable.__init__(self)
        Reservable.__init__(self)
        self.format_fichier = format_fichier

# Vérifier le MRO
print(LivreNumerique.__mro__)