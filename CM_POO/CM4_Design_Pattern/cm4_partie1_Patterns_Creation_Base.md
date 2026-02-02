# CM4 - Design Patterns (Partie 1)
## Programmation Orientée Objet

---

## Objectifs du cours

À la fin de cette partie, vous serez capable de :
- Comprendre ce qu'est un design pattern et pourquoi l'utiliser
- Identifier les situations où appliquer des patterns
- Implémenter les patterns de création fondamentaux
- Reconnaître les anti-patterns à éviter

---

## 1. Introduction aux Design Patterns

### 1.1 Qu'est-ce qu'un Design Pattern ?

Un **design pattern** (ou patron de conception) est une solution réutilisable à un problème récurrent dans la conception logicielle. Ce n'est pas du code prêt à l'emploi, mais plutôt un **modèle** ou une **recette** pour résoudre un type de problème.

**Analogie concrète** : Tout comme une recette de cuisine donne des instructions pour préparer un plat (sans être le plat lui-même), un design pattern donne une structure pour résoudre un problème (sans être le code final).

### 1.2 Pourquoi utiliser des Design Patterns ?

**1. Communication efficace**
```python
# Au lieu de dire : "J'ai fait une classe qui gère une seule instance..."
# On dit simplement : "J'ai utilisé un Singleton"
```

**2. Solutions éprouvées**
- Évite de réinventer la roue
- Réduit les bugs potentiels
- Accélère le développement

**3. Code maintenable**
- Structure claire et prévisible
- Facilite les modifications futures
- Améliore la collaboration en équipe

**4. Évolutivité**
- Facilite l'ajout de nouvelles fonctionnalités
- Réduit l'impact des changements

### 1.3 Les trois catégories de patterns

Les design patterns sont classés en trois grandes familles :

#### 🏗️ **Patterns de Création** (Creational Patterns)
Concernent la **création d'objets** de manière flexible et réutilisable.
- Singleton
- Factory Method
- Abstract Factory
- Builder
- Prototype

#### 🔧 **Patterns de Structure** (Structural Patterns)
Concernent l'**organisation des classes et objets** pour former des structures plus complexes.
- Adapter
- Decorator
- Facade
- Composite
- Proxy

#### ⚡ **Patterns de Comportement** (Behavioral Patterns)
Concernent la **communication entre objets** et la répartition des responsabilités.
- Observer
- Strategy
- Command
- State
- Template Method

---

## 2. Les Patterns de Création

Dans cette première partie, nous allons étudier les patterns de création les plus fondamentaux.

### 2.1 Le Pattern Singleton

#### Problème à résoudre

Imaginez que vous développez une application pour gérer les ressources d'un campus universitaire. Vous avez besoin d'une classe `Configuration` qui charge les paramètres de l'application (base de données, API keys, etc.).

**Problème** : Si plusieurs parties du code créent des instances de `Configuration`, vous aurez :
- Plusieurs lectures du fichier de configuration (ralentissement)
- Incohérences possibles si les valeurs changent
- Gaspillage de mémoire

**Solution** : Garantir qu'une seule instance de la classe existe dans toute l'application.

#### Structure du Singleton

```python
class Singleton:
    """
    Pattern Singleton classique
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

#### Exemple concret : Gestionnaire de Configuration

```python
class ConfigurationManager:
    """
    Gestionnaire de configuration pour l'application campus
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Éviter la réinitialisation à chaque appel
        if not ConfigurationManager._initialized:
            self.config = {}
            self.load_config()
            ConfigurationManager._initialized = True
    
    def load_config(self):
        """Charge la configuration depuis un fichier"""
        self.config = {
            'db_host': 'localhost',
            'db_port': 5432,
            'api_key': 'secret_key_123',
            'max_connections': 100
        }
        print("Configuration chargée")
    
    def get(self, key):
        """Récupère une valeur de configuration"""
        return self.config.get(key)
    
    def set(self, key, value):
        """Modifie une valeur de configuration"""
        self.config[key] = value


# Utilisation
if __name__ == "__main__":
    # Première instance
    config1 = ConfigurationManager()
    print(f"DB Host: {config1.get('db_host')}")
    
    # Deuxième "instance" - en réalité, c'est la même !
    config2 = ConfigurationManager()
    
    # Vérification
    print(f"config1 est config2 ? {config1 is config2}")  # True
    
    # Modification via config2
    config2.set('db_host', 'production-server')
    
    # La modification est visible via config1
    print(f"DB Host via config1: {config1.get('db_host')}")  # production-server
```

**Sortie** :
```
Configuration chargée
DB Host: localhost
config1 est config2 ? True
DB Host via config1: production-server
```

#### Variante : Singleton avec décorateur (Pythonic)

```python
def singleton(cls):
    """
    Décorateur pour transformer une classe en Singleton
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class DatabaseConnection:
    """
    Connexion unique à la base de données
    """
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        print("Connexion à la base de données établie")
        self.connection = "Connection Object"
    
    def query(self, sql):
        return f"Exécution de : {sql}"


# Utilisation
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"db1 is db2 ? {db1 is db2}")  # True
print(db1.query("SELECT * FROM students"))
```

#### ⚠️ Quand utiliser le Singleton ?

**✅ Utilisez-le pour :**
- Gestionnaires de configuration
- Connexions à la base de données (pool de connexions)
- Gestionnaires de logs
- Gestionnaires de cache
- Services partagés globalement

**❌ Évitez-le pour :**
- Tout ce qui nécessite plusieurs instances
- Classes avec état modifiable par plusieurs composants (risque de bugs)
- Tests unitaires (difficile à mocker)

---

### 2.2 Le Pattern Factory Method

#### Problème à résoudre

Vous développez un système de gestion d'événements pour le campus. Vous avez différents types d'événements (conférences, ateliers, compétitions sportives), chacun avec des comportements spécifiques.

**Problème** : Comment créer le bon type d'événement sans avoir à connaître les détails de chaque classe ?

**Mauvaise approche** :
```python
# Code difficile à maintenir
if event_type == "conference":
    event = Conference(title, date, speaker)
elif event_type == "workshop":
    event = Workshop(title, date, max_participants)
elif event_type == "sport":
    event = SportEvent(title, date, sport_type)
# ... et si on ajoute un nouveau type ?
```

**Solution** : Déléguer la création d'objets à des méthodes factory.

#### Structure du Factory Method

```python
from abc import ABC, abstractmethod


class Event(ABC):
    """Classe abstraite pour tous les événements"""
    
    def __init__(self, title, date):
        self.title = title
        self.date = date
    
    @abstractmethod
    def get_description(self):
        """Retourne une description de l'événement"""
        pass
    
    @abstractmethod
    def get_duration(self):
        """Retourne la durée de l'événement"""
        pass


class Conference(Event):
    """Événement de type conférence"""
    
    def __init__(self, title, date, speaker, topic):
        super().__init__(title, date)
        self.speaker = speaker
        self.topic = topic
    
    def get_description(self):
        return f"Conférence: {self.title} par {self.speaker} sur {self.topic}"
    
    def get_duration(self):
        return "2 heures"


class Workshop(Event):
    """Événement de type atelier pratique"""
    
    def __init__(self, title, date, max_participants, materials):
        super().__init__(title, date)
        self.max_participants = max_participants
        self.materials = materials
    
    def get_description(self):
        return f"Atelier: {self.title} (max {self.max_participants} participants)"
    
    def get_duration(self):
        return "3 heures"


class SportEvent(Event):
    """Événement sportif"""
    
    def __init__(self, title, date, sport_type, teams):
        super().__init__(title, date)
        self.sport_type = sport_type
        self.teams = teams
    
    def get_description(self):
        return f"Compétition de {self.sport_type}: {self.title}"
    
    def get_duration(self):
        return "Variable selon le sport"


class EventFactory:
    """
    Factory pour créer des événements
    """
    
    @staticmethod
    def create_event(event_type, **kwargs):
        """
        Crée un événement selon son type
        
        Args:
            event_type: Type d'événement ('conference', 'workshop', 'sport')
            **kwargs: Paramètres spécifiques à chaque type
        
        Returns:
            Instance de Event
        """
        event_types = {
            'conference': Conference,
            'workshop': Workshop,
            'sport': SportEvent
        }
        
        event_class = event_types.get(event_type)
        
        if event_class is None:
            raise ValueError(f"Type d'événement inconnu: {event_type}")
        
        return event_class(**kwargs)


# Utilisation
if __name__ == "__main__":
    factory = EventFactory()
    
    # Créer une conférence
    conf = factory.create_event(
        'conference',
        title="Intelligence Artificielle et Éducation",
        date="2025-03-15",
        speaker="Dr. Dupont",
        topic="IA dans l'enseignement"
    )
    
    # Créer un atelier
    workshop = factory.create_event(
        'workshop',
        title="Développement Web avec Laravel",
        date="2025-03-20",
        max_participants=25,
        materials=["Ordinateur", "Connexion Internet"]
    )
    
    # Créer un événement sportif
    sport = factory.create_event(
        'sport',
        title="Tournoi Inter-Universités",
        date="2025-04-10",
        sport_type="Football",
        teams=["UA", "UG", "UAG"]
    )
    
    # Afficher les événements
    events = [conf, workshop, sport]
    for event in events:
        print(f"{event.get_description()}")
        print(f"Durée: {event.get_duration()}")
        print("-" * 50)
```

**Sortie** :
```
Conférence: Intelligence Artificielle et Éducation par Dr. Dupont sur IA dans l'enseignement
Durée: 2 heures
--------------------------------------------------
Atelier: Développement Web avec Laravel (max 25 participants)
Durée: 3 heures
--------------------------------------------------
Compétition de Football: Tournoi Inter-Universités
Durée: Variable selon le sport
--------------------------------------------------
```

#### Variante avancée : Factory avec enregistrement dynamique

```python
class EventRegistry:
    """
    Registry pattern combiné avec Factory
    Permet d'enregistrer dynamiquement de nouveaux types d'événements
    """
    _event_types = {}
    
    @classmethod
    def register(cls, event_type_name):
        """Décorateur pour enregistrer un type d'événement"""
        def decorator(event_class):
            cls._event_types[event_type_name] = event_class
            return event_class
        return decorator
    
    @classmethod
    def create(cls, event_type, **kwargs):
        """Crée un événement enregistré"""
        event_class = cls._event_types.get(event_type)
        if event_class is None:
            raise ValueError(f"Type non enregistré: {event_type}")
        return event_class(**kwargs)
    
    @classmethod
    def list_types(cls):
        """Liste tous les types d'événements disponibles"""
        return list(cls._event_types.keys())


# Utilisation avec le décorateur
@EventRegistry.register('conference')
class Conference(Event):
    # ... (même implémentation)
    pass

@EventRegistry.register('workshop')
class Workshop(Event):
    # ... (même implémentation)
    pass

# Créer un événement
event = EventRegistry.create('conference', title="...", date="...", ...)

# Lister les types disponibles
print(EventRegistry.list_types())  # ['conference', 'workshop']
```

#### ⚠️ Quand utiliser Factory Method ?

**✅ Utilisez-le pour :**
- Créer des objets dont le type exact n'est connu qu'à l'exécution
- Centraliser la logique de création complexe
- Faciliter l'ajout de nouveaux types sans modifier le code existant
- Encapsuler les dépendances de création

**❌ Évitez-le pour :**
- Création simple d'objets (surcharge inutile)
- Quand vous avez seulement 1-2 types d'objets

---

## 3. Exercices pratiques

### Exercice 1 : Singleton - Gestionnaire de Session

Créez un gestionnaire de session utilisateur pour une application campus qui :
- Stocke l'utilisateur connecté
- Garde trace de l'heure de connexion
- Permet de vérifier si la session est active (max 2 heures)
- Garantit qu'une seule session existe

```python
# À compléter
class SessionManager:
    # Votre code ici
    pass
```

### Exercice 2 : Factory Method - Système de Notifications

Créez un système de notifications qui peut envoyer des messages via différents canaux :
- Email
- SMS
- Push notification (mobile)

Chaque type de notification a des paramètres spécifiques et une méthode `send()`.

```python
# À compléter
class NotificationFactory:
    # Votre code ici
    pass
```

### Exercice 3 : Combinaison - Logger avec Factory

Créez un système de logging qui :
- Utilise Singleton pour avoir une instance unique du logger
- Utilise Factory pour créer différents types de handlers (console, fichier, remote)
- Permet de logger à différents niveaux (DEBUG, INFO, WARNING, ERROR)

---

## 4. Anti-Patterns à éviter

### 4.1 Le God Object (Objet Dieu)

**Problème** : Une classe qui fait tout.

```python
# ❌ Mauvais
class Application:
    def connect_database(self): pass
    def send_email(self): pass
    def process_payment(self): pass
    def generate_report(self): pass
    def manage_users(self): pass
    # ... 50 autres méthodes
```

**Solution** : Séparer les responsabilités (principe SRP - Single Responsibility Principle).

### 4.2 Singleton Abuse

**Problème** : Utiliser Singleton partout par facilité.

```python
# ❌ Mauvais - Singleton inutile
@singleton
class Student:  # Pourquoi une seule instance d'étudiant ?!
    pass
```

**Solution** : N'utiliser Singleton que quand c'est vraiment nécessaire.

---

## 5. Résumé de la Partie 1

### Ce que nous avons vu

1. **Les Design Patterns** sont des solutions réutilisables à des problèmes récurrents
2. **Trois catégories** : Création, Structure, Comportement
3. **Singleton** : Une seule instance dans toute l'application
4. **Factory Method** : Déléguer la création d'objets à des méthodes dédiées

### Principes clés à retenir

- Un pattern n'est pas du code, c'est un modèle
- Choisir le bon pattern selon le problème
- Ne pas sur-utiliser les patterns (KISS - Keep It Simple, Stupid)
- Les patterns facilitent la communication entre développeurs

### Dans la partie 2, nous verrons :

- Builder Pattern (construction d'objets complexes)
- Prototype Pattern (clonage d'objets)
- Abstract Factory (familles d'objets)
- Patterns de structure (Adapter, Decorator, Facade)

---

## 6. Ressources complémentaires

**Livres recommandés :**
- "Design Patterns" (Gang of Four) - Le livre de référence
- "Head First Design Patterns" - Approche visuelle et ludique
- "Python Design Patterns" - Spécifique à Python

**Sites web :**
- [Refactoring.Guru](https://refactoring.guru/design-patterns) - Excellentes illustrations
- [Python Patterns](https://python-patterns.guide/) - Patterns en Python

---

## Questions ?

N'hésitez pas à poser vos questions sur :
- L'utilisation pratique des patterns
- Les cas d'usage spécifiques
- L'implémentation en Python
- Les différences avec d'autres langages

**Prochaine séance** : CM4 Partie 2 - Suite des patterns de création et introduction aux patterns de structure.