# CM5 - Principes SOLID (Partie 2)
## Synthèse, Exercices et Applications Pratiques

---

## 6. Synthèse des Principes SOLID

### Tableau Récapitulatif

| Principe | Acronyme | En bref | Bénéfice principal |
|----------|----------|---------|-------------------|
| **Single Responsibility** | **S** | Une classe = une responsabilité | Maintenabilité |
| **Open/Closed** | **O** | Ouvert extension, fermé modification | Évolutivité |
| **Liskov Substitution** | **L** | Sous-classes interchangeables | Polymorphisme sûr |
| **Interface Segregation** | **I** | Interfaces spécifiques | Découplage |
| **Dependency Inversion** | **D** | Dépendre des abstractions | Flexibilité |

### Interconnexions entre les Principes

```
     SRP ─────┐
              ├──→ Code modulaire
     ISP ─────┘

     OCP ─────┐
              ├──→ Extensibilité
     DIP ─────┘

     LSP ─────→ Polymorphisme correct

     Tous ────→ QUALITÉ LOGICIELLE
```

### SOLID et Design Patterns

| Pattern | Principes SOLID appliqués |
|---------|---------------------------|
| **Strategy** | OCP, DIP |
| **Observer** | OCP, DIP |
| **Decorator** | OCP, SRP |
| **Factory** | OCP, DIP |
| **Adapter** | LSP, ISP |
| **Facade** | SRP, ISP |
| **Command** | SRP, OCP |

---

## 7. Applications Pratiques - Refactoring

### Cas d'étude 1 : Système de Notification

#### ❌ Version initiale (viole plusieurs principes)

```python
class NotificationSystem:
    """
    ❌ Viole SRP, OCP, ISP
    """
    
    def send_notification(self, user_id, message, method):
        # Récupérer l'utilisateur
        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
        conn.close()
        
        # Envoyer selon la méthode
        if method == "email":
            import smtplib
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.send_message(user[2], message)
        elif method == "sms":
            import requests
            requests.post('https://sms-api.com/send', 
                         data={'phone': user[3], 'message': message})
        elif method == "push":
            import firebase
            firebase.send(user[1], message)
```

#### ✅ Version refactorisée (respecte SOLID)

```python
from abc import ABC, abstractmethod
from typing import Dict


# === SRP: Séparation des responsabilités ===

class User:
    """Représente un utilisateur"""
    
    def __init__(self, user_id: str, email: str, phone: str, device_token: str):
        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.device_token = device_token


class UserRepository:
    """Responsabilité: Persistance des utilisateurs"""
    
    def __init__(self, database):
        self.db = database
    
    def find_by_id(self, user_id: str) -> User:
        """Récupère un utilisateur"""
        # Logique de récupération
        pass


# === ISP: Interfaces ségrégées ===

class NotificationChannel(ABC):
    """Interface pour les canaux de notification"""
    
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Envoie une notification"""
        pass


# === OCP: Ouvert à l'extension ===

class EmailChannel(NotificationChannel):
    """Canal email"""
    
    def __init__(self, smtp_config: Dict):
        self.config = smtp_config
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"📧 Email envoyé à {recipient}: {message}")
        # import smtplib
        # Logique d'envoi
        return True


class SMSChannel(NotificationChannel):
    """Canal SMS"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"📱 SMS envoyé à {recipient}: {message}")
        # import requests
        # Logique d'envoi
        return True


class PushChannel(NotificationChannel):
    """Canal push notification"""
    
    def __init__(self, firebase_config: Dict):
        self.config = firebase_config
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"🔔 Push envoyé à {recipient}: {message}")
        # Logique Firebase
        return True


# Nouveau canal ajouté SANS modifier le code existant
class SlackChannel(NotificationChannel):
    """Canal Slack"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"💬 Slack envoyé à {recipient}: {message}")
        return True


# === DIP: Dépendance sur l'abstraction ===

class NotificationService:
    """
    Service de notification qui dépend de l'abstraction NotificationChannel
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.channels: Dict[str, NotificationChannel] = {}
    
    def register_channel(self, name: str, channel: NotificationChannel):
        """Enregistre un canal de notification"""
        self.channels[name] = channel
    
    def send_notification(self, user_id: str, message: str, channel_name: str) -> bool:
        """
        Envoie une notification via le canal spécifié
        """
        # Récupérer l'utilisateur
        user = self.user_repo.find_by_id(user_id)
        
        # Récupérer le canal
        if channel_name not in self.channels:
            raise ValueError(f"Canal inconnu: {channel_name}")
        
        channel = self.channels[channel_name]
        
        # Déterminer le destinataire selon le canal
        recipient_map = {
            'email': user.email,
            'sms': user.phone,
            'push': user.device_token,
            'slack': user.email  # ou username Slack
        }
        
        recipient = recipient_map.get(channel_name, user.email)
        
        # Envoyer
        return channel.send(recipient, message)
    
    def broadcast(self, user_id: str, message: str):
        """Envoie sur tous les canaux"""
        for channel_name in self.channels.keys():
            self.send_notification(user_id, message, channel_name)


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("REFACTORING AVEC SOLID - SYSTÈME DE NOTIFICATION")
    print("=" * 70)
    
    # Setup (normalement dans un fichier de config)
    from typing import Optional
    
    class MockUserRepository(UserRepository):
        def __init__(self):
            self.users = {
                "001": User("001", "alice@ua.fr", "0696123456", "device_abc")
            }
        
        def find_by_id(self, user_id: str) -> Optional[User]:
            return self.users.get(user_id)
    
    # Créer le service
    user_repo = MockUserRepository()
    notification_service = NotificationService(user_repo)
    
    # Enregistrer les canaux
    notification_service.register_channel("email", EmailChannel({}))
    notification_service.register_channel("sms", SMSChannel("api_key_123"))
    notification_service.register_channel("push", PushChannel({}))
    notification_service.register_channel("slack", SlackChannel("webhook_url"))
    
    # Envoyer des notifications
    print("\n--- Notifications individuelles ---")
    notification_service.send_notification("001", "Nouveau message!", "email")
    notification_service.send_notification("001", "Alerte urgente", "sms")
    
    print("\n--- Broadcast (tous les canaux) ---")
    notification_service.broadcast("001", "Maintenance prévue ce soir")
    
    print("\n" + "=" * 70)
    print("✅ Code respecte tous les principes SOLID")
    print("=" * 70)
```

---

### Cas d'étude 2 : Système de Rapports

```python
from abc import ABC, abstractmethod
from typing import List, Dict
import json


# === Données ===

class CourseData:
    """Données d'un cours"""
    
    def __init__(self, name: str, instructor: str, students: List[str], grades: Dict[str, float]):
        self.name = name
        self.instructor = instructor
        self.students = students
        self.grades = grades
    
    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)


# === SRP: Extraction de données séparée de la génération ===

class DataExtractor(ABC):
    """Interface pour extraire des données"""
    
    @abstractmethod
    def extract(self, course: CourseData) -> Dict:
        pass


class BasicDataExtractor(DataExtractor):
    """Extraction des données de base"""
    
    def extract(self, course: CourseData) -> Dict:
        return {
            'name': course.name,
            'instructor': course.instructor,
            'student_count': len(course.students),
            'average': course.get_average()
        }


class DetailedDataExtractor(DataExtractor):
    """Extraction détaillée avec toutes les notes"""
    
    def extract(self, course: CourseData) -> Dict:
        return {
            'name': course.name,
            'instructor': course.instructor,
            'students': course.students,
            'grades': course.grades,
            'average': course.get_average(),
            'max_grade': max(course.grades.values()) if course.grades else 0,
            'min_grade': min(course.grades.values()) if course.grades else 0
        }


# === OCP + Strategy: Formats de rapports ===

class ReportFormatter(ABC):
    """Interface pour formater les rapports"""
    
    @abstractmethod
    def format(self, data: Dict) -> str:
        pass


class TextFormatter(ReportFormatter):
    """Formatage texte"""
    
    def format(self, data: Dict) -> str:
        report = "=" * 50 + "\n"
        report += f"RAPPORT: {data['name']}\n"
        report += "=" * 50 + "\n"
        report += f"Enseignant: {data['instructor']}\n"
        report += f"Étudiants: {data['student_count']}\n"
        report += f"Moyenne: {data['average']:.2f}/20\n"
        report += "=" * 50
        return report


class JSONFormatter(ReportFormatter):
    """Formatage JSON"""
    
    def format(self, data: Dict) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatter(ReportFormatter):
    """Formatage HTML"""
    
    def format(self, data: Dict) -> str:
        html = f"""
        <div class="report">
            <h2>{data['name']}</h2>
            <p><strong>Enseignant:</strong> {data['instructor']}</p>
            <p><strong>Étudiants:</strong> {data['student_count']}</p>
            <p><strong>Moyenne:</strong> {data['average']:.2f}/20</p>
        </div>
        """
        return html


class MarkdownFormatter(ReportFormatter):
    """Formatage Markdown"""
    
    def format(self, data: Dict) -> str:
        md = f"# Rapport: {data['name']}\n\n"
        md += f"**Enseignant:** {data['instructor']}\n\n"
        md += f"**Étudiants:** {data['student_count']}\n\n"
        md += f"**Moyenne:** {data['average']:.2f}/20\n"
        return md


# === DIP: Service qui dépend des abstractions ===

class ReportGenerator:
    """
    Générateur de rapports flexible
    Respecte tous les principes SOLID
    """
    
    def __init__(self, extractor: DataExtractor, formatter: ReportFormatter):
        self.extractor = extractor
        self.formatter = formatter
    
    def generate(self, course: CourseData) -> str:
        """Génère un rapport"""
        # 1. Extraire les données
        data = self.extractor.extract(course)
        
        # 2. Formater
        report = self.formatter.format(data)
        
        return report
    
    def set_extractor(self, extractor: DataExtractor):
        """Change l'extracteur (OCP)"""
        self.extractor = extractor
    
    def set_formatter(self, formatter: ReportFormatter):
        """Change le formateur (OCP)"""
        self.formatter = formatter


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE RAPPORTS - SOLID")
    print("=" * 70)
    
    # Créer des données de cours
    course = CourseData(
        name="Programmation Orientée Objet",
        instructor="Prof. Roor",
        students=["Alice", "Bob", "Charlie", "Diana"],
        grades={
            "Alice": 16,
            "Bob": 14,
            "Charlie": 15,
            "Diana": 17
        }
    )
    
    # Rapport basique en texte
    print("\n--- Rapport Basique (Texte) ---")
    generator = ReportGenerator(
        BasicDataExtractor(),
        TextFormatter()
    )
    print(generator.generate(course))
    
    # Rapport détaillé en JSON
    print("\n--- Rapport Détaillé (JSON) ---")
    generator.set_extractor(DetailedDataExtractor())
    generator.set_formatter(JSONFormatter())
    print(generator.generate(course))
    
    # Rapport en Markdown
    print("\n--- Rapport (Markdown) ---")
    generator.set_formatter(MarkdownFormatter())
    print(generator.generate(course))
    
    print("\n" + "=" * 70)
    print("AVANTAGES:")
    print("- SRP: Extraction, formatage, génération séparés")
    print("- OCP: Nouveaux formats sans modifier le générateur")
    print("- DIP: Générateur dépend des abstractions")
    print("- Combinaisons infinies: extractor x formatter")
    print("=" * 70)
```

---

## 8. Exercices Pratiques

### Exercice 1 : Refactoring d'un système de paiement

**Code initial (viole SOLID) :**

```python
class PaymentSystem:
    def process_payment(self, amount, method, user_data):
        # Validation
        if amount <= 0:
            return False
        if not user_data.get('email'):
            return False
        
        # Traitement
        if method == "credit_card":
            # Code carte
            pass
        elif method == "paypal":
            # Code PayPal
            pass
        
        # Sauvegarde en base
        import sqlite3
        conn = sqlite3.connect('payments.db')
        # ...
        
        # Email de confirmation
        import smtplib
        # ...
        
        return True
```

**Consignes :**
1. Identifiez les violations de SOLID
2. Refactorisez en respectant tous les principes
3. Ajoutez 2 nouvelles méthodes de paiement sans modifier le code existant

---

### Exercice 2 : Système de validation

**Objectif :** Créer un système de validation flexible pour des formulaires.

**Exigences :**
- Valider différents types de champs (email, téléphone, date, etc.)
- Composer plusieurs validations (requis + format)
- Ajouter facilement de nouvelles règles de validation
- Messages d'erreur personnalisables

**Principes à appliquer :**
- SRP : Chaque validator une responsabilité
- OCP : Nouveaux validators sans modification
- ISP : Interfaces spécifiques
- DIP : Dépendre des abstractions

**Structure suggérée :**

```python
from abc import ABC, abstractmethod

class Validator(ABC):
    @abstractmethod
    def validate(self, value) -> tuple[bool, str]:
        """Returns (is_valid, error_message)"""
        pass

class EmailValidator(Validator):
    # À implémenter
    pass

class CompositeValidator(Validator):
    """Combine plusieurs validators"""
    # À implémenter
    pass

class FormValidator:
    """Valide un formulaire complet"""
    # À implémenter
    pass
```

---

### Exercice 3 : Système de logging

**Objectif :** Créer un système de logging flexible.

**Exigences :**
- Différents niveaux (DEBUG, INFO, WARNING, ERROR)
- Différentes destinations (console, fichier, database, remote)
- Formatage personnalisable
- Filtrage par niveau

**Consignes :**
1. Concevoir avec SOLID en tête
2. Utiliser les design patterns appropriés (Strategy, Decorator, Observer)
3. Permettre la configuration runtime

---

## 9. Anti-Patterns et Pièges Courants

### 9.1 Over-Engineering

```python
# ❌ Sur-ingénierie pour un cas simple
class SimpleName:
    pass

class SimpleNameFactory(ABC):
    @abstractmethod
    def create_name(self): pass

class ConcreteSimpleNameFactory(SimpleNameFactory):
    def create_name(self):
        return SimpleName()

class SimpleNameFactoryProvider:
    def get_factory(self):
        return ConcreteSimpleNameFactory()

# Pour créer un simple objet !
name = SimpleNameFactoryProvider().get_factory().create_name()

# ✅ KISS (Keep It Simple, Stupid)
name = SimpleName()  # C'est suffisant !
```

**Règle :** Appliquer SOLID quand c'est nécessaire, pas systématiquement.

### 9.2 Abstraction Prématurée

```python
# ❌ Créer des abstractions "au cas où"
class DataSource(ABC):  # Abstraction jamais utilisée
    @abstractmethod
    def get_data(self): pass

class MySQLDataSource(DataSource):  # Seule implémentation
    def get_data(self):
        return []

# ✅ Commencer simple, abstraire quand nécessaire
class DataSource:
    def get_data(self):
        return []

# Plus tard, si besoin d'une deuxième implémentation:
# 1. Créer l'interface
# 2. Refactorer l'existant
# 3. Ajouter la nouvelle implémentation
```

**Règle :** YAGNI (You Aren't Gonna Need It)

### 9.3 Interface Bloat

```python
# ❌ Interface trop grosse qui viole ISP
class Repository(ABC):
    @abstractmethod
    def find_all(self): pass
    
    @abstractmethod
    def find_by_id(self, id): pass
    
    @abstractmethod
    def save(self, entity): pass
    
    @abstractmethod
    def delete(self, id): pass
    
    @abstractmethod
    def count(self): pass
    
    @abstractmethod
    def exists(self, id): pass
    
    # ... 20 autres méthodes

# ReadOnlyRepository forcé d'implémenter save() et delete()
class ReadOnlyRepository(Repository):
    def save(self, entity):
        raise NotImplementedError("Read-only!")
    
    def delete(self, id):
        raise NotImplementedError("Read-only!")
```

---

## 10. SOLID dans le Monde Réel

### 10.1 Frameworks Populaires

**Django (Python Web Framework)**
- **SRP** : Models, Views, Forms séparés
- **OCP** : Middleware extensible
- **DIP** : Settings injectables

**Flask (Python Web Framework)**
- **OCP** : Blueprints
- **DIP** : Extensions

**React (JavaScript)**
- **SRP** : Composants à responsabilité unique
- **OCP** : Higher-Order Components
- **ISP** : Props spécifiques

### 10.2 Architecture Logicielle

**Clean Architecture (Uncle Bob)**

```
┌─────────────────────────────────────┐
│     Frameworks & Drivers            │
│  (Web, DB, UI, External Interfaces) │
├─────────────────────────────────────┤
│     Interface Adapters              │
│  (Controllers, Gateways, Presenters)│
├─────────────────────────────────────┤
│     Use Cases                       │
│  (Application Business Rules)       │
├─────────────────────────────────────┤
│     Entities                        │
│  (Enterprise Business Rules)        │
└─────────────────────────────────────┘

Dépendances : Extérieur → Intérieur (DIP)
```

**Hexagonal Architecture (Ports & Adapters)**
- **DIP** : Dépendance sur les ports (interfaces)
- **OCP** : Nouveaux adapters sans modifier le core

---

## 11. Checklist SOLID pour Code Review

### Avant de merger du code, vérifiez :

**Single Responsibility**
- [ ] Chaque classe a-t-elle UNE seule raison de changer ?
- [ ] Peut-on décrire la classe en une phrase sans "et" ?
- [ ] La classe a-t-elle moins de 200 lignes ?

**Open/Closed**
- [ ] Peut-on étendre sans modifier ?
- [ ] Y a-t-il trop de if/else ou switch ?
- [ ] Utilise-t-on le polymorphisme ?

**Liskov Substitution**
- [ ] Les sous-classes respectent-elles le contrat de la classe de base ?
- [ ] Pas d'exceptions inattendues dans les sous-classes ?
- [ ] Le polymorphisme fonctionne-t-il correctement ?

**Interface Segregation**
- [ ] Les interfaces sont-elles spécifiques ?
- [ ] Y a-t-il des méthodes NotImplementedError ?
- [ ] Les clients utilisent-ils toutes les méthodes ?

**Dependency Inversion**
- [ ] Dépend-on des abstractions ?
- [ ] Utilise-t-on l'injection de dépendances ?
- [ ] Le code est-il testable sans mocks complexes ?

---

## 12. Conclusion

### Ce que nous avons appris

✅ **Les 5 principes SOLID** en profondeur  
✅ **Violations courantes** et comment les corriger  
✅ **Applications pratiques** avec refactoring  
✅ **Liens avec les design patterns**  
✅ **Anti-patterns** à éviter  

### Principes clés à retenir

1. **SOLID n'est pas dogmatique** : Utilisez avec jugement
2. **Commencez simple** : Refactorez vers SOLID quand nécessaire
3. **La maintenabilité avant tout** : SOLID sert ce but
4. **Testabilité** : Code SOLID = code testable
5. **Évolutivité** : Anticiper le changement sans sur-ingénierie

### Règles d'Or

**KISS** - Keep It Simple, Stupid  
**YAGNI** - You Aren't Gonna Need It  
**DRY** - Don't Repeat Yourself  
**SOLID** - Pour la qualité et la maintenabilité  

### La Pyramide de la Qualité

```
         Fonctionne
            ↑
         Maintenable (SOLID)
            ↑
         Testable
            ↑
         Compréhensible
            ↑
         Simple
```

---

## 13. Pour Aller Plus Loin

### Livres Recommandés

- **"Clean Code"** - Robert C. Martin  
  Les fondations de la qualité logicielle

- **"Clean Architecture"** - Robert C. Martin  
  Architecture et principes SOLID

- **"Refactoring"** - Martin Fowler  
  Améliorer le code existant

- **"Design Patterns"** - Gang of Four  
  Patterns classiques

### Ressources en Ligne

- **Refactoring.Guru** - Excellentes illustrations
- **SOLID Principles (Uncle Bob)** - Articles originaux
- **Python Design Patterns** - Implémentations Python

### Pratique

- **Code Katas** : Exercices de refactoring
- **Open Source** : Lire du code de qualité
- **Code Review** : Appliquer SOLID dans vos projets

---

## 14. Projet Final

### Système de Gestion de Bibliothèque

**Objectif :** Concevoir et implémenter un système complet en respectant SOLID.

**Fonctionnalités :**
1. Gestion des livres (ajout, recherche, emprunt, retour)
2. Gestion des membres (inscription, historique)
3. Système de pénalités (retards)
4. Notifications (email, SMS)
5. Rapports (statistiques, inventaire)
6. Différentes sources de données (SQLite, PostgreSQL, JSON)

**Contraintes :**
- Respecter tous les principes SOLID
- Utiliser au moins 5 design patterns
- Code 100% testé
- Documentation complète

**Livrables :**
1. Diagramme UML de classes
2. Code source avec commentaires
3. Tests unitaires
4. README avec justification des choix architecturaux

**Critères d'évaluation :**
- Respect de SOLID (40%)
- Qualité du code (30%)
- Tests (20%)
- Documentation (10%)

---

## 15. Quiz Final

### Questions Théoriques

1. **SRP :** Donnez 3 exemples de violations du SRP dans du code réel
2. **OCP :** Comment Strategy Pattern applique-t-il l'OCP ?
3. **LSP :** Expliquez pourquoi Square héritant de Rectangle viole le LSP
4. **ISP :** Quelle est la différence entre ISP et SRP ?
5. **DIP :** Qu'est-ce que l'injection de dépendances ?

### Questions Pratiques

**Identifiez les violations :**

```python
class UserManager:
    def create_user(self, data):
        # Validation
        if not data.get('email'):
            return False
        
        # Hash password
        import hashlib
        password = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Save to DB
        import sqlite3
        conn = sqlite3.connect('users.db')
        # ...
        
        # Send email
        import smtplib
        # ...
        
        # Log
        print(f"User created: {data['email']}")
        
        return True
```

**Quels principes sont violés ? Comment corriger ?**

---

## 16. Prochains Cours

**CM6 : Architecture Logicielle**
- Clean Architecture
- Hexagonal Architecture
- Domain-Driven Design
- Microservices

**CM7 : Tests et Qualité**
- Tests unitaires
- TDD (Test-Driven Development)
- Mocking et Dependency Injection
- Code Coverage

**CM8 : Patterns Avancés**
- CQRS (Command Query Responsibility Segregation)
- Event Sourcing
- Repository Pattern
- Unit of Work

---

## Conclusion Finale

Les principes SOLID ne sont pas des règles strictes, mais des **guidelines** pour créer du code de qualité. Utilisez votre jugement :

- ✅ Appliquez SOLID quand ça améliore la maintenabilité
- ❌ N'appliquez pas SOLID aveuglément
- ✅ Refactorez vers SOLID progressivement
- ❌ Ne faites pas de sur-ingénierie

**Objectif final :** Code **simple**, **maintenable**, et **évolutif**.

---

## Questions ?

Merci pour votre attention !

**Contact :** roland.ratenan@nasdy.fr  
**Office Hours :** 9h-17h

---

*Fin du CM5 - Principes SOLID*