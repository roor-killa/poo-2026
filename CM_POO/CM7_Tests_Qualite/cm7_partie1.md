# CM7 - Tests et Qualité de Code (Partie 1)
## Tests Unitaires, TDD et Coverage

---

## Introduction

### Rappel des cours précédents

**CM1-CM3 :** Fondamentaux POO (Classes, Héritage, Polymorphisme)  
**CM4 :** Design Patterns  
**CM5 :** Principes SOLID  
**CM6 :** Architecture Logicielle  

**Aujourd'hui - CM7 :**
- **Tests unitaires** : pytest, unittest
- **TDD** : Test-Driven Development
- **Mocking** : Simuler les dépendances
- **Coverage** : Mesurer la couverture de code
- **Tests d'intégration** : Tester les interactions
- **Qualité de code** : Linting, formatage

---

## 1. Pourquoi Tester ?

### 1.1 Les Problèmes sans Tests

```python
# ❌ Code sans tests
class Calculator:
    def divide(self, a, b):
        return a / b  # Que se passe-t-il si b=0 ?

# Utilisation en production
calc = Calculator()
result = calc.divide(10, 0)  # 💥 CRASH !
```

**Problèmes :**
- ❌ Bugs en production
- ❌ Peur de modifier le code
- ❌ Régressions lors des changements
- ❌ Documentation inexistante
- ❌ Confiance faible dans le code

### 1.2 Les Avantages des Tests

```python
# ✅ Code avec tests
class Calculator:
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division par zéro impossible")
        return a / b


# Tests
def test_divide_normal():
    calc = Calculator()
    assert calc.divide(10, 2) == 5

def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, 0)
```

**Avantages :**
- ✅ Détection précoce des bugs
- ✅ Confiance pour refactorer
- ✅ Documentation vivante
- ✅ Design meilleur (testable = modulaire)
- ✅ Régression impossible

---

## 2. Types de Tests

### Pyramide des Tests

```
           /\
          /  \
         / E2E \        ← Tests End-to-End (lents, peu nombreux)
        /--------\
       /          \
      / Intégration \   ← Tests d'intégration (moyens)
     /--------------\
    /                \
   /   Tests          \  ← Tests unitaires (rapides, nombreux)
  /    Unitaires       \
 /______________________\
```

### 2.1 Tests Unitaires

> **Testent une fonction/méthode isolée, sans dépendances externes.**

**Caractéristiques :**
- ⚡ Très rapides (millisecondes)
- 🔒 Isolés (pas de BD, réseau, fichiers)
- 🎯 Focalisés (une seule fonctionnalité)

```python
# Exemple : Test unitaire d'une fonction pure
def test_calculate_average():
    # Arrange
    grades = [15, 16, 14]
    
    # Act
    result = calculate_average(grades)
    
    # Assert
    assert result == 15.0
```

### 2.2 Tests d'Intégration

> **Testent l'interaction entre plusieurs composants.**

```python
# Exemple : Test d'intégration avec base de données
def test_save_and_retrieve_student():
    # Arrange
    db = Database()
    student = Student("Marie", "marie@ua.fr")
    
    # Act
    db.save(student)
    retrieved = db.find_by_id(student.id)
    
    # Assert
    assert retrieved.name == "Marie"
```

### 2.3 Tests End-to-End (E2E)

> **Testent l'application complète, du début à la fin.**

```python
# Exemple : Test E2E d'une API
def test_complete_user_workflow():
    # 1. Inscription
    response = client.post("/register", data={"email": "marie@ua.fr"})
    assert response.status_code == 201
    
    # 2. Connexion
    response = client.post("/login", data={"email": "marie@ua.fr"})
    token = response.json()["token"]
    
    # 3. Utilisation
    response = client.get("/profile", headers={"Authorization": token})
    assert response.json()["email"] == "marie@ua.fr"
```

---

## 3. pytest : Framework de Test Python

### 3.1 Installation et Premiers Tests

```bash
# Installation
pip install pytest pytest-cov

# Structure de projet
project/
├── src/
│   └── calculator.py
└── tests/
    └── test_calculator.py
```

**calculator.py :**
```python
class Calculator:
    """Calculatrice simple"""
    
    def add(self, a: float, b: float) -> float:
        """Addition"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Soustraction"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Division"""
        if b == 0:
            raise ValueError("Division par zéro impossible")
        return a / b
```

**test_calculator.py :**
```python
import pytest
from src.calculator import Calculator


class TestCalculator:
    """Tests de la calculatrice"""
    
    def setup_method(self):
        """Exécuté avant chaque test"""
        self.calc = Calculator()
    
    def test_add(self):
        """Test de l'addition"""
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0
    
    def test_subtract(self):
        """Test de la soustraction"""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(0, 5) == -5
    
    def test_multiply(self):
        """Test de la multiplication"""
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(0, 100) == 0
    
    def test_divide(self):
        """Test de la division normale"""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        """Test de la division par zéro"""
        with pytest.raises(ValueError, match="Division par zéro"):
            self.calc.divide(10, 0)


# Exécution : pytest tests/
# Ou : pytest tests/ -v (verbose)
```

**Sortie :**
```
======================== test session starts ========================
collected 5 items

tests/test_calculator.py .....                                [100%]

========================= 5 passed in 0.02s =========================
```

### 3.2 Fixtures pytest

> **Les fixtures fournissent des données/objets réutilisables pour les tests.**

```python
import pytest


@pytest.fixture
def calculator():
    """Fixture : crée une calculatrice pour chaque test"""
    return Calculator()


@pytest.fixture
def sample_grades():
    """Fixture : données de test"""
    return [15, 16, 14, 17, 13]


def test_with_fixtures(calculator, sample_grades):
    """Utilisation de fixtures"""
    total = sum(sample_grades)
    avg = calculator.divide(total, len(sample_grades))
    assert avg == 15.0
```

### 3.3 Paramétrage de Tests

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5),
])
def test_add_multiple_cases(calculator, a, b, expected):
    """Test avec plusieurs cas"""
    assert calculator.add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (15, 3, 5),
    (7, 2, 3.5),
    (1, 4, 0.25),
])
def test_divide_multiple_cases(calculator, a, b, expected):
    """Test division avec plusieurs cas"""
    assert calculator.divide(a, b) == expected
```

---

## 4. TDD (Test-Driven Development)

### 4.1 Cycle TDD : Red-Green-Refactor

```
1. 🔴 RED : Écrire un test qui échoue
2. 🟢 GREEN : Écrire le code minimal pour passer le test
3. 🔵 REFACTOR : Améliorer le code sans casser les tests
4. Répéter
```

### 4.2 Exemple Pratique : Classe Student

**Étape 1 - RED : Écrire le test**

```python
# test_student.py
import pytest


def test_student_creation():
    """Test création d'un étudiant"""
    # Ce test va ÉCHOUER (Student n'existe pas encore)
    student = Student("20231001", "Marie Lafleur", "marie@ua.fr")
    
    assert student.student_id == "20231001"
    assert student.name == "Marie Lafleur"
    assert student.email == "marie@ua.fr"
    assert student.grades == []
```

**Exécution :**
```bash
pytest tests/test_student.py
# ❌ FAILED - NameError: name 'Student' is not defined
```

**Étape 2 - GREEN : Code minimal**

```python
# student.py
class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
```

**Exécution :**
```bash
pytest tests/test_student.py
# ✅ PASSED
```

**Étape 3 - Nouveau test (RED)**

```python
def test_add_grade():
    """Test ajout de note"""
    student = Student("20231001", "Marie", "marie@ua.fr")
    
    student.add_grade(15)
    student.add_grade(16)
    
    assert len(student.grades) == 2
    assert 15 in student.grades
    assert 16 in student.grades
```

**Exécution :**
```bash
pytest tests/test_student.py::test_add_grade
# ❌ FAILED - AttributeError: 'Student' object has no attribute 'add_grade'
```

**Étape 4 - GREEN : Implémenter**

```python
class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
    
    def add_grade(self, grade):
        """Ajoute une note"""
        self.grades.append(grade)
```

**Étape 5 - Nouveau test avec validation**

```python
def test_add_grade_validation():
    """Test validation des notes"""
    student = Student("20231001", "Marie", "marie@ua.fr")
    
    # Note valide
    student.add_grade(15)
    assert 15 in student.grades
    
    # Note invalide
    with pytest.raises(ValueError):
        student.add_grade(25)  # > 20
    
    with pytest.raises(ValueError):
        student.add_grade(-5)  # < 0
```

**Implémentation avec validation :**

```python
class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
    
    def add_grade(self, grade):
        """Ajoute une note avec validation"""
        if not 0 <= grade <= 20:
            raise ValueError(f"Note invalide: {grade}. Doit être entre 0 et 20")
        self.grades.append(grade)
    
    def calculate_average(self):
        """Calcule la moyenne"""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)
```

**Étape 6 - Tests complets**

```python
import pytest
from src.student import Student


class TestStudent:
    """Suite de tests complète pour Student"""
    
    @pytest.fixture
    def student(self):
        """Fixture : étudiant pour les tests"""
        return Student("20231001", "Marie Lafleur", "marie@ua.fr")
    
    def test_creation(self, student):
        """Test création"""
        assert student.student_id == "20231001"
        assert student.name == "Marie Lafleur"
        assert student.email == "marie@ua.fr"
        assert student.grades == []
    
    def test_add_grade(self, student):
        """Test ajout de notes valides"""
        student.add_grade(15)
        student.add_grade(16)
        
        assert len(student.grades) == 2
        assert student.grades == [15, 16]
    
    @pytest.mark.parametrize("invalid_grade", [-1, -10, 21, 25, 100])
    def test_add_invalid_grade(self, student, invalid_grade):
        """Test notes invalides"""
        with pytest.raises(ValueError, match="Note invalide"):
            student.add_grade(invalid_grade)
    
    def test_calculate_average_empty(self, student):
        """Test moyenne avec aucune note"""
        assert student.calculate_average() == 0.0
    
    def test_calculate_average(self, student):
        """Test calcul de moyenne"""
        student.add_grade(15)
        student.add_grade(16)
        student.add_grade(14)
        
        assert student.calculate_average() == 15.0
    
    def test_edge_cases(self, student):
        """Test cas limites"""
        # Note minimale
        student.add_grade(0)
        assert 0 in student.grades
        
        # Note maximale
        student.add_grade(20)
        assert 20 in student.grades
```

---

## 5. Exemple Complet : TDD pour une Classe BankAccount

### 5.1 Tests d'abord (TDD)

```python
# tests/test_bank_account.py
import pytest
from src.bank_account import BankAccount


class TestBankAccount:
    """Tests TDD pour BankAccount"""
    
    @pytest.fixture
    def account(self):
        """Fixture : compte avec solde initial"""
        return BankAccount("Marie Lafleur", initial_balance=1000)
    
    # Test 1 : Création
    def test_account_creation(self):
        """Test création de compte"""
        account = BankAccount("Jean Martin", 500)
        
        assert account.owner == "Jean Martin"
        assert account.balance == 500
        assert account.transactions == []
    
    # Test 2 : Dépôt
    def test_deposit(self, account):
        """Test dépôt d'argent"""
        result = account.deposit(500)
        
        assert result is True
        assert account.balance == 1500
        assert len(account.transactions) == 1
        assert account.transactions[0]['type'] == 'DEPOSIT'
        assert account.transactions[0]['amount'] == 500
    
    # Test 3 : Dépôt invalide
    def test_deposit_invalid_amount(self, account):
        """Test dépôt avec montant invalide"""
        with pytest.raises(ValueError, match="Montant invalide"):
            account.deposit(-100)
        
        with pytest.raises(ValueError):
            account.deposit(0)
    
    # Test 4 : Retrait
    def test_withdraw(self, account):
        """Test retrait d'argent"""
        result = account.withdraw(300)
        
        assert result is True
        assert account.balance == 700
        assert len(account.transactions) == 1
    
    # Test 5 : Retrait avec solde insuffisant
    def test_withdraw_insufficient_funds(self, account):
        """Test retrait avec solde insuffisant"""
        with pytest.raises(ValueError, match="Solde insuffisant"):
            account.withdraw(2000)
    
    # Test 6 : Transfert
    def test_transfer(self):
        """Test transfert entre comptes"""
        account1 = BankAccount("Marie", 1000)
        account2 = BankAccount("Jean", 500)
        
        account1.transfer(account2, 300)
        
        assert account1.balance == 700
        assert account2.balance == 800
    
    # Test 7 : Historique
    def test_transaction_history(self, account):
        """Test historique des transactions"""
        account.deposit(500)
        account.withdraw(200)
        account.deposit(100)
        
        assert len(account.transactions) == 3
        assert account.transactions[0]['type'] == 'DEPOSIT'
        assert account.transactions[1]['type'] == 'WITHDRAWAL'
        assert account.transactions[2]['type'] == 'DEPOSIT'
```

### 5.2 Implémentation (après les tests)

```python
# src/bank_account.py
from datetime import datetime
from typing import List, Dict


class BankAccount:
    """Compte bancaire"""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        """
        Initialise un compte bancaire
        
        Args:
            owner: Propriétaire du compte
            initial_balance: Solde initial
        """
        if initial_balance < 0:
            raise ValueError("Solde initial ne peut pas être négatif")
        
        self.owner = owner
        self._balance = initial_balance
        self.transactions: List[Dict] = []
    
    @property
    def balance(self) -> float:
        """Solde actuel (lecture seule)"""
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        """
        Dépose de l'argent
        
        Args:
            amount: Montant à déposer
            
        Returns:
            True si succès
            
        Raises:
            ValueError: Si montant invalide
        """
        if amount <= 0:
            raise ValueError(f"Montant invalide: {amount}")
        
        self._balance += amount
        self._add_transaction('DEPOSIT', amount)
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        Retire de l'argent
        
        Args:
            amount: Montant à retirer
            
        Returns:
            True si succès
            
        Raises:
            ValueError: Si montant invalide ou solde insuffisant
        """
        if amount <= 0:
            raise ValueError(f"Montant invalide: {amount}")
        
        if amount > self._balance:
            raise ValueError(
                f"Solde insuffisant. Disponible: {self._balance}€, "
                f"Demandé: {amount}€"
            )
        
        self._balance -= amount
        self._add_transaction('WITHDRAWAL', amount)
        return True
    
    def transfer(self, target_account: 'BankAccount', amount: float) -> bool:
        """
        Transfère de l'argent vers un autre compte
        
        Args:
            target_account: Compte destinataire
            amount: Montant à transférer
            
        Returns:
            True si succès
        """
        self.withdraw(amount)
        target_account.deposit(amount)
        self._add_transaction('TRANSFER_OUT', amount, target_account.owner)
        target_account._add_transaction('TRANSFER_IN', amount, self.owner)
        return True
    
    def _add_transaction(self, transaction_type: str, amount: float, 
                        other_party: str = None):
        """Ajoute une transaction à l'historique"""
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance
        }
        
        if other_party:
            transaction['other_party'] = other_party
        
        self.transactions.append(transaction)
    
    def get_statement(self) -> str:
        """Génère un relevé de compte"""
        lines = [
            f"{'='*60}",
            f"RELEVÉ DE COMPTE - {self.owner}",
            f"{'='*60}",
            f"Solde actuel: {self._balance:.2f}€",
            f"\nDernières transactions:",
        ]
        
        for trans in self.transactions[-10:]:
            timestamp = trans['timestamp'].strftime("%d/%m/%Y %H:%M")
            lines.append(
                f"  {timestamp} | {trans['type']:15} | "
                f"{trans['amount']:8.2f}€ | Solde: {trans['balance_after']:.2f}€"
            )
        
        lines.append(f"{'='*60}")
        return '\n'.join(lines)


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TDD - BANK ACCOUNT DÉMONSTRATION")
    print("=" * 70)
    
    # Créer des comptes
    marie = BankAccount("Marie Lafleur", 1000)
    jean = BankAccount("Jean Martin", 500)
    
    print("\n--- Opérations ---")
    marie.deposit(500)
    marie.withdraw(200)
    marie.transfer(jean, 300)
    
    print("\n--- Relevés ---")
    print(marie.get_statement())
    print("\n")
    print(jean.get_statement())
```

---

## 6. Coverage : Mesurer la Couverture

### 6.1 Installation et Utilisation

```bash
# Installation
pip install pytest-cov

# Exécution avec coverage
pytest --cov=src tests/

# Rapport HTML
pytest --cov=src --cov-report=html tests/
# Ouvre htmlcov/index.html
```

**Exemple de sortie :**
```
======================== test session starts ========================
collected 15 items

tests/test_bank_account.py ...............                    [100%]

---------- coverage: platform linux, python 3.11.0 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
src/bank_account.py        45      2    96%
-------------------------------------------
TOTAL                      45      2    96%
```

### 6.2 Interpréter la Coverage

```
✅ 80-100% : Excellente couverture
⚠️  60-80% : Couverture acceptable
❌ <60% : Couverture insuffisante
```

**Attention :** 100% coverage ≠ code parfait !

```python
# Exemple : 100% coverage mais bug possible
def divide(a, b):
    return a / b  # ✓ Couvert par les tests, mais crash si b=0

def test_divide():
    assert divide(10, 2) == 5  # Test OK, mais pas le cas b=0
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **Pourquoi tester** : Avantages et problèmes sans tests  
✅ **Types de tests** : Unitaires, Intégration, E2E  
✅ **pytest** : Framework moderne de test Python  
✅ **Fixtures** : Données réutilisables pour tests  
✅ **TDD** : Cycle Red-Green-Refactor  
✅ **Exemple complet** : BankAccount avec TDD  
✅ **Coverage** : Mesurer la couverture de code  

### Concepts clés

- **AAA Pattern** : Arrange, Act, Assert
- **Fixtures** : Données/objets pour tests
- **TDD** : Tests avant le code
- **Coverage** : % de code testé
- **Isolation** : Tests indépendants

### Dans la Partie 2, nous verrons :

- Mocking et Test Doubles
- Tests d'intégration avancés
- Tests de performance
- Qualité de code (Linting, Formatage)
- CI/CD avec GitHub Actions
- Cas pratiques complets

---

*Suite dans la Partie 2...*