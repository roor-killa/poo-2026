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