# Creer une classe LIvre avec la methode qui affiche "Je suis un livre"
class Livre:
    def afficher(self):
        return "Je suis un livre"

# Creer une classe Magazine avec la methode qui affiche "Je suis un lmagazine"
class Magazine:
    def afficher(self):
        return "Je suis un magazine"

# Creer une classe DVD avec la methode qui affiche "Je suis un DVD"
class DVD:
    def afficher(self):
        return "Je suis un DVD"

# Creer une fct qui prend n'importe quel document et appelle sa methode afficher() pour afficher le document
def presenter_document(doc):
    # Peu importe le type, tant qu'il a une méthode afficher()
    print(doc.afficher())

# Polymorphisme en action
documents = [Livre(), Magazine(), DVD()] # Creer une livre avec un LIvre, Magazine et DVD

# Permet d'afficher tous les differents documents dans la variable documents comme chaque document a la meme methode afficher()
for doc in documents:
    presenter_document(doc)  # Affiche Je suis un livre /n Je suis un magazine /n Je suis un DVD

