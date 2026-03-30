

## 📚 CM4 - Concepts avancés et bonnes pratiques (2h)

### Partie 2 : Principes SOLID (45min)

**S - Single Responsibility**
```python
# ❌ Mauvais : trop de responsabilités
class Livre:
    def sauvegarder_bd(self):
        pass  # Sauvegarde en base
    def envoyer_email(self):
        pass  # Envoie un email
    def generer_pdf(self):
        pass  # Génère un PDF

# ✅ Bon : responsabilités séparées
class Livre:
    def __init__(self, titre):
        self.titre = titre

class DepotLivre:
    def sauvegarder(self, livre):
        pass  # Sauvegarde en base

class ServiceNotification:
    def envoyer_email(self, livre):
        pass

class GenerateurRapport:
    def generer_pdf(self, livre):
        pass
```

**O - Open/Closed**
```python
# ✅ Ouvert à l'extension, fermé à la modification
class CalculateurFrais:
    def calculer(self, document, jours):
        return document.calculer_frais_retard(jours)

# On peut ajouter de nouveaux types de documents sans modifier CalculateurFrais
```

**L - Liskov Substitution**
```python
# ✅ Les sous-classes doivent pouvoir remplacer leurs classes parentes
def traiter_document(doc: Document):
    doc.emprunter()
    print(doc.calculer_duree_max_emprunt())

# Fonctionne avec n'importe quelle sous-classe de Document
traiter_document(Livre("1984", "Orwell"))
traiter_document(Magazine("Science", "Collectif", 42))
```

**I - Interface Segregation**
```python
# ✅ Interfaces spécifiques plutôt qu'une interface générale
class Empruntable(ABC):
    @abstractmethod
    def emprunter(self):
        pass

class Reservable(ABC):
    @abstractmethod
    def reserver(self):
        pass

# Un document peut implémenter seulement ce dont il a besoin
```

**D - Dependency Inversion**
```python
# ✅ Dépendre d'abstractions, pas de concrétions
class ServiceEmprunt:
    def __init__(self, depot: DepotDocument):  # Dépend de l'abstraction
        self.depot = depot
    
    def emprunter(self, doc):
        # ...
        self.depot.sauvegarder(doc)
```

### Partie 3 : Tests et qualité (15min)

**Introduction aux tests unitaires**
```python
import unittest

class TestLivre(unittest.TestCase):
    def setUp(self):
        self.livre = Livre("1984", "Orwell", "123")
    
    def test_emprunt_disponible(self):
        self.assertTrue(self.livre.emprunter())
        self.assertFalse(self.livre.disponible)
    
    def test_emprunt_indisponible(self):
        self.livre.emprunter()
        self.assertFalse(self.livre.emprunter())
    
    def test_retour(self):
        self.livre.emprunter()
        self.livre.retourner()
        self.assertTrue(self.livre.disponible)
```

**Discussion : IA et tests**
- L'IA peut générer des tests, mais il faut vérifier la pertinence
- Importance des tests pour valider le code généré par IA

---
