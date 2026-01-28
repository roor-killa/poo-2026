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
        Livre.__init__(self, titre, auteur, isbn)
        Empruntable.__init__(self)
        Reservable.__init__(self)
        self.format_fichier = format_fichier


#test

# Vérification du MRO
print("MRO LivreNumerique :")
for cls in LivreNumerique.__mro__:
    print(cls)

print("\n---\n")

# Création d’un livre numérique
livre_num = LivreNumerique(
    "Peau noire, masques blancs",
    "Fanon",
    "ISBN123",
    "PDF"
)

# Vérification des attributs hérités
print("Titre :", livre_num.titre)
print("Auteur :", livre_num.auteur)
print("ISBN :", livre_num.isbn)
print("Format :", livre_num.format_fichier)
print("Disponible :", livre_num.disponible)

print("\n---\n")

# Test de l’emprunt
print("Emprunt par Alice :", livre_num.emprunter("Alice"))
print("Emprunté par :", livre_num.emprunte_par)

# Tentative de second emprunt (doit échouer)
print("Emprunt par Bob :", livre_num.emprunter("Bob"))
print("Emprunté par :", livre_num.emprunte_par)

print("\n---\n")

# Test des réservations
livre_num.reserver("Bob")
livre_num.reserver("Charlie")
print("Réservations :", livre_num.reservations)

print("\n---\n")

# Vérification de l’attribut de classe
print("Nombre total de livres :", Livre.nombre_total)