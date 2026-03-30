# Travaux Dirigés - Programmation Orientée Objet (8h)
## Licence 2 - S4 - Python

---

## 📋 Informations générales

**Volume horaire** : 8h de TD
**Organisation** : 4 séances de 2h
**Modalités** : Travail en binôme ou trinôme
**Rendu** : Code commenté + réponses aux questions
**Évaluation** : Participation + justesse des solutions

**⚠️ Règle importante : IA autorisée**
- Vous POUVEZ utiliser ChatGPT, Claude, Copilot, etc.
- MAIS vous devez expliquer chaque ligne de code que vous utilisez
- Des questions orales seront posées pour vérifier votre compréhension
- Le code sans explication = 0 point

---

## 📚 TD3 - Polymorphisme et design patterns (2h)

### 🎯 Objectifs
- Appliquer le polymorphisme
- Implémenter des design patterns de base
- Utiliser les classes abstraites

### Exercice 7 : Système de notification (40min)

**Contexte** : Envoyer des notifications de différentes manières.

**Cahier des charges :**

1. Créez une classe abstraite `Notification` avec :
   - Méthode abstraite `envoyer(message, destinataire)`
   - Méthode `formater_message(message)` (commune à tous)

2. Créez les implémentations :
   - `NotificationEmail` : simule l'envoi d'un email
   - `NotificationSMS` : simule l'envoi d'un SMS
   - `NotificationPush` : simule une notification mobile

3. Créez une classe `GestionnaireNotifications` avec :
   - Liste de notifications
   - Méthode `ajouter_canal(notification)`
   - Méthode `notifier_tous(message, destinataire)` qui envoie via tous les canaux

**Code squelette :**
```python
from abc import ABC, abstractmethod

class Notification(ABC):
    def formater_message(self, message):
        return f"[{self.__class__.__name__}] {message}"
    
    @abstractmethod
    def envoyer(self, message, destinataire):
        pass

class NotificationEmail(Notification):
    def envoyer(self, message, destinataire):
        # TODO : Implémenter
        pass

# TODO : Compléter les autres classes
```

**Questions :**
- Q1 : C'est quoi le polymorphisme dans cet exercice ?
- Q2 : Pourquoi `Notification` doit-elle être abstraite ?
- Q3 : Comment ajouter un nouveau canal sans modifier le code existant ?

**Test :**
```python
gestionnaire = GestionnaireNotifications()
gestionnaire.ajouter_canal(NotificationEmail())
gestionnaire.ajouter_canal(NotificationSMS())
gestionnaire.ajouter_canal(NotificationPush())

gestionnaire.notifier_tous("Votre livre est disponible", "marie@example.com")
```

---

### Exercice 8 : Factory Pattern (40min)

**Contexte** : Créer différents types de documents sans connaître les détails.

**Cahier des charges :**

1. Créez les classes de documents :
   - `Livre` : titre, auteur, isbn, nb_pages
   - `Magazine` : titre, editeur, numero, mois
   - `DVD` : titre, realisateur, duree
   - `EBook` : titre, auteur, format, taille_mo

2. Créez une `FabriqueDocument` avec :
   - Méthode statique `creer(type_doc, **kwargs)`
   - Gestion des erreurs si type inconnu

3. Testez avec un système qui lit des données depuis un dictionnaire

**Code squelette :**
```python
class FabriqueDocument:
    @staticmethod
    def creer(type_doc, **kwargs):
        if type_doc == "livre":
            return Livre(**kwargs)
        elif type_doc == "magazine":
            return Magazine(**kwargs)
        # TODO : Compléter
        else:
            raise ValueError(f"Type de document inconnu : {type_doc}")

# Utilisation avec des données
donnees = [
    {"type": "livre", "titre": "1984", "auteur": "Orwell", "isbn": "123", "nb_pages": 328},
    {"type": "magazine", "titre": "Science", "editeur": "Nature", "numero": 42, "mois": "Janvier"},
    {"type": "dvd", "titre": "Matrix", "realisateur": "Wachowski", "duree": 136}
]

documents = []
for data in donnees:
    type_doc = data.pop("type")
    doc = FabriqueDocument.creer(type_doc, **data)
    documents.append(doc)
```

**Questions :**
- Q1 : Quel est l'avantage du pattern Factory ?
- Q2 : Comment ajouter un nouveau type de document ?
- Q3 : Peut-on utiliser un dictionnaire au lieu de if/elif ?

**Challenge :**
Implémentez une version avec un dictionnaire de mapping :
```python
class FabriqueDocument:
    _types = {
        "livre": Livre,
        "magazine": Magazine,
        # ...
    }
    
    @classmethod
    def creer(cls, type_doc, **kwargs):
        # TODO : Utiliser _types au lieu de if/elif
        pass
```

---

### Exercice 9 : Observer Pattern (40min)

**Contexte** : Notifier automatiquement quand un livre est rendu.

**Cahier des charges :**

1. Créez une classe `Observateur` (interface) avec :
   - Méthode `update(evenement)`

2. Créez des observateurs concrets :
   - `JournalEvenements` : écrit dans un fichier log
   - `StatistiquesEmprunts` : compte les emprunts/retours
   - `NotificateurUtilisateurs` : prévient les utilisateurs en attente

3. Créez une classe `Document` observable avec :
   - Liste d'observateurs
   - Méthodes `ajouter_observateur()`, `retirer_observateur()`
   - Méthode `notifier_observateurs(evenement)`
   - Méthodes `emprunter()` et `retourner()` qui notifient

**Code squelette :**
```python
class Observateur(ABC):
    @abstractmethod
    def update(self, evenement):
        pass

class JournalEvenements(Observateur):
    def __init__(self):
        self.journal = []
    
    def update(self, evenement):
        self.journal.append(evenement)
        print(f"[LOG] {evenement}")

class DocumentObservable:
    def __init__(self, titre):
        self.titre = titre
        self._observateurs = []
    
    def ajouter_observateur(self, obs):
        self._observateurs.append(obs)
    
    def notifier_observateurs(self, evenement):
        for obs in self._observateurs:
            obs.update(evenement)
    
    def emprunter(self, utilisateur):
        # TODO : Logique d'emprunt + notification
        pass
```

**Questions :**
- Q1 : Quelle est la différence avec le pattern Strategy ?
- Q2 : Pourquoi utiliser une liste d'observateurs ?
- Q3 : Comment éviter les références circulaires ?

---