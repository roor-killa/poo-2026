from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass

class Livre(Document):
    def calculer_frais_retard(self, jours):
        return jours * 0.50  # 0.50€ par jour

class Magazine(Document):
    def calculer_frais_retard(self, jours):
        return jours * 0.20  # 0.20€ par jour

class DVD(Document):
    def calculer_frais_retard(self, jours):
        return jours * 1.00  # 1€ par jour

def calculer_total_frais(documents, jours):
    total = 0
    for doc in documents:
        total += doc.calculer_frais_retard(jours)
    return total

#test

# Création des documents
livre = Livre()
magazine = Magazine()
dvd = DVD()

# Test individuel du calcul des frais de retard
print("Frais livre (5 jours) :", livre.calculer_frais_retard(5), "€")
print("Frais magazine (5 jours) :", magazine.calculer_frais_retard(5), "€")
print("Frais DVD (5 jours) :", dvd.calculer_frais_retard(5), "€")

print("\n---\n")

# Test du polymorphisme avec une liste de documents
documents = [livre, magazine, dvd]

# Calcul du total des frais pour 5 jours de retard
total = calculer_total_frais(documents, 5)
print("Total des frais de retard (5 jours) :", total, "€")

print("\n---\n")

# Tentative d'instanciation de la classe abstraite (doit échouer)
try:
    doc = Document()
except TypeError as e:
    print("Erreur :", e)