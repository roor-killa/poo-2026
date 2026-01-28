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


#Le polymorphisme permet d’utiliser des objets de classes différentes 
# de manière uniforme, tant qu’ils partagent une même interface donc ici c'est 'afficher'


#test

# Création des différents documents
livre = Livre()
magazine = Magazine()
dvd = DVD()

# Test individuel de la méthode afficher()
print(livre.afficher())
print(magazine.afficher())
print(dvd.afficher())

# Test du polymorphisme avec une liste
documents = [livre, magazine, dvd]

for doc in documents:
    presenter_document(doc)
