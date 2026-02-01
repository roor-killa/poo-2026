class Document:
    # Creer les attributs titre, auteur, disponible pour la classe Document
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.disponible = True
    
    # Fct qui permet d'emprunter un document et de changer son status
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    # Permet d'afficher le titre et l'auteur du document
    def afficher_info(self):
        return f"{self.titre} par {self.auteur}"

# Livre(Document) permet d'herités tous les attributs et méthodes de la classe Document
class Livre(Document):
    # Permet de d'ajouter les attributs isbn, nb_pages + les attributs heritees de la classe Document avec super().__init__() qui creer les attributs titre, auteur et disponible
    def __init__(self, titre, auteur, isbn, nb_pages):
        super().__init__(titre, auteur)
        self.isbn = isbn
        self.nb_pages = nb_pages
    
    def afficher_info(self):
        info_base = super().afficher_info() # Prend la methode afficher_info de la classe Document
        return f"{info_base} - ISBN: {self.isbn} ({self.nb_pages} pages)" # Permet d'afficher : Tire par auteur - ISBN : NB_ISBN (NB pages)

# Magazine(Document) permet d'herités tous les attributs et méthodes de la classe Document
class Magazine(Document):
    # Permet de creer les attributs numero, mois + les attributs heritees de la classe Document avec super().__init__() qui creer les attributs titre, auteur et disponible
    def __init__(self, titre, auteur, numero, mois):
        super().__init__(titre, auteur)
        self.numero = numero
        self.mois = mois
    
    def afficher_info(self):
        info_base = super().afficher_info() # Prend la methode afficher_info de la classe Document qui renvoie Titre par auteur
        return f"{info_base} - N°{self.numero} ({self.mois})"  # Permet d'afficher : Tire par auteur - N°NB (mois)
    
# ===

doc1 = Document("Peau noir et masque blanc", "Fanon")
print(doc1.afficher_info()) # Affiche : Peau noir et masque blanc par Fanon
print(doc1.emprunter()) # Affiche True donc le document a été emprunté

livre1 = Livre("Peau noir et masque blancx", "Fanonx", "AA11EE", "100")
print(livre1.afficher_info()) # Peau noir et masque blancx par Fanonx - ISBN: AA11EE (100 pages)
print(livre1.emprunter()) # Affiche True donc le livre a été emprunté (et la classe a bien heritee la methode emprunter())

magazine1 = Magazine("Toy Story", "Randi", "BB938H", "janvier")
print(magazine1.afficher_info()) # Toy Story par Randi - N°BB938H (janvier)
print(magazine1.emprunter()) # Affiche True donc le magazine1 a été emprunté (et la classe a bien heritee la methode emprunter())