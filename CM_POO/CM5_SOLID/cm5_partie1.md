# CM5 - Principes SOLID Approfondis
## Programmation Orientée Objet

---

## Introduction

Dans le CM4, nous avons étudié les **design patterns** - des solutions réutilisables à des problèmes récurrents. Aujourd'hui, nous allons approfondir les **principes SOLID**, qui sont les fondations d'une bonne conception orientée objet.

### Qu'est-ce que SOLID ?

SOLID est un acronyme pour 5 principes fondamentaux de la POO, introduits par Robert C. Martin (Uncle Bob) :

- **S** - Single Responsibility Principle (Principe de responsabilité unique)
- **O** - Open/Closed Principle (Principe ouvert/fermé)
- **L** - Liskov Substitution Principle (Principe de substitution de Liskov)
- **I** - Interface Segregation Principle (Principe de ségrégation des interfaces)
- **D** - Dependency Inversion Principle (Principe d'inversion des dépendances)

### Pourquoi SOLID ?

Ces principes permettent de créer du code :
- ✅ **Maintenable** : Facile à modifier et étendre
- ✅ **Testable** : Facile à tester unitairement
- ✅ **Flexible** : S'adapte aux changements
- ✅ **Compréhensible** : Structure claire et logique
- ✅ **Réutilisable** : Composants indépendants

**Important :** SOLID ne sont pas des règles absolues, mais des **guidelines** pour prendre de meilleures décisions de conception.

---

## 1. Single Responsibility Principle (SRP)

### Définition

> **Une classe ne devrait avoir qu'une seule raison de changer.**

Autrement dit : **une classe = une responsabilité**.

### Problème à résoudre

Quand une classe fait trop de choses différentes :
- Difficile à comprendre
- Difficile à tester
- Changements risqués (effet domino)
- Violation du principe de cohésion

### ❌ Violation du SRP

```python
class Student:
    """
    ❌ Cette classe a TROP de responsabilités
    """
    
    def __init__(self, name, email, student_id):
        self.name = name
        self.email = email
        self.student_id = student_id
        self.grades = []
    
    # Responsabilité 1: Gestion des données étudiant
    def add_grade(self, course, grade):
        self.grades.append({'course': course, 'grade': grade})
    
    def get_average(self):
        if not self.grades:
            return 0
        return sum(g['grade'] for g in self.grades) / len(self.grades)
    
    # Responsabilité 2: Validation des données
    def validate_email(self):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, self.email) is not None
    
    def validate_student_id(self):
        return len(self.student_id) == 8 and self.student_id.isdigit()
    
    # Responsabilité 3: Persistance en base de données
    def save_to_database(self):
        import sqlite3
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (self.student_id, self.name, self.email)
        )
        conn.commit()
        conn.close()
    
    # Responsabilité 4: Génération de rapports
    def generate_report(self):
        report = f"=== Rapport pour {self.name} ===\n"
        report += f"ID: {self.student_id}\n"
        report += f"Email: {self.email}\n"
        report += f"Moyenne: {self.get_average():.2f}\n"
        return report
    
    # Responsabilité 5: Envoi d'emails
    def send_welcome_email(self):
        import smtplib
        msg = f"Bienvenue {self.name}!"
        # Code d'envoi d'email...
        print(f"Email envoyé à {self.email}")
    
    # Responsabilité 6: Export
    def export_to_json(self):
        import json
        return json.dumps({
            'name': self.name,
            'email': self.email,
            'student_id': self.student_id,
            'grades': self.grades
        })
```

**Problèmes de cette classe :**
1. Si le format de rapport change → modifier Student
2. Si la base de données change → modifier Student
3. Si la validation d'email change → modifier Student
4. Impossible de tester la logique métier sans BD
5. Classe énorme et difficile à maintenir

### ✅ Respect du SRP

```python
from abc import ABC, abstractmethod
from typing import List, Dict
import re
import json


# === Classe Student : UNE SEULE responsabilité (données métier) ===

class Student:
    """
    ✅ Responsabilité unique: Gérer les données métier d'un étudiant
    """
    
    def __init__(self, name: str, email: str, student_id: str):
        self.name = name
        self.email = email
        self.student_id = student_id
        self.grades: List[Dict] = []
    
    def add_grade(self, course: str, grade: float):
        """Ajoute une note"""
        self.grades.append({'course': course, 'grade': grade})
    
    def get_average(self) -> float:
        """Calcule la moyenne"""
        if not self.grades:
            return 0.0
        return sum(g['grade'] for g in self.grades) / len(self.grades)
    
    def get_grades_for_course(self, course: str) -> List[float]:
        """Récupère toutes les notes pour un cours"""
        return [g['grade'] for g in self.grades if g['course'] == course]


# === Validation : Responsabilité séparée ===

class StudentValidator:
    """
    ✅ Responsabilité unique: Valider les données étudiant
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valide le format d'email"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """Valide le format de l'ID étudiant"""
        return len(student_id) == 8 and student_id.isdigit()
    
    @staticmethod
    def validate_grade(grade: float) -> bool:
        """Valide qu'une note est dans l'intervalle valide"""
        return 0 <= grade <= 20
    
    def validate_student(self, student: Student) -> tuple[bool, List[str]]:
        """
        Valide un étudiant complet
        Returns: (is_valid, error_messages)
        """
        errors = []
        
        if not self.validate_email(student.email):
            errors.append("Email invalide")
        
        if not self.validate_student_id(student.student_id):
            errors.append("ID étudiant invalide (doit être 8 chiffres)")
        
        if not student.name or len(student.name) < 2:
            errors.append("Nom invalide")
        
        return len(errors) == 0, errors


# === Persistance : Responsabilité séparée ===

class StudentRepository:
    """
    ✅ Responsabilité unique: Gérer la persistance des étudiants
    """
    
    def __init__(self, db_path: str = 'students.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def save(self, student: Student):
        """Sauvegarde un étudiant"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO students VALUES (?, ?, ?)",
            (student.student_id, student.name, student.email)
        )
        conn.commit()
        conn.close()
    
    def find_by_id(self, student_id: str) -> Student:
        """Récupère un étudiant par son ID"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Student(name=row[1], email=row[2], student_id=row[0])
        return None
    
    def delete(self, student_id: str):
        """Supprime un étudiant"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()


# === Génération de rapports : Responsabilité séparée ===

class StudentReportGenerator:
    """
    ✅ Responsabilité unique: Générer des rapports sur les étudiants
    """
    
    def generate_text_report(self, student: Student) -> str:
        """Génère un rapport texte"""
        report = f"{'=' * 50}\n"
        report += f"RAPPORT ÉTUDIANT\n"
        report += f"{'=' * 50}\n"
        report += f"Nom: {student.name}\n"
        report += f"ID: {student.student_id}\n"
        report += f"Email: {student.email}\n"
        report += f"Moyenne générale: {student.get_average():.2f}/20\n"
        report += f"\nDétail des notes:\n"
        
        for grade_info in student.grades:
            report += f"  - {grade_info['course']}: {grade_info['grade']}/20\n"
        
        report += f"{'=' * 50}\n"
        return report
    
    def generate_json_report(self, student: Student) -> str:
        """Génère un rapport JSON"""
        return json.dumps({
            'name': student.name,
            'email': student.email,
            'student_id': student.student_id,
            'average': student.get_average(),
            'grades': student.grades
        }, indent=2)
    
    def generate_html_report(self, student: Student) -> str:
        """Génère un rapport HTML"""
        html = f"""
        <div class="student-report">
            <h2>{student.name}</h2>
            <p>ID: {student.student_id}</p>
            <p>Email: {student.email}</p>
            <p>Moyenne: {student.get_average():.2f}/20</p>
            <ul>
        """
        for grade_info in student.grades:
            html += f"<li>{grade_info['course']}: {grade_info['grade']}/20</li>\n"
        html += "</ul></div>"
        return html


# === Notification : Responsabilité séparée ===

class StudentNotificationService:
    """
    ✅ Responsabilité unique: Envoyer des notifications aux étudiants
    """
    
    def send_welcome_email(self, student: Student):
        """Envoie un email de bienvenue"""
        # Simulation d'envoi d'email
        print(f"📧 Email de bienvenue envoyé à {student.email}")
        print(f"   Destinataire: {student.name}")
    
    def send_grade_notification(self, student: Student, course: str, grade: float):
        """Notifie l'étudiant d'une nouvelle note"""
        print(f"📧 Notification de note envoyée à {student.email}")
        print(f"   {course}: {grade}/20")
    
    def send_report(self, student: Student, report_content: str):
        """Envoie un rapport par email"""
        print(f"📧 Rapport envoyé à {student.email}")


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION DU PRINCIPE SRP")
    print("=" * 70)
    
    # Créer un étudiant
    student = Student(
        name="Marie Lafleur",
        email="marie.lafleur@etudiant.ua.fr",
        student_id="20231234"
    )
    
    # Ajouter des notes
    student.add_grade("POO", 15)
    student.add_grade("Web Dev", 16)
    student.add_grade("Mobile", 14)
    
    # Validation (responsabilité séparée)
    print("\n--- Validation ---")
    validator = StudentValidator()
    is_valid, errors = validator.validate_student(student)
    
    if is_valid:
        print("✓ Étudiant valide")
    else:
        print("✗ Erreurs de validation:")
        for error in errors:
            print(f"  - {error}")
    
    # Persistance (responsabilité séparée)
    print("\n--- Persistance ---")
    repository = StudentRepository(':memory:')  # Base en mémoire pour démo
    repository.save(student)
    print("✓ Étudiant sauvegardé en base de données")
    
    # Génération de rapport (responsabilité séparée)
    print("\n--- Génération de rapport ---")
    report_generator = StudentReportGenerator()
    print(report_generator.generate_text_report(student))
    
    # Notification (responsabilité séparée)
    print("\n--- Notifications ---")
    notifier = StudentNotificationService()
    notifier.send_welcome_email(student)
    notifier.send_grade_notification(student, "POO", 15)
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU SRP:")
    print("- Chaque classe a une responsabilité claire")
    print("- Facile à tester unitairement")
    print("- Modifications isolées (changer le format de rapport n'affecte pas Student)")
    print("- Réutilisable (StudentValidator peut valider d'autres entités)")
    print("=" * 70)
```

**Sortie :**
```
======================================================================
DÉMONSTRATION DU PRINCIPE SRP
======================================================================

--- Validation ---
✓ Étudiant valide

--- Persistance ---
✓ Étudiant sauvegardé en base de données

--- Génération de rapport ---
==================================================
RAPPORT ÉTUDIANT
==================================================
Nom: Marie Lafleur
ID: 20231234
Email: marie.lafleur@etudiant.ua.fr
Moyenne générale: 15.00/20

Détail des notes:
  - POO: 15/20
  - Web Dev: 16/20
  - Mobile: 14/20
==================================================

--- Notifications ---
📧 Email de bienvenue envoyé à marie.lafleur@etudiant.ua.fr
   Destinataire: Marie Lafleur
📧 Notification de note envoyée à marie.lafleur@etudiant.ua.fr
   POO: 15/20

======================================================================
AVANTAGES DU SRP:
- Chaque classe a une responsabilité claire
- Facile à tester unitairement
- Modifications isolées (changer le format de rapport n'affecte pas Student)
- Réutilisable (StudentValidator peut valider d'autres entités)
======================================================================
```

### Comment identifier une violation du SRP ?

**Questions à se poser :**
1. Cette classe a-t-elle plus d'une raison de changer ?
2. Peut-on décrire la classe en une phrase sans utiliser "et" ?
3. La classe a-t-elle des dépendances vers des systèmes externes (BD, email, API) ?

**Signes d'alerte :**
- Classe avec beaucoup de méthodes (>10-15)
- Imports nombreux et variés
- Nom de classe vague (Manager, Handler, Util)
- Difficile à tester sans mocks multiples

---

## 2. Open/Closed Principle (OCP)

### Définition

> **Les entités logicielles doivent être ouvertes à l'extension mais fermées à la modification.**

Autrement dit : On doit pouvoir **ajouter des fonctionnalités** sans **modifier le code existant**.

### Problème à résoudre

Quand on ajoute une fonctionnalité, il faut modifier du code existant :
- Risque de casser ce qui fonctionnait
- Tests à refaire
- Déploiements risqués

### ❌ Violation de l'OCP

```python
class PaymentProcessor:
    """
    ❌ Pour ajouter une nouvelle méthode de paiement,
    il faut MODIFIER cette classe
    """
    
    def process_payment(self, amount: float, method: str, details: dict):
        """Traite un paiement"""
        
        if method == "credit_card":
            # Traitement carte de crédit
            card_number = details['card_number']
            cvv = details['cvv']
            print(f"Paiement CB de {amount}€")
            print(f"Carte: ****{card_number[-4:]}")
            return {"status": "success", "transaction_id": "CC-12345"}
        
        elif method == "paypal":
            # Traitement PayPal
            email = details['email']
            print(f"Paiement PayPal de {amount}€")
            print(f"Compte: {email}")
            return {"status": "success", "transaction_id": "PP-67890"}
        
        elif method == "bank_transfer":
            # Traitement virement
            iban = details['iban']
            print(f"Virement de {amount}€")
            print(f"IBAN: {iban}")
            return {"status": "pending", "transaction_id": "BT-11111"}
        
        # ❌ Pour ajouter Stripe, il faut MODIFIER cette méthode
        # elif method == "stripe":
        #     ...
        
        # ❌ Pour ajouter Apple Pay, il faut MODIFIER cette méthode
        # elif method == "apple_pay":
        #     ...
        
        else:
            raise ValueError(f"Méthode de paiement inconnue: {method}")
```

**Problèmes :**
- Chaque nouveau mode de paiement = modification de la classe
- Risque de casser les méthodes existantes
- Violation du SRP (trop de responsabilités)
- Code difficile à tester

### ✅ Respect de l'OCP

```python
from abc import ABC, abstractmethod
from typing import Dict


# === Interface (abstraction) ===

class PaymentMethod(ABC):
    """
    Interface pour les méthodes de paiement
    ✅ Ouvert à l'extension (nouvelle classe)
    ✅ Fermé à la modification (pas besoin de changer cette interface)
    """
    
    @abstractmethod
    def process(self, amount: float, details: Dict) -> Dict:
        """
        Traite un paiement
        Returns: dict avec status et transaction_id
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retourne le nom de la méthode"""
        pass


# === Implémentations concrètes ===

class CreditCardPayment(PaymentMethod):
    """Paiement par carte de crédit"""
    
    def process(self, amount: float, details: Dict) -> Dict:
        card_number = details['card_number']
        cvv = details['cvv']
        
        print(f"💳 Paiement CB de {amount}€")
        print(f"   Carte: ****{card_number[-4:]}")
        
        # Logique spécifique carte de crédit
        return {
            "status": "success",
            "transaction_id": f"CC-{card_number[-4:]}",
            "method": self.get_name()
        }
    
    def get_name(self) -> str:
        return "Carte de Crédit"


class PayPalPayment(PaymentMethod):
    """Paiement via PayPal"""
    
    def process(self, amount: float, details: Dict) -> Dict:
        email = details['email']
        
        print(f"💰 Paiement PayPal de {amount}€")
        print(f"   Compte: {email}")
        
        # Logique spécifique PayPal
        return {
            "status": "success",
            "transaction_id": f"PP-{hash(email) % 100000}",
            "method": self.get_name()
        }
    
    def get_name(self) -> str:
        return "PayPal"


class BankTransferPayment(PaymentMethod):
    """Paiement par virement bancaire"""
    
    def process(self, amount: float, details: Dict) -> Dict:
        iban = details['iban']
        
        print(f"🏦 Virement de {amount}€")
        print(f"   IBAN: {iban}")
        
        # Les virements prennent du temps
        return {
            "status": "pending",
            "transaction_id": f"BT-{iban[-4:]}",
            "method": self.get_name(),
            "estimated_days": 3
        }
    
    def get_name(self) -> str:
        return "Virement Bancaire"


# ✅ NOUVELLE méthode sans MODIFIER le code existant
class StripePayment(PaymentMethod):
    """Paiement via Stripe"""
    
    def process(self, amount: float, details: Dict) -> Dict:
        token = details['stripe_token']
        
        print(f"⚡ Paiement Stripe de {amount}€")
        print(f"   Token: {token[:10]}...")
        
        return {
            "status": "success",
            "transaction_id": f"STRIPE-{token[-6:]}",
            "method": self.get_name()
        }
    
    def get_name(self) -> str:
        return "Stripe"


# ✅ NOUVELLE méthode sans MODIFIER le code existant
class ApplePayPayment(PaymentMethod):
    """Paiement via Apple Pay"""
    
    def process(self, amount: float, details: Dict) -> Dict:
        device_id = details['device_id']
        
        print(f"🍎 Paiement Apple Pay de {amount}€")
        print(f"   Appareil: {device_id}")
        
        return {
            "status": "success",
            "transaction_id": f"APPLE-{device_id[-6:]}",
            "method": self.get_name()
        }
    
    def get_name(self) -> str:
        return "Apple Pay"


# === Processeur de paiement (utilise le polymorphisme) ===

class PaymentProcessor:
    """
    ✅ Cette classe n'a JAMAIS besoin d'être modifiée
    pour ajouter de nouvelles méthodes de paiement
    """
    
    def __init__(self):
        self.payment_methods: Dict[str, PaymentMethod] = {}
    
    def register_payment_method(self, key: str, method: PaymentMethod):
        """Enregistre une méthode de paiement"""
        self.payment_methods[key] = method
        print(f"✓ Méthode '{method.get_name()}' enregistrée")
    
    def process_payment(self, amount: float, method_key: str, details: Dict) -> Dict:
        """Traite un paiement"""
        
        if method_key not in self.payment_methods:
            raise ValueError(f"Méthode inconnue: {method_key}")
        
        payment_method = self.payment_methods[method_key]
        return payment_method.process(amount, details)
    
    def list_available_methods(self):
        """Liste les méthodes disponibles"""
        print("\n📋 Méthodes de paiement disponibles:")
        for key, method in self.payment_methods.items():
            print(f"  - {key}: {method.get_name()}")


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION DU PRINCIPE OCP")
    print("=" * 70)
    
    # Créer le processeur
    processor = PaymentProcessor()
    
    # Enregistrer les méthodes de paiement
    print("\n--- Enregistrement des méthodes ---")
    processor.register_payment_method("credit_card", CreditCardPayment())
    processor.register_payment_method("paypal", PayPalPayment())
    processor.register_payment_method("bank_transfer", BankTransferPayment())
    
    # ✅ Ajouter Stripe SANS modifier PaymentProcessor
    processor.register_payment_method("stripe", StripePayment())
    
    # ✅ Ajouter Apple Pay SANS modifier PaymentProcessor
    processor.register_payment_method("apple_pay", ApplePayPayment())
    
    # Lister les méthodes
    processor.list_available_methods()
    
    # Traiter des paiements
    print("\n--- Traitement de paiements ---\n")
    
    result1 = processor.process_payment(
        50.00,
        "credit_card",
        {"card_number": "1234567890123456", "cvv": "123"}
    )
    print(f"Résultat: {result1}\n")
    
    result2 = processor.process_payment(
        75.50,
        "stripe",
        {"stripe_token": "tok_1234567890abcdef"}
    )
    print(f"Résultat: {result2}\n")
    
    result3 = processor.process_payment(
        100.00,
        "apple_pay",
        {"device_id": "iPhone-XYZ-123"}
    )
    print(f"Résultat: {result3}\n")
    
    print("=" * 70)
    print("AVANTAGES DE L'OCP:")
    print("- Nouvelles méthodes ajoutées SANS modifier le code existant")
    print("- Aucun risque de casser les méthodes qui fonctionnent")
    print("- Tests existants toujours valides")
    print("- Extension facile et sûre")
    print("=" * 70)
```

**Sortie :**
```
======================================================================
DÉMONSTRATION DU PRINCIPE OCP
======================================================================

--- Enregistrement des méthodes ---
✓ Méthode 'Carte de Crédit' enregistrée
✓ Méthode 'PayPal' enregistrée
✓ Méthode 'Virement Bancaire' enregistrée
✓ Méthode 'Stripe' enregistrée
✓ Méthode 'Apple Pay' enregistrée

📋 Méthodes de paiement disponibles:
  - credit_card: Carte de Crédit
  - paypal: PayPal
  - bank_transfer: Virement Bancaire
  - stripe: Stripe
  - apple_pay: Apple Pay

--- Traitement de paiements ---

💳 Paiement CB de 50.0€
   Carte: ****3456
Résultat: {'status': 'success', 'transaction_id': 'CC-3456', 'method': 'Carte de Crédit'}

⚡ Paiement Stripe de 75.5€
   Token: tok_123456...
Résultat: {'status': 'success', 'transaction_id': 'STRIPE-bcdef', 'method': 'Stripe'}

🍎 Paiement Apple Pay de 100.0€
   Appareil: iPhone-XYZ-123
Résultat: {'status': 'success', 'transaction_id': 'APPLE-XYZ-12', 'method': 'Apple Pay'}

======================================================================
AVANTAGES DE L'OCP:
- Nouvelles méthodes ajoutées SANS modifier le code existant
- Aucun risque de casser les méthodes qui fonctionnent
- Tests existants toujours valides
- Extension facile et sûre
======================================================================
```

### Techniques pour respecter l'OCP

1. **Héritage et polymorphisme** (comme ci-dessus)
2. **Design patterns** : Strategy, Decorator, Factory
3. **Injection de dépendances**
4. **Configuration externe** (fichiers, base de données)

### Lien avec les Design Patterns

- **Strategy Pattern** = Application directe de l'OCP
- **Decorator Pattern** = Extension sans modification
- **Factory Pattern** = Ajout de types sans modifier la factory

---

## 3. Liskov Substitution Principle (LSP)

### Définition

> **Les objets d'une classe dérivée doivent pouvoir remplacer les objets de la classe de base sans altérer le bon fonctionnement du programme.**

Autrement dit : **Si S est un sous-type de T, alors les objets de type T peuvent être remplacés par des objets de type S sans changer les propriétés désirables du programme.**

### Problème à résoudre

Une classe dérivée qui ne respecte pas le contrat de la classe de base :
- Comportement inattendu
- Bugs difficiles à détecter
- Code client doit connaître les types spécifiques

### ❌ Violation du LSP

```python
class Bird:
    """Classe de base pour les oiseaux"""
    
    def __init__(self, name: str):
        self.name = name
    
    def fly(self):
        """Tous les oiseaux volent... ou pas ?"""
        print(f"{self.name} vole dans le ciel")


class Sparrow(Bird):
    """Moineau - peut voler ✓"""
    
    def fly(self):
        print(f"{self.name} vole rapidement")


class Penguin(Bird):
    """
    ❌ Pingouin - NE PEUT PAS voler !
    Violation du LSP car Penguin ne peut pas remplacer Bird
    """
    
    def fly(self):
        # ❌ Lève une exception ou comportement inattendu
        raise Exception(f"{self.name} ne peut pas voler!")


# Code client qui attend que tous les oiseaux volent
def make_birds_fly(birds: list[Bird]):
    """Fait voler tous les oiseaux"""
    for bird in birds:
        bird.fly()  # ❌ Crash avec Penguin!


# Utilisation
birds = [
    Sparrow("Moineau"),
    Sparrow("Hirondelle"),
    Penguin("Tux")  # ❌ Va causer un crash
]

# make_birds_fly(birds)  # ❌ Exception!
```

### ✅ Respect du LSP

```python
from abc import ABC, abstractmethod


# === Solution 1: Revoir la hiérarchie ===

class Bird(ABC):
    """
    ✅ Classe de base sans assomptions sur le vol
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def move(self):
        """Tous les oiseaux se déplacent (abstrait)"""
        pass
    
    def eat(self):
        """Tous les oiseaux mangent"""
        print(f"{self.name} mange")


class FlyingBird(Bird):
    """
    ✅ Oiseaux qui peuvent voler
    """
    
    def move(self):
        self.fly()
    
    def fly(self):
        """Comportement de vol"""
        print(f"{self.name} vole")


class FlightlessBird(Bird):
    """
    ✅ Oiseaux qui ne volent pas
    """
    
    def move(self):
        self.walk()
    
    def walk(self):
        """Comportement de marche"""
        print(f"{self.name} marche")


# Implémentations concrètes
class Sparrow(FlyingBird):
    """Moineau"""
    
    def fly(self):
        print(f"🐦 {self.name} vole rapidement")


class Eagle(FlyingBird):
    """Aigle"""
    
    def fly(self):
        print(f"🦅 {self.name} plane majestueusement")


class Penguin(FlightlessBird):
    """Pingouin"""
    
    def walk(self):
        print(f"🐧 {self.name} se dandine")
    
    def swim(self):
        """Comportement spécifique: nager"""
        print(f"🐧 {self.name} nage sous l'eau")


class Ostrich(FlightlessBird):
    """Autruche"""
    
    def walk(self):
        print(f"🦤 {self.name} court très vite")


# === Code client qui respecte le LSP ===

def make_birds_move(birds: list[Bird]):
    """
    ✅ Fonctionne avec TOUS les oiseaux
    car on utilise la méthode abstraite move()
    """
    for bird in birds:
        bird.move()  # Polymorphisme correct


def make_flying_birds_fly(birds: list[FlyingBird]):
    """
    ✅ Spécifique aux oiseaux volants
    """
    for bird in birds:
        bird.fly()


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION DU PRINCIPE LSP")
    print("=" * 70)
    
    # Tous les oiseaux
    all_birds = [
        Sparrow("Moineau"),
        Eagle("Aigle"),
        Penguin("Tux"),
        Ostrich("Oscar")
    ]
    
    print("\n--- Tous les oiseaux se déplacent ---")
    make_birds_move(all_birds)  # ✅ Fonctionne!
    
    # Seulement les oiseaux volants
    flying_birds = [
        Sparrow("Piou"),
        Eagle("Grand Aigle")
    ]
    
    print("\n--- Oiseaux volants uniquement ---")
    make_flying_birds_fly(flying_birds)  # ✅ Fonctionne!
    
    # Démonstration des capacités spécifiques
    print("\n--- Capacités spécifiques ---")
    penguin = Penguin("Pingu")
    penguin.walk()
    penguin.swim()  # Capacité spécifique aux pingouins
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU LSP:")
    print("- Hiérarchie logique et cohérente")
    print("- Pas de surprises dans le code client")
    print("- Polymorphisme qui fonctionne correctement")
    print("- Chaque type peut être utilisé de manière sûre")
    print("=" * 70)
```

### Exemple pratique : Formes géométriques

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Forme géométrique de base"""
    
    @abstractmethod
    def area(self) -> float:
        """Calcule l'aire"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calcule le périmètre"""
        pass


class Rectangle(Shape):
    """Rectangle"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def set_width(self, width: float):
        self.width = width
    
    def set_height(self, height: float):
        self.height = height


# ❌ Violation du LSP classique
class Square(Rectangle):
    """
    ❌ Un carré EST-IL vraiment un rectangle en POO ?
    Mathématiquement oui, mais en POO...
    """
    
    def set_width(self, width: float):
        # ❌ Change aussi la hauteur
        self.width = width
        self.height = width  # Maintient le carré
    
    def set_height(self, height: float):
        # ❌ Change aussi la largeur
        self.width = height  # Maintient le carré
        self.height = height


# Test qui échoue
def test_rectangle(rect: Rectangle):
    """
    ❌ Ce test fonctionne pour Rectangle mais PAS pour Square
    """
    rect.set_width(5)
    rect.set_height(4)
    
    expected_area = 5 * 4  # 20
    actual_area = rect.area()
    
    assert expected_area == actual_area, f"Attendu {expected_area}, obtenu {actual_area}"


# ✅ Solution: Composition plutôt qu'héritage
class Square(Shape):
    """✅ Square comme classe indépendante"""
    
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2
    
    def perimeter(self) -> float:
        return 4 * self.side
    
    def set_side(self, side: float):
        self.side = side
```

### Règles pour respecter le LSP

1. **Préconditions** : Une sous-classe ne peut pas renforcer les préconditions
2. **Postconditions** : Une sous-classe ne peut pas affaiblir les postconditions
3. **Invariants** : Les invariants de la classe de base doivent être préservés
4. **Exceptions** : Une sous-classe ne devrait pas lever de nouvelles exceptions

---

## 4. Interface Segregation Principle (ISP)

### Définition

> **Les clients ne doivent pas être forcés de dépendre d'interfaces qu'ils n'utilisent pas.**

Autrement dit : **Plusieurs interfaces spécifiques valent mieux qu'une seule interface générale.**

### Problème à résoudre

Une grosse interface avec beaucoup de méthodes force les classes à implémenter des méthodes dont elles n'ont pas besoin.

### ❌ Violation de l'ISP

```python
from abc import ABC, abstractmethod


class Worker(ABC):
    """
    ❌ Interface "fourre-tout" avec trop de méthodes
    """
    
    @abstractmethod
    def work(self):
        """Travailler"""
        pass
    
    @abstractmethod
    def eat(self):
        """Manger"""
        pass
    
    @abstractmethod
    def sleep(self):
        """Dormir"""
        pass
    
    @abstractmethod
    def attend_meeting(self):
        """Assister à une réunion"""
        pass
    
    @abstractmethod
    def write_code(self):
        """Écrire du code"""
        pass


class HumanWorker(Worker):
    """✓ Humain - toutes les méthodes ont du sens"""
    
    def work(self):
        print("Travaille sur un projet")
    
    def eat(self):
        print("Mange au réfectoire")
    
    def sleep(self):
        print("Dort 8 heures")
    
    def attend_meeting(self):
        print("Participe à la réunion")
    
    def write_code(self):
        print("Code en Python")


class RobotWorker(Worker):
    """
    ❌ Robot - certaines méthodes n'ont PAS de sens
    """
    
    def work(self):
        print("Exécute des tâches automatisées")
    
    def eat(self):
        # ❌ Un robot ne mange pas!
        raise NotImplementedError("Les robots ne mangent pas")
    
    def sleep(self):
        # ❌ Un robot ne dort pas!
        raise NotImplementedError("Les robots ne dorment pas")
    
    def attend_meeting(self):
        # ❌ Un robot n'assiste pas aux réunions!
        raise NotImplementedError("Les robots ne vont pas en réunion")
    
    def write_code(self):
        print("Génère du code automatiquement")
```

**Problème :** RobotWorker est forcé d'implémenter des méthodes qu'il ne peut pas réaliser.

### ✅ Respect de l'ISP

```python
from abc import ABC, abstractmethod


# === Interfaces ségrégées (spécifiques) ===

class Workable(ABC):
    """Interface pour le travail"""
    
    @abstractmethod
    def work(self):
        pass


class Eatable(ABC):
    """Interface pour manger"""
    
    @abstractmethod
    def eat(self):
        pass


class Sleepable(ABC):
    """Interface pour dormir"""
    
    @abstractmethod
    def sleep(self):
        pass


class MeetingAttendable(ABC):
    """Interface pour les réunions"""
    
    @abstractmethod
    def attend_meeting(self):
        pass


class Codeable(ABC):
    """Interface pour coder"""
    
    @abstractmethod
    def write_code(self):
        pass


# === Implémentations ===

class HumanWorker(Workable, Eatable, Sleepable, MeetingAttendable, Codeable):
    """
    ✅ Humain implémente toutes les interfaces qui le concernent
    """
    
    def __init__(self, name: str):
        self.name = name
    
    def work(self):
        print(f"{self.name} travaille sur un projet")
    
    def eat(self):
        print(f"{self.name} mange au réfectoire")
    
    def sleep(self):
        print(f"{self.name} dort 8 heures")
    
    def attend_meeting(self):
        print(f"{self.name} participe à la réunion")
    
    def write_code(self):
        print(f"{self.name} code en Python")


class RobotWorker(Workable, Codeable):
    """
    ✅ Robot implémente SEULEMENT les interfaces qui le concernent
    """
    
    def __init__(self, model: str):
        self.model = model
    
    def work(self):
        print(f"Robot {self.model} exécute des tâches automatisées")
    
    def write_code(self):
        print(f"Robot {self.model} génère du code automatiquement")


class Manager(Workable, Eatable, Sleepable, MeetingAttendable):
    """
    ✅ Manager ne code pas, mais participe aux réunions
    """
    
    def __init__(self, name: str):
        self.name = name
    
    def work(self):
        print(f"{self.name} gère l'équipe")
    
    def eat(self):
        print(f"{self.name} déjeune avec l'équipe")
    
    def sleep(self):
        print(f"{self.name} dort (trop peu)")
    
    def attend_meeting(self):
        print(f"{self.name} organise la réunion")


# === Code client ===

def make_workers_work(workers: list[Workable]):
    """Fait travailler tous les workers"""
    for worker in workers:
        worker.work()


def feed_workers(eaters: list[Eatable]):
    """Nourrit les workers qui mangent"""
    for eater in eaters:
        eater.eat()


def organize_meeting(attendees: list[MeetingAttendable]):
    """Organise une réunion"""
    for attendee in attendees:
        attendee.attend_meeting()


def code_sprint(coders: list[Codeable]):
    """Sprint de code"""
    for coder in coders:
        coder.write_code()


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION DU PRINCIPE ISP")
    print("=" * 70)
    
    # Créer les workers
    alice = HumanWorker("Alice")
    bob = HumanWorker("Bob")
    robot1 = RobotWorker("R2D2")
    manager = Manager("Charlie")
    
    # Faire travailler tout le monde
    print("\n--- Tout le monde travaille ---")
    all_workers = [alice, bob, robot1, manager]
    make_workers_work(all_workers)
    
    # Nourrir seulement ceux qui mangent
    print("\n--- Pause déjeuner (seulement les humains) ---")
    eaters = [alice, bob, manager]  # ✅ Robot exclu automatiquement
    feed_workers(eaters)
    
    # Réunion (seulement ceux qui y participent)
    print("\n--- Réunion d'équipe ---")
    meeting_attendees = [alice, bob, manager]  # ✅ Robot exclu
    organize_meeting(meeting_attendees)
    
    # Sprint de code
    print("\n--- Sprint de développement ---")
    coders = [alice, bob, robot1]  # ✅ Manager exclu
    code_sprint(coders)
    
    print("\n" + "=" * 70)
    print("AVANTAGES DE L'ISP:")
    print("- Chaque worker implémente seulement ce qui le concerne")
    print("- Pas de méthodes non implémentées ou levant des exceptions")
    print("- Code client flexible et type-safe")
    print("- Facile d'ajouter de nouveaux types de workers")
    print("=" * 70)
```

**Sortie :**
```
======================================================================
DÉMONSTRATION DU PRINCIPE ISP
======================================================================

--- Tout le monde travaille ---
Alice travaille sur un projet
Bob travaille sur un projet
Robot R2D2 exécute des tâches automatisées
Charlie gère l'équipe

--- Pause déjeuner (seulement les humains) ---
Alice mange au réfectoire
Bob mange au réfectoire
Charlie déjeune avec l'équipe

--- Réunion d'équipe ---
Alice participe à la réunion
Bob participe à la réunion
Charlie organise la réunion

--- Sprint de développement ---
Alice code en Python
Bob code en Python
Robot R2D2 génère du code automatiquement

======================================================================
AVANTAGES DE L'ISP:
- Chaque worker implémente seulement ce qui le concerne
- Pas de méthodes non implémentées ou levant des exceptions
- Code client flexible et type-safe
- Facile d'ajouter de nouveaux types de workers
======================================================================
```

### Exemple pratique : Document et imprimantes

```python
# ❌ Violation ISP
class Printer(ABC):
    @abstractmethod
    def print(self, document): pass
    
    @abstractmethod
    def scan(self, document): pass
    
    @abstractmethod
    def fax(self, document): pass


# SimplePrinter forcé d'implémenter scan et fax
class SimplePrinter(Printer):
    def print(self, document):
        print(f"Impression: {document}")
    
    def scan(self, document):
        raise NotImplementedError("Pas de scanner")
    
    def fax(self, document):
        raise NotImplementedError("Pas de fax")


# ✅ Respect ISP
class Printable(ABC):
    @abstractmethod
    def print(self, document): pass


class Scannable(ABC):
    @abstractmethod
    def scan(self, document): pass


class Faxable(ABC):
    @abstractmethod
    def fax(self, document): pass


class SimplePrinter(Printable):
    def print(self, document):
        print(f"Impression: {document}")


class MultiFunctionPrinter(Printable, Scannable, Faxable):
    def print(self, document):
        print(f"Impression: {document}")
    
    def scan(self, document):
        print(f"Scan: {document}")
    
    def fax(self, document):
        print(f"Fax: {document}")
```

---

## 5. Dependency Inversion Principle (DIP)

### Définition

> **Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre d'abstractions.**
>
> **Les abstractions ne doivent pas dépendre des détails. Les détails doivent dépendre des abstractions.**

Autrement dit :
1. Dépendez des **interfaces**, pas des **implémentations**
2. Les **abstractions** sont stables, les **détails** changent

### Problème à résoudre

Couplage fort entre les couches de l'application :
- Difficile à tester
- Difficile à changer d'implémentation
- Rigide et fragile

### ❌ Violation du DIP

```python
import sqlite3


# Bas niveau: Implémentation concrète
class SQLiteDatabase:
    """❌ Implémentation concrète de base de données"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def close(self):
        if self.connection:
            self.connection.close()


# Haut niveau: Dépend directement de SQLiteDatabase
class StudentRepository:
    """
    ❌ Dépend d'une implémentation concrète (SQLiteDatabase)
    Impossible de changer de BD sans modifier cette classe
    """
    
    def __init__(self):
        # ❌ Couplage fort avec SQLiteDatabase
        self.db = SQLiteDatabase('students.db')
        self.db.connect()
    
    def save_student(self, student_id: str, name: str, email: str):
        query = f"INSERT INTO students VALUES ('{student_id}', '{name}', '{email}')"
        self.db.execute_query(query)
    
    def find_student(self, student_id: str):
        query = f"SELECT * FROM students WHERE student_id = '{student_id}'"
        return self.db.execute_query(query)
```

**Problèmes :**
- StudentRepository ne peut pas utiliser PostgreSQL ou MySQL
- Impossible de tester sans vraie base de données
- Changement de BD = modification de StudentRepository

### ✅ Respect du DIP

```python
from abc import ABC, abstractmethod
from typing import List, Tuple, Any


# === ABSTRACTION (Interface) ===

class Database(ABC):
    """
    ✅ Abstraction stable
    Ni haut niveau ni bas niveau ne dépendent des détails
    """
    
    @abstractmethod
    def connect(self):
        """Établit la connexion"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        """Exécute une requête"""
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: Tuple = None):
        """Exécute une mise à jour"""
        pass
    
    @abstractmethod
    def close(self):
        """Ferme la connexion"""
        pass


# === DÉTAILS (Implémentations concrètes) ===

class SQLiteDatabase(Database):
    """✅ Implémentation SQLite dépend de l'abstraction"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect(self.db_path)
        print(f"✓ Connecté à SQLite: {self.db_path}")
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    
    def execute_update(self, query: str, params: Tuple = None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("✓ Connexion SQLite fermée")


class PostgreSQLDatabase(Database):
    """✅ Implémentation PostgreSQL dépend de l'abstraction"""
    
    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        # Simulation (psycopg2 nécessaire en réel)
        print(f"✓ Connecté à PostgreSQL: {self.database}@{self.host}")
        # import psycopg2
        # self.connection = psycopg2.connect(...)
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        # Simulation
        print(f"[PostgreSQL] Query: {query}")
        return []
    
    def execute_update(self, query: str, params: Tuple = None):
        # Simulation
        print(f"[PostgreSQL] Update: {query}")
    
    def close(self):
        print("✓ Connexion PostgreSQL fermée")


class InMemoryDatabase(Database):
    """✅ Implémentation en mémoire pour les tests"""
    
    def __init__(self):
        self.data = {}  # Simule une BD en mémoire
    
    def connect(self):
        print("✓ Base de données en mémoire initialisée")
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        print(f"[InMemory] Query: {query}")
        # Logique simplifiée pour la démo
        if "SELECT" in query:
            return list(self.data.values())
        return []
    
    def execute_update(self, query: str, params: Tuple = None):
        print(f"[InMemory] Update: {query}")
        if params and "INSERT" in query:
            self.data[params[0]] = params
    
    def close(self):
        print("✓ Base de données en mémoire libérée")


# === HAUT NIVEAU (dépend de l'abstraction) ===

class StudentRepository:
    """
    ✅ Dépend de l'abstraction Database, pas d'une implémentation
    """
    
    def __init__(self, database: Database):
        # ✅ Injection de dépendance
        self.db = database
        self.db.connect()
        self._create_table()
    
    def _create_table(self):
        """Crée la table si elle n'existe pas"""
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT
        )
        """
        try:
            self.db.execute_update(query)
        except:
            pass  # Table peut déjà exister
    
    def save_student(self, student_id: str, name: str, email: str):
        """Sauvegarde un étudiant"""
        query = "INSERT OR REPLACE INTO students VALUES (?, ?, ?)"
        self.db.execute_update(query, (student_id, name, email))
        print(f"✓ Étudiant {name} sauvegardé")
    
    def find_student(self, student_id: str) -> Tuple:
        """Trouve un étudiant par ID"""
        query = "SELECT * FROM students WHERE student_id = ?"
        results = self.db.execute_query(query, (student_id,))
        return results[0] if results else None
    
    def get_all_students(self) -> List[Tuple]:
        """Récupère tous les étudiants"""
        query = "SELECT * FROM students"
        return self.db.execute_query(query)
    
    def close(self):
        """Ferme la connexion"""
        self.db.close()


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION DU PRINCIPE DIP")
    print("=" * 70)
    
    # Scenario 1: Utilisation avec SQLite
    print("\n--- Scénario 1: SQLite ---")
    sqlite_db = SQLiteDatabase(':memory:')
    repo_sqlite = StudentRepository(sqlite_db)
    
    repo_sqlite.save_student("20231001", "Alice Dupont", "alice@ua.fr")
    repo_sqlite.save_student("20231002", "Bob Martin", "bob@ua.fr")
    
    students = repo_sqlite.get_all_students()
    print(f"Nombre d'étudiants: {len(students)}")
    repo_sqlite.close()
    
    # Scenario 2: Changement vers PostgreSQL (aucune modification du Repository!)
    print("\n--- Scénario 2: PostgreSQL (changement transparent) ---")
    # ✅ Même code client, différente implémentation
    postgres_db = PostgreSQLDatabase(
        host="localhost",
        database="campus_db",
        user="admin",
        password="secret"
    )
    repo_postgres = StudentRepository(postgres_db)
    repo_postgres.save_student("20231003", "Charlie Leroy", "charlie@ua.fr")
    repo_postgres.close()
    
    # Scenario 3: Tests avec InMemory (pas besoin de vraie BD!)
    print("\n--- Scénario 3: Tests avec base en mémoire ---")
    # ✅ Tests rapides sans dépendances externes
    test_db = InMemoryDatabase()
    repo_test = StudentRepository(test_db)
    repo_test.save_student("TEST001", "Test Student", "test@ua.fr")
    repo_test.close()
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU DIP:")
    print("- Repository indépendant de l'implémentation de BD")
    print("- Facile de changer de BD sans toucher au Repository")
    print("- Tests faciles avec InMemoryDatabase")
    print("- Code flexible et découplé")
    print("=" * 70)
```

**Sortie :**
```
======================================================================
DÉMONSTRATION DU PRINCIPE DIP
======================================================================

--- Scénario 1: SQLite ---
✓ Connecté à SQLite: :memory:
✓ Étudiant Alice Dupont sauvegardé
✓ Étudiant Bob Martin sauvegardé
Nombre d'étudiants: 2
✓ Connexion SQLite fermée

--- Scénario 2: PostgreSQL (changement transparent) ---
✓ Connecté à PostgreSQL: campus_db@localhost
[PostgreSQL] Update: INSERT OR REPLACE INTO students VALUES (?, ?, ?)
✓ Étudiant Charlie Leroy sauvegardé
✓ Connexion PostgreSQL fermée

--- Scénario 3: Tests avec base en mémoire ---
✓ Base de données en mémoire initialisée
[InMemory] Update: INSERT OR REPLACE INTO students VALUES (?, ?, ?)
✓ Étudiant Test Student sauvegardé
✓ Base de données en mémoire libérée

======================================================================
AVANTAGES DU DIP:
- Repository indépendant de l'implémentation de BD
- Facile de changer de BD sans toucher au Repository
- Tests faciles avec InMemoryDatabase
- Code flexible et découplé
======================================================================
```

### Techniques pour appliquer le DIP

1. **Dependency Injection** (comme ci-dessus)
2. **Factory Pattern**
3. **Service Locator Pattern**
4. **IoC Containers** (Inversion of Control)

### Exemple avec Injection de Dépendances

```python
# ❌ Sans DI
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Couplage fort
        self.email = GmailSender()  # Couplage fort


# ✅ Avec DI
class UserService:
    def __init__(self, database: Database, email_sender: EmailSender):
        self.db = database  # ✅ Dépend de l'abstraction
        self.email = email_sender  # ✅ Dépend de l'abstraction


# Configuration (dans un fichier séparé ou main)
def create_user_service():
    db = MySQLDatabase()  # ou PostgreSQLDatabase()
    email = GmailSender()  # ou SendGridSender()
    return UserService(db, email)
```

---

## 6. Synthèse et Exercices Pratiques

[La suite dans le prochain message...]