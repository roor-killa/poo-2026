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