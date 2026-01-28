class Document:
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.disponible = True
    
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def afficher_info(self):
        return f"{self.titre} par {self.auteur}"

class Livre(Document):
    def __init__(self, titre, auteur, isbn, nb_pages):
        super().__init__(titre, auteur)
        self.isbn = isbn
        self.nb_pages = nb_pages
    
    def afficher_info(self):
        info_base = super().afficher_info()
        return f"{info_base} - ISBN: {self.isbn} ({self.nb_pages} pages)"

class Magazine(Document):
    def __init__(self, titre, auteur, numero, mois):
        super().__init__(titre, auteur)
        self.numero = numero
        self.mois = mois
    
    def afficher_info(self):
        info_base = super().afficher_info()
        return f"{info_base} - N°{self.numero} ({self.mois})"


#test

# Test de la classe Document
doc1 = Document("Peau noire, masques blancs", "Fanon")

# Affichage des informations du document
print(doc1.afficher_info())  # Affiche : titre + auteur

# Test de l'emprunt
if doc1.emprunter():
    print("Document emprunté")
else:
    print("Document indisponible")

# Vérification de l'état après emprunt
print("Disponible :", doc1.disponible)


# Test de la classe Livre (héritage + surcharge)
livre1 = Livre("Peau noire, masques blancs", "Fanon", "AA11EE", 100)

# Affichage des informations du livre
print(livre1.afficher_info())

# Emprunt du livre
livre1.emprunter()
print("Disponible :", livre1.disponible)


# Test de la classe Magazine
mag1 = Magazine("Sciences & Vie", "Rédaction", 245, "Mars")

# Affichage des informations du magazine
print(mag1.afficher_info())
