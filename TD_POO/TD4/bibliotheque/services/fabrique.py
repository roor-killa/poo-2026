# on importe les classes de documents
from modeles.documents import Livre, Magazine, DVD, EBook


# -----------------------------
# Factory Pattern
# -----------------------------

# Cette classe sert à créer les documents automatiquement
class FabriqueDocument:

    # dictionnaire qui associe un type de document à sa classe
    _types = {
        "livre": Livre,
        "magazine": Magazine,
        "dvd": DVD,
        "ebook": EBook
    }


    # méthode de classe pour créer un document
    @classmethod
    def creer(cls, type_doc, **kwargs):

        # vérifier si le type existe dans le dictionnaire
        if type_doc not in cls._types:

            raise ValueError(f"Type de document inconnu : {type_doc}")

        # récupérer la classe correspondante
        classe_document = cls._types[type_doc]

        # créer l'objet avec les paramètres fournis
        return classe_document(**kwargs)