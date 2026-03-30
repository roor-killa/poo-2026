

## 📚 CM4 - Concepts avancés et bonnes pratiques (2h)

### Partie 1 : Design Patterns essentiels (1h)

**Pattern 1 : Singleton**
```python
class Bibliotheque:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, nom="Bibliothèque centrale"):
        if not hasattr(self, 'initialized'):
            self.nom = nom
            self.documents = []
            self.initialized = True

# Test
b1 = Bibliotheque("Biblio 1")
b2 = Bibliotheque("Biblio 2")
print(b1 is b2)  # True
```

**Pattern 2 : Factory**
```python
class DocumentFactory:
    @staticmethod
    def creer_document(type_doc, **kwargs):
        if type_doc == "livre":
            return Livre(kwargs['titre'], kwargs['auteur'], kwargs['isbn'])
        elif type_doc == "magazine":
            return Magazine(kwargs['titre'], kwargs['auteur'], kwargs['numero'])
        elif type_doc == "dvd":
            return DVD(kwargs['titre'], kwargs['realisateur'])
        else:
            raise ValueError(f"Type de document inconnu : {type_doc}")

# Utilisation
doc1 = DocumentFactory.creer_document("livre", titre="1984", auteur="Orwell", isbn="123")
doc2 = DocumentFactory.creer_document("magazine", titre="Science", auteur="Collectif", numero=42)
```

**Pattern 3 : Observer**
```python
class Observateur:
    def notifier(self, evenement):
        pass

class NotificationEmail(Observateur):
    def notifier(self, evenement):
        print(f"Email envoyé : {evenement}")

class NotificationSMS(Observateur):
    def notifier(self, evenement):
        print(f"SMS envoyé : {evenement}")

class Emprunt:
    def __init__(self):
        self.observateurs = []
    
    def ajouter_observateur(self, obs):
        self.observateurs.append(obs)
    
    def effectuer_emprunt(self, livre, utilisateur):
        # Logique d'emprunt
        livre.emprunter()
        # Notification
        for obs in self.observateurs:
            obs.notifier(f"{utilisateur} a emprunté {livre.titre}")

# Utilisation
emprunt = Emprunt()
emprunt.ajouter_observateur(NotificationEmail())
emprunt.ajouter_observateur(NotificationSMS())
```
