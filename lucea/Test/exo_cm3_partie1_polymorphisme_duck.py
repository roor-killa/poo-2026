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
    print(doc.afficher())

documents = [Livre(), Magazine(), DVD()]
for doc in documents:
    presenter_document(doc)