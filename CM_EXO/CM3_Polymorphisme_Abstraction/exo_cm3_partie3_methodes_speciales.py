
# Creation de la classe Bibliotheque 
class Bibliotheque:
    # Creation des attributs nom et listes de documents
    def __init__(self, nom):
        self.nom = nom
        self.documents = []
    
    # Creation de la methode ajouter qui permet dajouter un document
    def ajouter(self, document):
        self.documents.append(document)
    
    # Creation de la methode qui permet de retourner le nb de documents quand on ecrit len(Bibliotheque)
    def __len__(self):
        return len(self.documents)
    
    # Creation d'une methode qui permet de directement de choisir un document avec un index 
    def __getitem__(self, index):
        return self.documents[index]
    
    # Creation d'une methode qui permet de verifier si le document est dans la bibliothèque  
    def __contains__(self, titre):
        return any(doc.titre == titre for doc in self.documents)
    
    # Creation de la methode qui permet d'affichier le nom de la bibliothèque avec le nb de documents 
    def __str__(self):
        return f"Bibliothèque {self.nom} avec {len(self)} documents"

bib = Bibliotheque("B1")
bib.ajouter("Peau noire, masques blancs")
bib.ajouter("L'Étranger")
bib.ajouter("1984")
print(bib)
print(bib[0])
print(len(bib))