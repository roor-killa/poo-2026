class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.documents = []
    
    def ajouter(self, document):
        self.documents.append(document)
    
    def __len__(self):
        return len(self.documents)
    
    def __getitem__(self, index):
        return self.documents[index]
    
    def __contains__(self, titre):
        return any(doc.titre == titre for doc in self.documents)
    
    def __str__(self):
        return f"Bibliothèque {self.nom} avec {len(self)} documents"

# Utilisation naturelle
biblio = Bibliotheque("Schoelcher")
biblio.ajouter(Livre("1984", "Orwell"))
print(len(biblio))  # Utilise __len__
print("1984" in biblio)  # Utilise __contains__
print(biblio[0])  # Utilise __getitem__