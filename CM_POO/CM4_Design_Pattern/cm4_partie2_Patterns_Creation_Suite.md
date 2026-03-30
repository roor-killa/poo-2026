# CM4 - Design Patterns (Partie 2)
## Programmation Orientée Objet

---

## Rappel de la Partie 1

Dans la partie précédente, nous avons étudié :
- ✅ Les fondamentaux des design patterns
- ✅ **Singleton** : Une seule instance globale
- ✅ **Factory Method** : Délégation de la création d'objets

Nous allons voir :
- **Builder** : Construction d'objets complexes étape par étape
- **Prototype** : Clonage d'objets
- **Abstract Factory** : Familles d'objets liés
- **Adapter** : Rendre compatibles des interfaces différentes
- **Decorator** : Ajouter des fonctionnalités dynamiquement
- **Facade** : Simplifier une interface complexe

---

## 1. Patterns de Création (Suite)

### 1.1 Le Pattern Builder

#### Problème à résoudre

Vous développez un système d'inscription pour les cours du campus. Chaque étudiant a de nombreux attributs optionnels : adresse, téléphone, photo, situation médicale, bourses, préférences, etc.

**Problème** : Le constructeur devient ingérable avec trop de paramètres.

```python
# ❌ Approche problématique
class Student:
    def __init__(self, first_name, last_name, email, phone=None, 
                 address=None, city=None, postal_code=None,
                 birth_date=None, photo=None, emergency_contact=None,
                 scholarship=None, dietary_restrictions=None,
                 medical_info=None, preferred_language=None):
        # Constructeur cauchemardesque !
        pass

# Utilisation confuse
student = Student("Jean", "Dupont", "jean@example.com", 
                 None, None, None, None, "1995-05-15", None, None, 
                 True, ["végétarien"], None, "fr")
# Quel paramètre correspond à quoi ?!
```

**Solution** : Construire l'objet étape par étape avec un Builder.

#### Structure du Builder

```python
class Student:
    """
    Classe Student avec de nombreux attributs
    """
    def __init__(self):
        # Attributs obligatoires (définis après)
        self.first_name = None
        self.last_name = None
        self.email = None
        
        # Attributs optionnels
        self.phone = None
        self.address = None
        self.city = None
        self.postal_code = None
        self.birth_date = None
        self.photo_url = None
        self.emergency_contact = None
        self.has_scholarship = False
        self.dietary_restrictions = []
        self.medical_info = None
        self.preferred_language = "fr"
    
    def __str__(self):
        return (f"Student: {self.first_name} {self.last_name} "
                f"({self.email})")
    
    def get_full_info(self):
        """Retourne toutes les informations de l'étudiant"""
        info = [
            f"Nom: {self.first_name} {self.last_name}",
            f"Email: {self.email}",
        ]
        
        if self.phone:
            info.append(f"Téléphone: {self.phone}")
        if self.city:
            info.append(f"Ville: {self.city}")
        if self.has_scholarship:
            info.append("Boursier: Oui")
        if self.dietary_restrictions:
            info.append(f"Régime: {', '.join(self.dietary_restrictions)}")
        
        return "\n".join(info)


class StudentBuilder:
    """
    Builder pour construire un objet Student étape par étape
    """
    
    def __init__(self):
        self._student = Student()
    
    def set_basic_info(self, first_name, last_name, email):
        """Définit les informations de base (obligatoires)"""
        self._student.first_name = first_name
        self._student.last_name = last_name
        self._student.email = email
        return self  # Permet le chaînage
    
    def set_contact(self, phone=None, address=None, city=None, postal_code=None):
        """Définit les informations de contact"""
        if phone:
            self._student.phone = phone
        if address:
            self._student.address = address
        if city:
            self._student.city = city
        if postal_code:
            self._student.postal_code = postal_code
        return self
    
    def set_birth_date(self, birth_date):
        """Définit la date de naissance"""
        self._student.birth_date = birth_date
        return self
    
    def set_photo(self, photo_url):
        """Définit la photo de profil"""
        self._student.photo_url = photo_url
        return self
    
    def set_emergency_contact(self, name, phone):
        """Définit le contact d'urgence"""
        self._student.emergency_contact = {
            'name': name,
            'phone': phone
        }
        return self
    
    def set_scholarship(self, has_scholarship):
        """Définit si l'étudiant est boursier"""
        self._student.has_scholarship = has_scholarship
        return self
    
    def add_dietary_restriction(self, restriction):
        """Ajoute une restriction alimentaire"""
        if restriction not in self._student.dietary_restrictions:
            self._student.dietary_restrictions.append(restriction)
        return self
    
    def set_medical_info(self, info):
        """Définit les informations médicales"""
        self._student.medical_info = info
        return self
    
    def set_preferred_language(self, language):
        """Définit la langue préférée"""
        self._student.preferred_language = language
        return self
    
    def build(self):
        """
        Construit et retourne l'objet Student final
        Vérifie que les informations obligatoires sont présentes
        """
        if not all([self._student.first_name, 
                   self._student.last_name, 
                   self._student.email]):
            raise ValueError("Les informations de base sont obligatoires")
        
        return self._student


# Utilisation avec chaînage de méthodes
if __name__ == "__main__":
    # Étudiant simple
    student1 = (StudentBuilder()
                .set_basic_info("Marie", "Lafleur", "marie.lafleur@etudiant.ua.fr")
                .set_contact(phone="0696123456", city="Fort-de-France")
                .build())
    
    print(student1)
    print(student1.get_full_info())
    print("-" * 50)
    
    # Étudiant avec toutes les informations
    student2 = (StudentBuilder()
                .set_basic_info("Jean", "Martin", "jean.martin@etudiant.ua.fr")
                .set_contact(
                    phone="0696789012",
                    address="15 Rue des Palmiers",
                    city="Schoelcher",
                    postal_code="97233"
                )
                .set_birth_date("2003-08-15")
                .set_emergency_contact("Anne Martin", "0696111222")
                .set_scholarship(True)
                .add_dietary_restriction("végétarien")
                .add_dietary_restriction("sans gluten")
                .set_preferred_language("fr")
                .build())
    
    print(student2)
    print(student2.get_full_info())
```

**Sortie** :
```
Student: Marie Lafleur (marie.lafleur@etudiant.ua.fr)
Nom: Marie Lafleur
Email: marie.lafleur@etudiant.ua.fr
Téléphone: 0696123456
Ville: Fort-de-France
--------------------------------------------------
Student: Jean Martin (jean.martin@etudiant.ua.fr)
Nom: Jean Martin
Email: jean.martin@etudiant.ua.fr
Téléphone: 0696789012
Ville: Schoelcher
Boursier: Oui
Régime: végétarien, sans gluten
```

#### Variante : Director Pattern

Parfois, on veut avoir des configurations prédéfinies. Le **Director** encapsule des séquences de construction communes.

```python
class StudentDirector:
    """
    Director qui fournit des configurations prédéfinies
    """
    
    @staticmethod
    def create_basic_student(first_name, last_name, email):
        """Crée un étudiant avec le minimum d'informations"""
        return (StudentBuilder()
                .set_basic_info(first_name, last_name, email)
                .build())
    
    @staticmethod
    def create_scholarship_student(first_name, last_name, email, city):
        """Crée un étudiant boursier avec les infos requises"""
        return (StudentBuilder()
                .set_basic_info(first_name, last_name, email)
                .set_contact(city=city)
                .set_scholarship(True)
                .build())
    
    @staticmethod
    def create_international_student(first_name, last_name, email, 
                                     country, language):
        """Crée un étudiant international"""
        return (StudentBuilder()
                .set_basic_info(first_name, last_name, email)
                .set_contact(city=country)
                .set_preferred_language(language)
                .build())


# Utilisation
director = StudentDirector()
student = director.create_scholarship_student(
    "Sophie", "Bernard", "sophie@etudiant.ua.fr", "Le Lamentin"
)
```

#### ⚠️ Quand utiliser Builder ?

**✅ Utilisez-le pour :**
- Objets avec beaucoup de paramètres optionnels
- Construction étape par étape nécessaire
- Différentes représentations d'un même objet
- Validation complexe lors de la construction

**❌ Évitez-le pour :**
- Objets simples avec peu d'attributs
- Construction en une seule étape suffisante

---

### 1.2 Le Pattern Prototype

#### Problème à résoudre

Vous gérez des modèles de documents pour le campus (syllabus, certificats, attestations). Créer un nouveau document à partir de zéro est coûteux, mais vous voulez pouvoir dupliquer et modifier des modèles existants.

**Problème** : Comment créer de nouveaux objets en copiant des objets existants plutôt qu'en les construisant depuis zéro ?

**Solution** : Le pattern Prototype permet de cloner des objets existants.

#### Structure du Prototype

```python
import copy
from abc import ABC, abstractmethod
from datetime import datetime


class DocumentPrototype(ABC):
    """
    Interface pour les documents clonables
    """
    
    @abstractmethod
    def clone(self):
        """Crée une copie de l'objet"""
        pass


class Document(DocumentPrototype):
    """
    Classe de document avec clonage
    """
    
    def __init__(self, doc_type, title, content, metadata=None):
        self.doc_type = doc_type
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.sections = []
    
    def add_section(self, section_title, section_content):
        """Ajoute une section au document"""
        self.sections.append({
            'title': section_title,
            'content': section_content
        })
    
    def clone(self):
        """
        Clone le document (copie profonde)
        """
        # Utilise copy.deepcopy pour une copie complète
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.doc_type}: {self.title} ({len(self.sections)} sections)"


class DocumentRegistry:
    """
    Registry qui stocke les prototypes de documents
    """
    
    def __init__(self):
        self._prototypes = {}
    
    def register_prototype(self, name, prototype):
        """Enregistre un prototype"""
        self._prototypes[name] = prototype
    
    def get_prototype(self, name):
        """Récupère et clone un prototype"""
        prototype = self._prototypes.get(name)
        if prototype is None:
            raise ValueError(f"Prototype '{name}' non trouvé")
        return prototype.clone()
    
    def list_prototypes(self):
        """Liste tous les prototypes disponibles"""
        return list(self._prototypes.keys())


# Utilisation
if __name__ == "__main__":
    # Créer le registry
    registry = DocumentRegistry()
    
    # Créer un prototype de syllabus
    syllabus_template = Document(
        doc_type="Syllabus",
        title="Syllabus - [COURS]",
        content="",
        metadata={
            'university': 'Université des Antilles',
            'year': '2024-2025'
        }
    )
    syllabus_template.add_section("Objectifs pédagogiques", "[À compléter]")
    syllabus_template.add_section("Programme", "[À compléter]")
    syllabus_template.add_section("Évaluation", "[À compléter]")
    syllabus_template.add_section("Bibliographie", "[À compléter]")
    
    # Enregistrer le prototype
    registry.register_prototype("syllabus_standard", syllabus_template)
    
    # Créer un prototype de certificat
    certificate_template = Document(
        doc_type="Certificat",
        title="Certificat de Scolarité",
        content="L'Université des Antilles certifie que...",
        metadata={
            'university': 'Université des Antilles',
            'signature_required': True
        }
    )
    registry.register_prototype("certificate", certificate_template)
    
    print("Prototypes disponibles:", registry.list_prototypes())
    print("-" * 50)
    
    # Utiliser les prototypes pour créer de nouveaux documents
    
    # Document 1 : Syllabus POO
    syllabus_poo = registry.get_prototype("syllabus_standard")
    syllabus_poo.title = "Syllabus - Programmation Orientée Objet"
    syllabus_poo.sections[0]['content'] = "Maîtriser les concepts de la POO"
    syllabus_poo.sections[1]['content'] = "Classes, objets, héritage, polymorphisme..."
    
    # Document 2 : Syllabus Web
    syllabus_web = registry.get_prototype("syllabus_standard")
    syllabus_web.title = "Syllabus - Développement Web"
    syllabus_web.sections[0]['content'] = "Créer des applications web modernes"
    
    # Document 3 : Certificat pour un étudiant
    cert1 = registry.get_prototype("certificate")
    cert1.metadata['student_name'] = "Marie Lafleur"
    cert1.metadata['student_id'] = "20231234"
    
    # Vérifier que les documents sont indépendants
    print(syllabus_poo)
    print(syllabus_web)
    print(cert1)
    print("-" * 50)
    
    # Modifier le prototype original n'affecte pas les clones
    syllabus_template.title = "MODIFIÉ"
    new_syllabus = registry.get_prototype("syllabus_standard")
    print(f"Nouveau syllabus titre: {new_syllabus.title}")  # Toujours "[COURS]"
```

**Sortie** :
```
Prototypes disponibles: ['syllabus_standard', 'certificate']
--------------------------------------------------
Syllabus: Syllabus - Programmation Orientée Objet (4 sections)
Syllabus: Syllabus - Développement Web (4 sections)
Certificat: Certificat de Scolarité (0 sections)
--------------------------------------------------
Nouveau syllabus titre: Syllabus - [COURS]
```

#### Copie superficielle vs copie profonde

```python
import copy

class ExampleClass:
    def __init__(self):
        self.simple_value = 10
        self.list_value = [1, 2, 3]

original = ExampleClass()

# Copie superficielle (shallow copy)
shallow = copy.copy(original)
shallow.simple_value = 20  # N'affecte pas original
shallow.list_value.append(4)  # AFFECTE original ! (référence partagée)

print(f"Original list: {original.list_value}")  # [1, 2, 3, 4]

# Copie profonde (deep copy)
deep = copy.deepcopy(original)
deep.list_value.append(5)  # N'affecte PAS original

print(f"Original list: {original.list_value}")  # [1, 2, 3, 4]
```

#### ⚠️ Quand utiliser Prototype ?

**✅ Utilisez-le pour :**
- Créer des objets coûteux à initialiser
- Système de templates/modèles
- Éviter des sous-classes juste pour la création
- Configuration d'objets complexes réutilisables

**❌ Évitez-le pour :**
- Objets simples faciles à créer
- Quand les objets ont beaucoup de références circulaires (copie profonde compliquée)

---

### 1.3 Le Pattern Abstract Factory

#### Problème à résoudre

Vous développez une plateforme de cours en ligne qui doit supporter différents "thèmes" visuels : un thème clair (light) et un thème sombre (dark). Chaque thème a ses propres composants : boutons, formulaires, cartes, etc.

**Problème** : Comment créer des familles d'objets liés (tous les composants d'un même thème) sans spécifier leurs classes concrètes ?

**Solution** : Abstract Factory crée des familles d'objets liés.

#### Structure de l'Abstract Factory

```python
from abc import ABC, abstractmethod


# === Interfaces des produits ===

class Button(ABC):
    """Interface pour les boutons"""
    
    @abstractmethod
    def render(self):
        pass


class Form(ABC):
    """Interface pour les formulaires"""
    
    @abstractmethod
    def render(self):
        pass


class Card(ABC):
    """Interface pour les cartes"""
    
    @abstractmethod
    def render(self):
        pass


# === Produits concrets - Thème LIGHT ===

class LightButton(Button):
    def render(self):
        return "<button class='btn-light'>Bouton Clair</button>"


class LightForm(Form):
    def render(self):
        return "<form class='form-light'>Formulaire Clair</form>"


class LightCard(Card):
    def render(self):
        return "<div class='card-light'>Carte Claire</div>"


# === Produits concrets - Thème DARK ===

class DarkButton(Button):
    def render(self):
        return "<button class='btn-dark'>Bouton Sombre</button>"


class DarkForm(Form):
    def render(self):
        return "<form class='form-dark'>Formulaire Sombre</form>"


class DarkCard(Card):
    def render(self):
        return "<div class='card-dark'>Carte Sombre</div>"


# === Abstract Factory ===

class UIFactory(ABC):
    """Factory abstraite pour créer des familles de composants UI"""
    
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_form(self) -> Form:
        pass
    
    @abstractmethod
    def create_card(self) -> Card:
        pass


# === Factories concrètes ===

class LightThemeFactory(UIFactory):
    """Factory pour le thème clair"""
    
    def create_button(self) -> Button:
        return LightButton()
    
    def create_form(self) -> Form:
        return LightForm()
    
    def create_card(self) -> Card:
        return LightCard()


class DarkThemeFactory(UIFactory):
    """Factory pour le thème sombre"""
    
    def create_button(self) -> Button:
        return DarkButton()
    
    def create_form(self) -> Form:
        return DarkForm()
    
    def create_card(self) -> Card:
        return DarkCard()


# === Client qui utilise la factory ===

class CoursePage:
    """
    Page de cours qui utilise une factory pour créer ses composants
    """
    
    def __init__(self, factory: UIFactory):
        self.factory = factory
        self.button = None
        self.form = None
        self.card = None
    
    def build_page(self):
        """Construit la page avec les composants du thème"""
        self.button = self.factory.create_button()
        self.form = self.factory.create_form()
        self.card = self.factory.create_card()
    
    def render(self):
        """Affiche tous les composants"""
        components = [
            self.button.render(),
            self.form.render(),
            self.card.render()
        ]
        return "\n".join(components)


# Utilisation
if __name__ == "__main__":
    # Créer une page avec le thème clair
    print("=== THÈME CLAIR ===")
    light_factory = LightThemeFactory()
    page_light = CoursePage(light_factory)
    page_light.build_page()
    print(page_light.render())
    
    print("\n" + "=" * 50 + "\n")
    
    # Créer une page avec le thème sombre
    print("=== THÈME SOMBRE ===")
    dark_factory = DarkThemeFactory()
    page_dark = CoursePage(dark_factory)
    page_dark.build_page()
    print(page_dark.render())
    
    print("\n" + "=" * 50 + "\n")
    
    # Changement de thème dynamique
    print("=== CHANGEMENT DE THÈME ===")
    user_preference = "dark"  # Préférence de l'utilisateur
    
    if user_preference == "dark":
        factory = DarkThemeFactory()
    else:
        factory = LightThemeFactory()
    
    page = CoursePage(factory)
    page.build_page()
    print(page.render())
```

**Sortie** :
```
=== THÈME CLAIR ===
<button class='btn-light'>Bouton Clair</button>
<form class='form-light'>Formulaire Clair</form>
<div class='card-light'>Carte Claire</div>

==================================================

=== THÈME SOMBRE ===
<button class='btn-dark'>Bouton Sombre</button>
<form class='form-dark'>Formulaire Sombre</form>
<div class='card-dark'>Carte Sombre</div>

==================================================

=== CHANGEMENT DE THÈME ===
<button class='btn-dark'>Bouton Sombre</button>
<form class='form-dark'>Formulaire Sombre</form>
<div class='card-dark'>Carte Sombre</div>
```

#### Exemple avancé : Factories de bases de données

```python
class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def execute_query(self, query): pass


class QueryBuilder(ABC):
    @abstractmethod
    def select(self, table, columns): pass


# PostgreSQL
class PostgreSQLConnection(DatabaseConnection):
    def connect(self):
        return "Connecté à PostgreSQL"
    
    def execute_query(self, query):
        return f"PostgreSQL exécute: {query}"


class PostgreSQLQueryBuilder(QueryBuilder):
    def select(self, table, columns):
        cols = ", ".join(columns)
        return f"SELECT {cols} FROM {table}"


# MySQL
class MySQLConnection(DatabaseConnection):
    def connect(self):
        return "Connecté à MySQL"
    
    def execute_query(self, query):
        return f"MySQL exécute: {query}"


class MySQLQueryBuilder(QueryBuilder):
    def select(self, table, columns):
        cols = ", ".join(columns)
        return f"SELECT {cols} FROM {table}"


# Abstract Factory
class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> DatabaseConnection: pass
    
    @abstractmethod
    def create_query_builder(self) -> QueryBuilder: pass


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self):
        return PostgreSQLConnection()
    
    def create_query_builder(self):
        return PostgreSQLQueryBuilder()


class MySQLFactory(DatabaseFactory):
    def create_connection(self):
        return MySQLConnection()
    
    def create_query_builder(self):
        return MySQLQueryBuilder()


# Utilisation
def setup_database(factory: DatabaseFactory):
    connection = factory.create_connection()
    query_builder = factory.create_query_builder()
    
    print(connection.connect())
    query = query_builder.select("students", ["name", "email"])
    print(connection.execute_query(query))


# Choisir la base de données
db_type = "postgresql"  # Configurable
if db_type == "postgresql":
    factory = PostgreSQLFactory()
else:
    factory = MySQLFactory()

setup_database(factory)
```

#### ⚠️ Quand utiliser Abstract Factory ?

**✅ Utilisez-le pour :**
- Créer des familles d'objets liés (thèmes, plateformes, drivers)
- Assurer la cohérence entre les objets créés
- Isoler le code client des classes concrètes
- Supporter plusieurs variantes d'un système

**❌ Évitez-le pour :**
- Une seule famille d'objets (Factory Method suffit)
- Objets indépendants sans relation forte

---

## 2. Patterns de Structure

Les patterns de structure concernent la composition des classes et objets pour former des structures plus larges et flexibles.

### 2.1 Le Pattern Adapter

#### Problème à résoudre

Vous intégrez un nouveau système de paiement dans votre application campus, mais son interface est différente de celle que vous utilisez actuellement.

**Problème** : Comment faire fonctionner ensemble des classes ayant des interfaces incompatibles ?

**Solution** : L'Adapter fait office de traducteur entre deux interfaces incompatibles.

#### Structure de l'Adapter

```python
from abc import ABC, abstractmethod


# === Interface cible (celle que le client attend) ===

class PaymentProcessor(ABC):
    """Interface standard de traitement des paiements"""
    
    @abstractmethod
    def process_payment(self, amount, student_id):
        """Traite un paiement"""
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id):
        """Récupère le statut d'une transaction"""
        pass


# === Ancienne implémentation ===

class UniversityPaymentSystem(PaymentProcessor):
    """Ancien système de paiement de l'université"""
    
    def process_payment(self, amount, student_id):
        print(f"[Système UA] Paiement de {amount}€ pour l'étudiant {student_id}")
        return f"UA-{student_id}-001"
    
    def get_transaction_status(self, transaction_id):
        return f"Statut de {transaction_id}: COMPLÉTÉ"


# === Nouveau système externe (interface incompatible) ===

class StripePaymentGateway:
    """
    API Stripe (interface différente)
    """
    
    def create_charge(self, amount_cents, customer_email, metadata):
        """
        Crée un paiement Stripe
        Note: montant en centimes, utilise email au lieu de student_id
        """
        print(f"[Stripe] Charge de {amount_cents} centimes pour {customer_email}")
        return {"charge_id": f"ch_stripe_{customer_email[:5]}", "status": "succeeded"}
    
    def retrieve_charge(self, charge_id):
        """Récupère les détails d'un paiement"""
        return {"id": charge_id, "status": "succeeded", "paid": True}


# === Adapter pour Stripe ===

class StripePaymentAdapter(PaymentProcessor):
    """
    Adapter qui fait fonctionner Stripe avec l'interface PaymentProcessor
    """
    
    def __init__(self):
        self.stripe = StripePaymentGateway()
        # Mapping des student_id vers emails (simplifié)
        self.student_emails = {}
    
    def register_student(self, student_id, email):
        """Enregistre l'email d'un étudiant"""
        self.student_emails[student_id] = email
    
    def process_payment(self, amount, student_id):
        """
        Adapte l'interface process_payment pour utiliser Stripe
        """
        # Convertir euros en centimes
        amount_cents = int(amount * 100)
        
        # Récupérer l'email de l'étudiant
        email = self.student_emails.get(student_id, f"student{student_id}@ua.fr")
        
        # Utiliser l'API Stripe
        result = self.stripe.create_charge(
            amount_cents=amount_cents,
            customer_email=email,
            metadata={"student_id": student_id}
        )
        
        return result["charge_id"]
    
    def get_transaction_status(self, transaction_id):
        """
        Adapte l'interface get_transaction_status pour Stripe
        """
        charge = self.stripe.retrieve_charge(transaction_id)
        
        # Traduire le statut Stripe vers notre format
        status_map = {
            "succeeded": "COMPLÉTÉ",
            "pending": "EN_ATTENTE",
            "failed": "ÉCHOUÉ"
        }
        
        status = status_map.get(charge["status"], "INCONNU")
        return f"Statut de {transaction_id}: {status}"


# === Client qui utilise le PaymentProcessor ===

class PaymentService:
    """
    Service de paiement qui utilise n'importe quel PaymentProcessor
    """
    
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def charge_student(self, amount, student_id):
        """Facture un étudiant"""
        print(f"\n--- Facturation de {amount}€ ---")
        transaction_id = self.processor.process_payment(amount, student_id)
        print(f"Transaction ID: {transaction_id}")
        
        # Vérifier le statut
        status = self.processor.get_transaction_status(transaction_id)
        print(status)
        
        return transaction_id


# Utilisation
if __name__ == "__main__":
    # Utilisation avec l'ancien système
    print("=== ANCIEN SYSTÈME ===")
    old_processor = UniversityPaymentSystem()
    service = PaymentService(old_processor)
    service.charge_student(50.00, "20231234")
    
    print("\n" + "=" * 50)
    
    # Migration vers Stripe avec l'Adapter
    print("\n=== NOUVEAU SYSTÈME (STRIPE) ===")
    stripe_adapter = StripePaymentAdapter()
    stripe_adapter.register_student("20231234", "marie.lafleur@etudiant.ua.fr")
    
    service = PaymentService(stripe_adapter)
    service.charge_student(75.50, "20231234")
    
    # Le code client reste IDENTIQUE !
    # Seul le processor change
```

**Sortie** :
```
=== ANCIEN SYSTÈME ===

--- Facturation de 50.0€ ---
[Système UA] Paiement de 50.0€ pour l'étudiant 20231234
Transaction ID: UA-20231234-001
Statut de UA-20231234-001: COMPLÉTÉ

==================================================

=== NOUVEAU SYSTÈME (STRIPE) ===

--- Facturation de 75.5€ ---
[Stripe] Charge de 7550 centimes pour marie.lafleur@etudiant.ua.fr
Transaction ID: ch_stripe_marie
Statut de ch_stripe_marie: COMPLÉTÉ
```

#### Variante : Object Adapter vs Class Adapter

```python
# Object Adapter (composition - recommandé en Python)
class ObjectAdapter(PaymentProcessor):
    def __init__(self, adaptee):
        self.adaptee = adaptee  # Composition
    
    def process_payment(self, amount, student_id):
        return self.adaptee.external_method(amount)


# Class Adapter (héritage multiple)
class ClassAdapter(PaymentProcessor, ExternalPaymentAPI):
    def process_payment(self, amount, student_id):
        return self.external_method(amount)  # Méthode héritée
```

#### ⚠️ Quand utiliser Adapter ?

**✅ Utilisez-le pour :**
- Intégrer des bibliothèques/API tierces
- Faire cohabiter ancien et nouveau code
- Réutiliser des classes existantes avec interface incompatible
- Migration progressive de systèmes

**❌ Évitez-le pour :**
- Interfaces déjà compatibles
- Quand vous pouvez modifier directement les classes

---

### 2.2 Le Pattern Decorator

#### Problème à résoudre

Vous avez un système de notifications pour le campus. Vous voulez pouvoir ajouter dynamiquement des fonctionnalités : logging, encryption, retry, rate limiting, etc.

**Problème** : Comment ajouter des responsabilités à un objet dynamiquement sans créer une explosion de sous-classes ?

**Solution** : Le Decorator enveloppe un objet pour ajouter des comportements.

#### Structure du Decorator

```python
from abc import ABC, abstractmethod
import time
from datetime import datetime


# === Interface de base ===

class Notification(ABC):
    """Interface pour les notifications"""
    
    @abstractmethod
    def send(self, message, recipient):
        """Envoie une notification"""
        pass


# === Composant concret de base ===

class EmailNotification(Notification):
    """Notification par email de base"""
    
    def send(self, message, recipient):
        print(f"[EMAIL] Envoi à {recipient}: {message}")
        return True


class SMSNotification(Notification):
    """Notification par SMS de base"""
    
    def send(self, message, recipient):
        print(f"[SMS] Envoi à {recipient}: {message[:50]}...")  # SMS limité
        return True


# === Decorator de base ===

class NotificationDecorator(Notification):
    """
    Decorator de base pour les notifications
    """
    
    def __init__(self, notification: Notification):
        self._notification = notification
    
    def send(self, message, recipient):
        return self._notification.send(message, recipient)


# === Decorators concrets ===

class LoggingDecorator(NotificationDecorator):
    """Ajoute du logging aux notifications"""
    
    def send(self, message, recipient):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {timestamp}] Début envoi notification")
        
        result = super().send(message, recipient)
        
        print(f"[LOG {timestamp}] Fin envoi notification - Succès: {result}")
        return result


class EncryptionDecorator(NotificationDecorator):
    """Chiffre le contenu des notifications"""
    
    def send(self, message, recipient):
        # Simulation de chiffrement
        encrypted_message = f"[ENCRYPTED: {message[::-1]}]"  # Inversion simple
        print(f"[CRYPTO] Message chiffré")
        
        return super().send(encrypted_message, recipient)


class RetryDecorator(NotificationDecorator):
    """Ajoute une logique de retry"""
    
    def __init__(self, notification: Notification, max_retries=3):
        super().__init__(notification)
        self.max_retries = max_retries
    
    def send(self, message, recipient):
        for attempt in range(1, self.max_retries + 1):
            print(f"[RETRY] Tentative {attempt}/{self.max_retries}")
            
            try:
                result = super().send(message, recipient)
                if result:
                    return True
            except Exception as e:
                print(f"[RETRY] Échec: {e}")
                if attempt < self.max_retries:
                    time.sleep(1)  # Attendre avant retry
        
        print(f"[RETRY] Échec après {self.max_retries} tentatives")
        return False


class RateLimitDecorator(NotificationDecorator):
    """Limite le nombre de notifications par période"""
    
    def __init__(self, notification: Notification, max_per_minute=5):
        super().__init__(notification)
        self.max_per_minute = max_per_minute
        self.sent_count = 0
        self.last_reset = time.time()
    
    def send(self, message, recipient):
        # Réinitialiser le compteur chaque minute
        if time.time() - self.last_reset > 60:
            self.sent_count = 0
            self.last_reset = time.time()
        
        if self.sent_count >= self.max_per_minute:
            print(f"[RATE_LIMIT] Limite atteinte ({self.max_per_minute}/min)")
            return False
        
        self.sent_count += 1
        return super().send(message, recipient)


# === Utilisation ===

if __name__ == "__main__":
    # Notification simple
    print("=== NOTIFICATION SIMPLE ===")
    simple = EmailNotification()
    simple.send("Rappel: cours demain à 8h", "marie@etudiant.ua.fr")
    
    print("\n" + "=" * 50 + "\n")
    
    # Notification avec logging
    print("=== AVEC LOGGING ===")
    with_logging = LoggingDecorator(EmailNotification())
    with_logging.send("Rappel: cours demain à 8h", "marie@etudiant.ua.fr")
    
    print("\n" + "=" * 50 + "\n")
    
    # Notification avec chiffrement ET logging
    print("=== CHIFFREMENT + LOGGING ===")
    encrypted_logged = LoggingDecorator(
        EncryptionDecorator(EmailNotification())
    )
    encrypted_logged.send("Message confidentiel", "admin@ua.fr")
    
    print("\n" + "=" * 50 + "\n")
    
    # Notification complète : Retry + Rate Limit + Logging + Encryption
    print("=== STACK COMPLET ===")
    full_stack = RetryDecorator(
        RateLimitDecorator(
            LoggingDecorator(
                EncryptionDecorator(
                    SMSNotification()
                )
            ),
            max_per_minute=10
        ),
        max_retries=2
    )
    
    full_stack.send("Alerte importante", "0696123456")
```

**Sortie** :
```
=== NOTIFICATION SIMPLE ===
[EMAIL] Envoi à marie@etudiant.ua.fr: Rappel: cours demain à 8h

==================================================

=== AVEC LOGGING ===
[LOG 2025-02-01 10:30:15] Début envoi notification
[EMAIL] Envoi à marie@etudiant.ua.fr: Rappel: cours demain à 8h
[LOG 2025-02-01 10:30:15] Fin envoi notification - Succès: True

==================================================

=== CHIFFREMENT + LOGGING ===
[LOG 2025-02-01 10:30:15] Début envoi notification
[CRYPTO] Message chiffré
[EMAIL] Envoi à admin@ua.fr: [ENCRYPTED: leitnedifnoc egasseM]
[LOG 2025-02-01 10:30:15] Fin envoi notification - Succès: True

==================================================

=== STACK COMPLET ===
[RETRY] Tentative 1/2
[CRYPTO] Message chiffré
[LOG 2025-02-01 10:30:15] Début envoi notification
[SMS] Envoi à 0696123456: [ENCRYPTED: etnatropmi etrelA]...
[LOG 2025-02-01 10:30:15] Fin envoi notification - Succès: True
```

#### Decorator vs Héritage

```python
# ❌ Avec héritage - Explosion combinatoire
class EmailWithLogging(EmailNotification): pass
class EmailWithEncryption(EmailNotification): pass
class EmailWithLoggingAndEncryption(EmailNotification): pass
class SMSWithLogging(SMSNotification): pass
class SMSWithEncryption(SMSNotification): pass
# ... combinaisons infinies !

# ✅ Avec Decorator - Composition flexible
notification = LoggingDecorator(EncryptionDecorator(EmailNotification()))
```

#### ⚠️ Quand utiliser Decorator ?

**✅ Utilisez-le pour :**
- Ajouter des responsabilités dynamiquement
- Combiner plusieurs comportements
- Éviter l'explosion de sous-classes
- Middleware, logging, caching, validation

**❌ Évitez-le pour :**
- Comportements qui doivent être dans la classe de base
- Quand l'ordre des decorators n'a pas d'importance (utilisez autre chose)

---

### 2.3 Le Pattern Facade

#### Problème à résoudre

Vous avez un système complexe de gestion des inscriptions qui implique plusieurs sous-systèmes : validation, paiement, génération de documents, envoi de notifications, mise à jour de la base de données.

**Problème** : Comment simplifier l'interaction avec un système complexe ?

**Solution** : La Facade fournit une interface simplifiée à un ensemble de sous-systèmes.

#### Structure de la Facade

```python
# === Sous-systèmes complexes ===

class StudentValidator:
    """Valide les informations d'un étudiant"""
    
    def validate_identity(self, first_name, last_name, birth_date):
        print(f"[Validator] Validation identité: {first_name} {last_name}")
        return True
    
    def validate_documents(self, documents):
        print(f"[Validator] Validation documents: {len(documents)} pièces")
        return True
    
    def check_prerequisites(self, student_id, course_id):
        print(f"[Validator] Vérification prérequis pour cours {course_id}")
        return True


class PaymentSystem:
    """Gère les paiements"""
    
    def calculate_fees(self, course_id, scholarship):
        print(f"[Payment] Calcul frais pour cours {course_id}")
        if scholarship:
            return 0.0
        return 250.0
    
    def process_payment(self, student_id, amount):
        print(f"[Payment] Traitement paiement de {amount}€")
        return "PAY-12345"
    
    def send_receipt(self, email, transaction_id):
        print(f"[Payment] Envoi reçu à {email}")


class CourseManager:
    """Gère les cours et inscriptions"""
    
    def check_availability(self, course_id):
        print(f"[Course] Vérification places disponibles pour {course_id}")
        return True
    
    def enroll_student(self, student_id, course_id):
        print(f"[Course] Inscription étudiant {student_id} au cours {course_id}")
        return True
    
    def reserve_seat(self, student_id, course_id):
        print(f"[Course] Réservation place pour {student_id}")


class DocumentGenerator:
    """Génère les documents administratifs"""
    
    def generate_enrollment_certificate(self, student_id, course_id):
        print(f"[DocGen] Génération certificat d'inscription")
        return "certificate_url.pdf"
    
    def generate_student_card(self, student_id):
        print(f"[DocGen] Génération carte étudiant")
        return "card_url.pdf"


class NotificationSystem:
    """Envoie les notifications"""
    
    def send_welcome_email(self, email, student_name):
        print(f"[Notification] Email de bienvenue à {email}")
    
    def send_course_confirmation(self, email, course_name):
        print(f"[Notification] Confirmation inscription à {course_name}")


class DatabaseManager:
    """Gère la base de données"""
    
    def save_student(self, student_data):
        print(f"[Database] Sauvegarde étudiant: {student_data.get('email')}")
        return "STU-2025-001"
    
    def update_enrollment_status(self, student_id, course_id, status):
        print(f"[Database] Mise à jour statut inscription: {status}")


# === FACADE ===

class EnrollmentFacade:
    """
    Facade qui simplifie le processus d'inscription
    Interface simple pour un système complexe
    """
    
    def __init__(self):
        # Initialiser tous les sous-systèmes
        self.validator = StudentValidator()
        self.payment = PaymentSystem()
        self.course_manager = CourseManager()
        self.doc_generator = DocumentGenerator()
        self.notifications = NotificationSystem()
        self.database = DatabaseManager()
    
    def enroll_new_student(self, student_data, course_id):
        """
        Méthode simplifiée pour inscrire un nouvel étudiant
        Cache toute la complexité des sous-systèmes
        
        Args:
            student_data: dict avec first_name, last_name, email, etc.
            course_id: ID du cours
        
        Returns:
            dict avec le résultat de l'inscription
        """
        print("=" * 60)
        print("DÉBUT DU PROCESSUS D'INSCRIPTION")
        print("=" * 60)
        
        try:
            # Étape 1: Validation
            print("\n[1/6] Validation des informations...")
            if not self.validator.validate_identity(
                student_data['first_name'],
                student_data['last_name'],
                student_data.get('birth_date')
            ):
                return {"success": False, "error": "Validation échouée"}
            
            if not self.validator.validate_documents(
                student_data.get('documents', [])
            ):
                return {"success": False, "error": "Documents invalides"}
            
            # Étape 2: Vérifier disponibilité du cours
            print("\n[2/6] Vérification du cours...")
            if not self.course_manager.check_availability(course_id):
                return {"success": False, "error": "Cours complet"}
            
            if not self.validator.check_prerequisites(
                student_data.get('id'), course_id
            ):
                return {"success": False, "error": "Prérequis non satisfaits"}
            
            # Étape 3: Traiter le paiement
            print("\n[3/6] Traitement du paiement...")
            amount = self.payment.calculate_fees(
                course_id, 
                student_data.get('has_scholarship', False)
            )
            
            if amount > 0:
                transaction_id = self.payment.process_payment(
                    student_data.get('id'), amount
                )
                self.payment.send_receipt(
                    student_data['email'], transaction_id
                )
            
            # Étape 4: Enregistrer l'étudiant
            print("\n[4/6] Enregistrement dans la base de données...")
            student_id = self.database.save_student(student_data)
            
            # Étape 5: Inscription au cours
            print("\n[5/6] Inscription au cours...")
            self.course_manager.reserve_seat(student_id, course_id)
            self.course_manager.enroll_student(student_id, course_id)
            self.database.update_enrollment_status(
                student_id, course_id, "ENROLLED"
            )
            
            # Étape 6: Générer documents et envoyer notifications
            print("\n[6/6] Finalisation...")
            certificate_url = self.doc_generator.generate_enrollment_certificate(
                student_id, course_id
            )
            card_url = self.doc_generator.generate_student_card(student_id)
            
            self.notifications.send_welcome_email(
                student_data['email'],
                f"{student_data['first_name']} {student_data['last_name']}"
            )
            self.notifications.send_course_confirmation(
                student_data['email'],
                f"Cours {course_id}"
            )
            
            print("\n" + "=" * 60)
            print("✓ INSCRIPTION RÉUSSIE")
            print("=" * 60)
            
            return {
                "success": True,
                "student_id": student_id,
                "certificate": certificate_url,
                "student_card": card_url
            }
        
        except Exception as e:
            print(f"\n✗ ERREUR: {e}")
            return {"success": False, "error": str(e)}


# === Utilisation ===

if __name__ == "__main__":
    # Sans Facade - Code client complexe
    print("### SANS FACADE (Complexe) ###\n")
    
    # Le client doit connaître et gérer tous les sous-systèmes
    validator = StudentValidator()
    payment = PaymentSystem()
    course_manager = CourseManager()
    # ... beaucoup de code complexe
    
    print("\n\n")
    
    # Avec Facade - Code client simple
    print("### AVEC FACADE (Simple) ###\n")
    
    enrollment = EnrollmentFacade()
    
    # Une seule méthode !
    result = enrollment.enroll_new_student(
        student_data={
            'first_name': 'Marie',
            'last_name': 'Lafleur',
            'email': 'marie.lafleur@etudiant.ua.fr',
            'birth_date': '2003-05-15',
            'has_scholarship': True,
            'documents': ['id_card.pdf', 'photo.jpg']
        },
        course_id='POO-L2-2025'
    )
    
    if result['success']:
        print(f"\nÉtudiant inscrit avec l'ID: {result['student_id']}")
        print(f"Certificat: {result['certificate']}")
        print(f"Carte: {result['student_card']}")
```

**Sortie** :
```
### AVEC FACADE (Simple) ###

============================================================
DÉBUT DU PROCESSUS D'INSCRIPTION
============================================================

[1/6] Validation des informations...
[Validator] Validation identité: Marie Lafleur
[Validator] Validation documents: 2 pièces

[2/6] Vérification du cours...
[Course] Vérification places disponibles pour POO-L2-2025
[Validator] Vérification prérequis pour cours POO-L2-2025

[3/6] Traitement du paiement...
[Payment] Calcul frais pour cours POO-L2-2025

[4/6] Enregistrement dans la base de données...
[Database] Sauvegarde étudiant: marie.lafleur@etudiant.ua.fr

[5/6] Inscription au cours...
[Course] Réservation place pour STU-2025-001
[Course] Inscription étudiant STU-2025-001 au cours POO-L2-2025
[Database] Mise à jour statut inscription: ENROLLED

[6/6] Finalisation...
[DocGen] Génération certificat d'inscription
[DocGen] Génération carte étudiant
[Notification] Email de bienvenue à marie.lafleur@etudiant.ua.fr
[Notification] Confirmation inscription à Cours POO-L2-2025

============================================================
✓ INSCRIPTION RÉUSSIE
============================================================

Étudiant inscrit avec l'ID: STU-2025-001
Certificat: certificate_url.pdf
Carte: card_url.pdf
```

#### ⚠️ Quand utiliser Facade ?

**✅ Utilisez-le pour :**
- Simplifier une interface complexe
- Réduire les dépendances entre le client et les sous-systèmes
- Découpler le code client des implémentations
- Fournir un point d'entrée unique

**❌ Évitez-le pour :**
- Systèmes déjà simples
- Quand le client a besoin d'accéder aux détails des sous-systèmes

---

## 3. Exercices pratiques

### Exercice 1 : Builder - Création de Quiz

Créez un système de construction de quiz avec :
- Questions de différents types (QCM, vrai/faux, réponse courte)
- Paramètres : durée, nombre de tentatives, note minimale
- Sections thématiques
- Options d'affichage aléatoire

```python
# À compléter
class QuizBuilder:
    # Votre code ici
    pass
```

### Exercice 2 : Decorator - Système de Cache

Créez des decorators pour un système de récupération de données :
- CacheDecorator : met en cache les résultats
- TimingDecorator : mesure le temps d'exécution
- ValidationDecorator : valide les données avant/après
- MockDecorator : retourne des données de test

```python
# À compléter
class DataRetriever(ABC):
    @abstractmethod
    def get_data(self, key): pass

# Vos decorators ici
```

### Exercice 3 : Facade + Adapter - Système Multi-API

Créez une facade qui unifie plusieurs APIs de ressources éducatives :
- YouTube API (vidéos)
- Wikipedia API (articles)
- ArXiv API (articles scientifiques)

Utilisez des Adapters pour normaliser les différentes APIs, puis une Facade pour fournir une interface simple de recherche.

---

## 4. Patterns combinés - Exemple complet

Voici comment combiner plusieurs patterns dans un système réel :

```python
# Singleton pour la configuration
@singleton
class AppConfig:
    pass

# Factory pour créer des resources
class ResourceFactory:
    pass

# Decorator pour ajouter des fonctionnalités
class CachedResource(ResourceDecorator):
    pass

# Facade pour simplifier l'utilisation
class LearningPlatformFacade:
    def __init__(self):
        self.config = AppConfig()  # Singleton
        self.factory = ResourceFactory()  # Factory
    
    def get_resource(self, resource_id):
        resource = self.factory.create_resource(resource_id)
        return CachedResource(resource)  # Decorator
```

---

## 5. Comparaison des Patterns

### Patterns de Création

| Pattern | Objectif | Cas d'usage |
|---------|----------|-------------|
| **Singleton** | Une seule instance | Configuration, connexion DB |
| **Factory Method** | Déléguer la création | Objets de types variés |
| **Abstract Factory** | Familles d'objets | Thèmes, plateformes |
| **Builder** | Construction complexe | Objets avec beaucoup de paramètres |
| **Prototype** | Clonage | Templates, copies |

### Patterns de Structure

| Pattern | Objectif | Cas d'usage |
|---------|----------|-------------|
| **Adapter** | Compatibilité d'interfaces | Intégration de systèmes |
| **Decorator** | Ajout dynamique de fonctionnalités | Middleware, logging |
| **Facade** | Simplification d'interface | Systèmes complexes |

---

## 6. Anti-Patterns et pièges

### 6.1 Pattern Overuse

```python
# ❌ Mauvais - Patterns inutiles
class SimpleName:
    pass

simple_factory = SimpleNameFactory()
name = simple_factory.create_name()  # Pourquoi une factory ?!
```

### 6.2 Decorator Hell

```python
# ❌ Trop de decorators = code illisible
obj = A(B(C(D(E(F(G(BaseClass())))))))
```

### 6.3 God Facade

```python
# ❌ Facade qui fait tout
class SuperFacade:
    def do_everything(self): pass  # 1000 lignes de code
```

---

## 7. Résumé

### Ce que nous avons vu

**Patterns de Création (suite) :**
- **Builder** : Construction étape par étape
- **Prototype** : Clonage d'objets
- **Abstract Factory** : Familles d'objets cohérentes

**Patterns de Structure :**
- **Adapter** : Compatibilité d'interfaces
- **Decorator** : Enrichissement dynamique
- **Facade** : Simplification d'interfaces complexes

### Principes clés

1. **Composition > Héritage** : Privilégier la composition (Decorator, Adapter)
2. **Interface simple** : Cacher la complexité (Facade)
3. **Flexibilité** : Permettre l'extension sans modification
4. **Réutilisabilité** : Solutions génériques adaptables

### Prochaine partie

Dans le CM5, nous verrons :
- **Patterns comportementaux** : Observer, Strategy, Command
- **Principes SOLID** appliqués
- **Design patterns avancés**

---

## 8. Ressources et liens utiles

**Pour aller plus loin :**
- Pratiquez avec des projets réels
- Identifiez les patterns dans les frameworks (Django, Flask, Laravel)
- Lisez du code open-source

**Quiz en ligne :**
- Refactoring.Guru - Design Patterns Quiz
- Python Patterns Interactive Tutorials

---

## Questions ?

Prochaine séance : **Patterns Comportementaux** et applications pratiques dans vos projets de groupe !