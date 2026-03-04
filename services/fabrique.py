from modeles.documents import Livre, Magazine, DVD, EBook

class FabriqueDocument:
    """Fabrique pour créer des documents à partir d'un type et de données"""

    @staticmethod
    def creer(type_doc: str, **kwargs):
        type_doc = type_doc.lower()
        if type_doc == "livre":
            return Livre(kwargs["titre"], kwargs["auteur"], kwargs["isbn"])
        elif type_doc == "magazine":
            return Magazine(kwargs["titre"], kwargs["editeur"], kwargs["numero"])
        elif type_doc == "dvd":
            return DVD(kwargs["titre"], kwargs["realisateur"], kwargs["duree"])
        elif type_doc == "ebook":
            return EBook(kwargs["titre"], kwargs["auteur"], kwargs["fichier"])
        else:
            raise ValueError(f"Type de document inconnu: {type_doc}")