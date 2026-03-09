# -----------------------------
# Classe Livre
# -----------------------------

# représente un livre dans la bibliothèque
class Livre:

    def __init__(self, titre, auteur, isbn, nb_pages):

        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.nb_pages = nb_pages

    def __str__(self):

        return f"Livre : {self.titre} - {self.auteur}"


# -----------------------------
# Classe Magazine
# -----------------------------

class Magazine:

    def __init__(self, titre, editeur, numero, mois):

        self.titre = titre
        self.editeur = editeur
        self.numero = numero
        self.mois = mois

    def __str__(self):

        return f"Magazine : {self.titre} ({self.mois})"


# -----------------------------
# Classe DVD
# -----------------------------

class DVD:

    def __init__(self, titre, realisateur, duree):

        self.titre = titre
        self.realisateur = realisateur
        self.duree = duree

    def __str__(self):

        return f"DVD : {self.titre} - {self.realisateur}"


# -----------------------------
# Classe EBook
# -----------------------------

class EBook:

    def __init__(self, titre, auteur, format, taille_mo):

        self.titre = titre
        self.auteur = auteur
        self.format = format
        self.taille_mo = taille_mo

    def __str__(self):

        return f"EBook : {self.titre} ({self.format})"


# -----------------------------
# Factory Pattern
# -----------------------------

class FabriqueDocument:

    # méthode statique qui crée les objets
    @staticmethod
    def creer(type_doc, **kwargs):

        # selon le type demandé on crée l'objet correspondant
        if type_doc == "livre":
            return Livre(**kwargs)

        elif type_doc == "magazine":
            return Magazine(**kwargs)

        elif type_doc == "dvd":
            return DVD(**kwargs)

        elif type_doc == "ebook":
            return EBook(**kwargs)

        else:
            # gestion erreur si type inconnu
            raise ValueError(f"Type de document inconnu : {type_doc}")


# -----------------------------
# Données simulant une base
# -----------------------------

donnees = [
    {"type": "livre", "titre": "1984", "auteur": "Orwell", "isbn": "123", "nb_pages": 328},
    {"type": "magazine", "titre": "Science", "editeur": "Nature", "numero": 42, "mois": "Janvier"},
    {"type": "dvd", "titre": "Matrix", "realisateur": "Wachowski", "duree": 136}
]


# liste de documents créés
documents = []

for data in donnees:

    # on récupère le type
    type_doc = data.pop("type")

    # on crée le document via la factory
    doc = FabriqueDocument.creer(type_doc, **data)

    documents.append(doc)


# affichage
for doc in documents:
    print(doc)