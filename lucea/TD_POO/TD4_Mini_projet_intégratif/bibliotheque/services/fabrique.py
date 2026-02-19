from TD4_Mini_projet_intégratif.bibliotheque.modeles.documents import Livre, Magazine, DVD, Ebook

class FabriqueDocument: #classe implémentant le design pattern de la fabrique pour créer des instances de différentes classes de documents en fonction d'un type de document donné
    _types = {
        "livre": Livre,
        "magazine": Magazine,
        "dvd": DVD,
        "ebook": Ebook
    }
    
    @classmethod
    def creer(cls, type_doc, **kwargs):
        if type_doc in cls._types:
            return cls._types[type_doc](**kwargs)
        else:
            raise ValueError(f"Type de document inconnu : {type_doc}")