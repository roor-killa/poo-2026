from abc import ABC, abstractmethod

# Permet de creer une classe abstraite Document qui ne peut pas etre instanciée mais va servir comme moule pour les classes Livre, Magazine, DVD
class Document(ABC):
    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass

# Creer une classe Livre qui herite la methode dans Document
class Livre(Document):
    def calculer_frais_retard(self, jours): # Modifie la methode herite de Document pour mettre un frais custom de 50 centimes / jour
        return jours * 0.50  # 0.50€ par jour

# Creer une classe Magazine qui herite la methode dans Document
class Magazine(Document):
    def calculer_frais_retard(self, jours): # Modifie la methode herite de Document pour mettre un frais custom de 20 centimes / jour
        return jours * 0.20  # 0.20€ par jour

# Creer une classe DVD qui herite la methode dans Document
class DVD(Document):
    def calculer_frais_retard(self, jours): # Modifie la methode herite de Document pour mettre un frais custom de 1 euro / jour
        return jours * 1.00  # 1€ par jour

def calculer_total_frais(documents, jours):
    total = 0
    for doc in documents:
        total += doc.calculer_frais_retard(jours)
    return total

# document = Document() Erreur : on peut pas instanciée une class abstraite

print(calculer_total_frais([Livre()],5)) # Renvoie 2.5 euro de frais
print(calculer_total_frais([Magazine()],5)) # Renvoie 1.0 euro de frais
print(calculer_total_frais([DVD()],5)) # Renvoie 5.0 euro de frais
print(calculer_total_frais([Livre(),Magazine(),DVD()],5)) # Retourne 8.5 euro de frais
