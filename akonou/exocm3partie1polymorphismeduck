class Livre:
    def afficher(self):
        return "Je suis un livre"

class Magazine:
    def afficher(self):
        return "Je suis un magazine"

class DVD:
    def afficher(self):
        return "Je suis un DVD"

def presenter_document(doc):
    # Peu importe le type, tant qu'il a une méthode afficher()
    print(doc.afficher())

# Polymorphisme en action
documents = [Livre(), Magazine(), DVD()]
for doc in documents:
    presenter_document(doc)