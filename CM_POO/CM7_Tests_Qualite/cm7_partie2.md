# CM7 - Tests et Qualité de Code (Partie 2)
## Mocking, Tests d'Intégration et Qualité

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ Types de tests (unitaires, intégration, E2E)
- ✅ pytest et fixtures
- ✅ TDD (Red-Green-Refactor)
- ✅ Coverage

**Aujourd'hui - Partie 2 :**
- **Mocking** : Simuler des dépendances
- **Tests d'intégration** : Tester les interactions
- **Tests de performance** : Benchmarking
- **Qualité de code** : Linting, formatage
- **CI/CD** : Automatisation des tests

---

## 7. Mocking et Test Doubles

### 7.1 Qu'est-ce qu'un Mock ?

> **Un mock est un objet simulé qui remplace une dépendance externe pendant les tests.**

**Pourquoi mocker ?**
- ❌ Tests lents (base de données, réseau)
- ❌ Environnement instable (API externes)
- ❌ Difficile à reproduire (emails, paiements)
- ❌ Coûteux (services payants)

**Types de Test Doubles :**

```
DUMMY    → Objet passé mais jamais utilisé
STUB     → Retourne des réponses prédéfinies
MOCK     → Vérifie les interactions
FAKE     → Implémentation simplifiée fonctionnelle
SPY      → Enregistre les appels
```

### 7.2 unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch
import pytest


# ============================================================================
# EXEMPLE : Service d'envoi d'email
# ============================================================================

class EmailService:
    """Service d'envoi d'emails (dépendance externe)"""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Envoie un email via SMTP
        ❌ Lent, nécessite configuration, coûteux
        """
        # Code SMTP réel ici
        print(f"Envoi email à {to}: {subject}")
        return True


class UserService:
    """Service utilisateur qui dépend de EmailService"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.users = {}
    
    def register_user(self, email: str, name: str) -> bool:
        """Inscrit un utilisateur et envoie un email de bienvenue"""
        if email in self.users:
            return False
        
        self.users[email] = {'name': name, 'email': email}
        
        # Envoie un email (dépendance externe)
        self.email_service.send_email(
            to=email,
            subject="Bienvenue !",
            body=f"Bonjour {name}, bienvenue sur notre plateforme."
        )
        
        return True


# ============================================================================
# TESTS SANS MOCK (❌ Mauvais)
# ============================================================================

def test_register_user_without_mock():
    """
    ❌ Test sans mock : envoie vraiment un email
    - Lent
    - Nécessite configuration SMTP
    - Peut échouer si réseau down
    """
    email_service = EmailService()  # Vrai service
    user_service = UserService(email_service)
    
    result = user_service.register_user("marie@ua.fr", "Marie")
    assert result is True


# ============================================================================
# TESTS AVEC MOCK (✅ Bon)
# ============================================================================

def test_register_user_with_mock():
    """
    ✅ Test avec mock : simule l'envoi d'email
    - Rapide
    - Pas de dépendance externe
    - Toujours stable
    """
    # Créer un mock d'EmailService
    mock_email_service = Mock(spec=EmailService)
    mock_email_service.send_email.return_value = True
    
    # Injecter le mock
    user_service = UserService(mock_email_service)
    
    # Tester
    result = user_service.register_user("marie@ua.fr", "Marie")
    
    # Assertions
    assert result is True
    assert "marie@ua.fr" in user_service.users
    
    # Vérifier que send_email a été appelé
    mock_email_service.send_email.assert_called_once()
    mock_email_service.send_email.assert_called_with(
        to="marie@ua.fr",
        subject="Bienvenue !",
        body="Bonjour Marie, bienvenue sur notre plateforme."
    )


def test_register_duplicate_user():
    """Test d'inscription avec email déjà existant"""
    mock_email_service = Mock(spec=EmailService)
    user_service = UserService(mock_email_service)
    
    # Premier utilisateur
    user_service.register_user("marie@ua.fr", "Marie")
    
    # Tentative de doublon
    result = user_service.register_user("marie@ua.fr", "Marie Duplicate")
    
    assert result is False
    
    # Vérifier que send_email n'a été appelé qu'une fois (pas pour le doublon)
    mock_email_service.send_email.assert_called_once()
```

### 7.3 Patch : Mocker des Fonctions/Classes

```python
from unittest.mock import patch


# ============================================================================
# CODE À TESTER
# ============================================================================

import requests


class WeatherService:
    """Service météo qui appelle une API externe"""
    
    API_URL = "https://api.weather.com/current"
    
    def get_temperature(self, city: str) -> float:
        """Récupère la température depuis l'API"""
        response = requests.get(f"{self.API_URL}?city={city}")
        response.raise_for_status()
        data = response.json()
        return data['temperature']
    
    def is_hot(self, city: str) -> bool:
        """Vérifie s'il fait chaud"""
        temp = self.get_temperature(city)
        return temp > 25


# ============================================================================
# TESTS AVEC PATCH
# ============================================================================

@patch('requests.get')
def test_get_temperature(mock_get):
    """Test avec mock de requests.get"""
    # Configurer le mock
    mock_response = Mock()
    mock_response.json.return_value = {'temperature': 28.5}
    mock_get.return_value = mock_response
    
    # Tester
    service = WeatherService()
    temp = service.get_temperature("Fort-de-France")
    
    # Assertions
    assert temp == 28.5
    mock_get.assert_called_once_with(
        "https://api.weather.com/current?city=Fort-de-France"
    )


@patch('requests.get')
def test_is_hot(mock_get):
    """Test is_hot avec différentes températures"""
    service = WeatherService()
    
    # Cas 1 : Chaud (> 25°C)
    mock_response = Mock()
    mock_response.json.return_value = {'temperature': 30}
    mock_get.return_value = mock_response
    
    assert service.is_hot("Fort-de-France") is True
    
    # Cas 2 : Pas chaud (<= 25°C)
    mock_response.json.return_value = {'temperature': 20}
    
    assert service.is_hot("Paris") is False


@patch('requests.get')
def test_api_error_handling(mock_get):
    """Test gestion d'erreur API"""
    # Simuler une erreur HTTP
    mock_get.side_effect = requests.HTTPError("API Error")
    
    service = WeatherService()
    
    with pytest.raises(requests.HTTPError):
        service.get_temperature("Unknown")
```

### 7.4 Exemple Complet : Payment Service

```python
from unittest.mock import Mock, patch
import pytest
from decimal import Decimal


# ============================================================================
# CODE À TESTER
# ============================================================================

class PaymentGateway:
    """Gateway de paiement externe (Stripe, PayPal, etc.)"""
    
    def charge(self, card_token: str, amount: Decimal) -> dict:
        """
        Charge une carte
        ❌ Appel API réel → coûteux et lent
        """
        # Appel API réel ici
        pass


class PaymentService:
    """Service de paiement qui utilise PaymentGateway"""
    
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
        self.transactions = []
    
    def process_payment(self, card_token: str, amount: Decimal, 
                       order_id: str) -> bool:
        """Traite un paiement"""
        if amount <= 0:
            raise ValueError("Montant invalide")
        
        try:
            # Appel au gateway (moqué dans les tests)
            result = self.gateway.charge(card_token, amount)
            
            if result['status'] == 'success':
                self.transactions.append({
                    'order_id': order_id,
                    'amount': amount,
                    'transaction_id': result['transaction_id']
                })
                return True
            
            return False
        
        except Exception as e:
            # Logger l'erreur en production
            return False


# ============================================================================
# TESTS AVEC MOCKS
# ============================================================================

class TestPaymentService:
    """Tests du service de paiement"""
    
    @pytest.fixture
    def mock_gateway(self):
        """Fixture : mock du gateway"""
        return Mock(spec=PaymentGateway)
    
    @pytest.fixture
    def payment_service(self, mock_gateway):
        """Fixture : service avec mock injecté"""
        return PaymentService(mock_gateway)
    
    def test_successful_payment(self, payment_service, mock_gateway):
        """Test paiement réussi"""
        # Configurer le mock
        mock_gateway.charge.return_value = {
            'status': 'success',
            'transaction_id': 'TXN123456'
        }
        
        # Exécuter
        result = payment_service.process_payment(
            card_token='tok_123',
            amount=Decimal('50.00'),
            order_id='ORD001'
        )
        
        # Vérifications
        assert result is True
        assert len(payment_service.transactions) == 1
        assert payment_service.transactions[0]['order_id'] == 'ORD001'
        
        # Vérifier l'appel au gateway
        mock_gateway.charge.assert_called_once_with('tok_123', Decimal('50.00'))
    
    def test_failed_payment(self, payment_service, mock_gateway):
        """Test paiement échoué"""
        mock_gateway.charge.return_value = {
            'status': 'failed',
            'error': 'Insufficient funds'
        }
        
        result = payment_service.process_payment(
            'tok_123', Decimal('50.00'), 'ORD002'
        )
        
        assert result is False
        assert len(payment_service.transactions) == 0
    
    def test_gateway_exception(self, payment_service, mock_gateway):
        """Test exception du gateway"""
        mock_gateway.charge.side_effect = ConnectionError("Network error")
        
        result = payment_service.process_payment(
            'tok_123', Decimal('50.00'), 'ORD003'
        )
        
        assert result is False
    
    def test_invalid_amount(self, payment_service):
        """Test montant invalide"""
        with pytest.raises(ValueError, match="Montant invalide"):
            payment_service.process_payment('tok_123', Decimal('0'), 'ORD004')
        
        with pytest.raises(ValueError):
            payment_service.process_payment('tok_123', Decimal('-10'), 'ORD005')
```

---

## 8. Tests d'Intégration

### 8.1 Tests avec Base de Données

```python
import pytest
import sqlite3
from contextlib import contextmanager


# ============================================================================
# CODE À TESTER
# ============================================================================

class StudentRepository:
    """Repository pour les étudiants"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialise la base de données"""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
    
    @contextmanager
    def _get_connection(self):
        """Context manager pour les connexions"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def save(self, student_id: str, name: str, email: str) -> int:
        """Sauvegarde un étudiant"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                'INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)',
                (student_id, name, email)
            )
            return cursor.lastrowid
    
    def find_by_student_id(self, student_id: str) -> dict:
        """Trouve un étudiant par son ID"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM students WHERE student_id = ?',
                (student_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def find_all(self) -> list:
        """Trouve tous les étudiants"""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM students')
            return [dict(row) for row in cursor.fetchall()]


# ============================================================================
# TESTS D'INTÉGRATION
# ============================================================================

@pytest.fixture
def db_repo(tmp_path):
    """
    Fixture : repository avec base de données temporaire
    tmp_path est fourni par pytest
    """
    db_path = tmp_path / "test.db"
    repo = StudentRepository(str(db_path))
    yield repo
    # Cleanup automatique par tmp_path


class TestStudentRepositoryIntegration:
    """Tests d'intégration avec vraie base de données"""
    
    def test_save_and_find(self, db_repo):
        """Test sauvegarde et récupération"""
        # Sauvegarder
        student_id = db_repo.save("20231001", "Marie Lafleur", "marie@ua.fr")
        
        # Récupérer
        student = db_repo.find_by_student_id("20231001")
        
        # Vérifier
        assert student is not None
        assert student['student_id'] == "20231001"
        assert student['name'] == "Marie Lafleur"
        assert student['email'] == "marie@ua.fr"
    
    def test_find_all(self, db_repo):
        """Test récupération de tous les étudiants"""
        # Ajouter plusieurs étudiants
        db_repo.save("20231001", "Marie", "marie@ua.fr")
        db_repo.save("20231002", "Jean", "jean@ua.fr")
        db_repo.save("20231003", "Sophie", "sophie@ua.fr")
        
        # Récupérer tous
        students = db_repo.find_all()
        
        # Vérifier
        assert len(students) == 3
        assert students[0]['name'] == "Marie"
        assert students[1]['name'] == "Jean"
        assert students[2]['name'] == "Sophie"
    
    def test_duplicate_student_id(self, db_repo):
        """Test unicité de student_id"""
        db_repo.save("20231001", "Marie", "marie@ua.fr")
        
        # Tentative de doublon
        with pytest.raises(sqlite3.IntegrityError):
            db_repo.save("20231001", "Duplicate", "dup@ua.fr")
    
    def test_find_nonexistent(self, db_repo):
        """Test recherche d'étudiant inexistant"""
        student = db_repo.find_by_student_id("999999")
        assert student is None
```

---

## 9. Qualité de Code

### 9.1 Linting avec pylint et flake8

```bash
# Installation
pip install pylint flake8 black mypy

# Vérification
pylint src/
flake8 src/
```

**Exemple de configuration (.pylintrc) :**
```ini
[MASTER]
max-line-length=100

[MESSAGES CONTROL]
disable=C0111  # missing-docstring (trop strict pour les tests)

[DESIGN]
max-args=7
max-locals=15
```

**Exemple de configuration (.flake8) :**
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203,W503
```

### 9.2 Formatage automatique avec black

```bash
# Formater tout le code
black src/ tests/

# Vérifier sans modifier
black --check src/

# Configuration (pyproject.toml)
[tool.black]
line-length = 100
target-version = ['py311']
```

### 9.3 Type Checking avec mypy

```python
# Code avec type hints
from typing import List, Optional


class Student:
    """Étudiant avec type hints"""
    
    def __init__(self, student_id: str, name: str, email: str):
        self.student_id: str = student_id
        self.name: str = name
        self.email: str = email
        self.grades: List[float] = []
    
    def add_grade(self, grade: float) -> None:
        """Ajoute une note"""
        if not 0 <= grade <= 20:
            raise ValueError(f"Note invalide: {grade}")
        self.grades.append(grade)
    
    def calculate_average(self) -> float:
        """Calcule la moyenne"""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)
    
    def get_highest_grade(self) -> Optional[float]:
        """Retourne la meilleure note"""
        if not self.grades:
            return None
        return max(self.grades)


# Vérification avec mypy
# $ mypy src/
```

### 9.4 Pre-commit Hooks

**Installation :**
```bash
pip install pre-commit

# Créer .pre-commit-config.yaml
```

**.pre-commit-config.yaml :**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

# Installer les hooks
# $ pre-commit install

# Exécuter manuellement
# $ pre-commit run --all-files
```

---

## 10. CI/CD avec GitHub Actions

### 10.1 Configuration de base

**.github/workflows/tests.yml :**
```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install black flake8 mypy
      
      - name: Check formatting with black
        run: black --check src/ tests/
      
      - name: Lint with flake8
        run: flake8 src/ tests/
      
      - name: Type check with mypy
        run: mypy src/
```

---

## 11. Cas Pratique Complet : API de Gestion d'Étudiants

```python
# ============================================================================
# src/api.py
# ============================================================================

from flask import Flask, jsonify, request
from typing import List, Dict
import sqlite3


app = Flask(__name__)


class StudentAPI:
    """API REST pour la gestion d'étudiants"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialise la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.close()
    
    def create_student(self, student_id: str, name: str, email: str) -> Dict:
        """Crée un étudiant"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                'INSERT INTO students (student_id, name, email) VALUES (?, ?, ?)',
                (student_id, name, email)
            )
            conn.commit()
            return {'student_id': student_id, 'name': name, 'email': email}
        except sqlite3.IntegrityError:
            raise ValueError(f"Student {student_id} already exists")
        finally:
            conn.close()
    
    def get_student(self, student_id: str) -> Dict:
        """Récupère un étudiant"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            'SELECT * FROM students WHERE student_id = ?',
            (student_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        raise ValueError(f"Student {student_id} not found")
    
    def get_all_students(self) -> List[Dict]:
        """Liste tous les étudiants"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM students')
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students


# ============================================================================
# tests/test_api.py - TESTS COMPLETS
# ============================================================================

import pytest
from src.api import StudentAPI


@pytest.fixture
def api(tmp_path):
    """Fixture : API avec base temporaire"""
    db_path = tmp_path / "test.db"
    return StudentAPI(str(db_path))


class TestStudentAPI:
    """Tests de l'API étudiante"""
    
    def test_create_student(self, api):
        """Test création d'étudiant"""
        student = api.create_student(
            "20231001",
            "Marie Lafleur",
            "marie@ua.fr"
        )
        
        assert student['student_id'] == "20231001"
        assert student['name'] == "Marie Lafleur"
        assert student['email'] == "marie@ua.fr"
    
    def test_create_duplicate_student(self, api):
        """Test création d'étudiant en doublon"""
        api.create_student("20231001", "Marie", "marie@ua.fr")
        
        with pytest.raises(ValueError, match="already exists"):
            api.create_student("20231001", "Duplicate", "dup@ua.fr")
    
    def test_get_student(self, api):
        """Test récupération d'étudiant"""
        api.create_student("20231001", "Marie", "marie@ua.fr")
        
        student = api.get_student("20231001")
        
        assert student['name'] == "Marie"
        assert student['email'] == "marie@ua.fr"
    
    def test_get_nonexistent_student(self, api):
        """Test récupération d'étudiant inexistant"""
        with pytest.raises(ValueError, match="not found"):
            api.get_student("999999")
    
    def test_get_all_students(self, api):
        """Test liste de tous les étudiants"""
        api.create_student("20231001", "Marie", "marie@ua.fr")
        api.create_student("20231002", "Jean", "jean@ua.fr")
        api.create_student("20231003", "Sophie", "sophie@ua.fr")
        
        students = api.get_all_students()
        
        assert len(students) == 3
        names = [s['name'] for s in students]
        assert "Marie" in names
        assert "Jean" in names
        assert "Sophie" in names
```

---

## Résumé Partie 2

### Ce que nous avons vu

✅ **Mocking** : unittest.mock, patch, test doubles  
✅ **Tests d'intégration** : Base de données, fixtures  
✅ **Qualité de code** : pylint, flake8, black, mypy  
✅ **Pre-commit hooks** : Automatisation des vérifications  
✅ **CI/CD** : GitHub Actions pour tests automatiques  
✅ **Cas pratique** : API complète avec tests  

### Bonnes Pratiques

**Tests :**
- Mocker les dépendances externes
- Utiliser des bases de données temporaires
- Viser 80%+ coverage
- Tests rapides et isolés

**Qualité :**
- Formatage automatique (black)
- Linting (flake8, pylint)
- Type checking (mypy)
- Pre-commit hooks

**CI/CD :**
- Tests sur chaque push
- Multiple versions Python
- Coverage tracking
- Lint automatique

### Conclusion CM7

**Concepts maîtrisés :**
1. **Tests unitaires** avec pytest
2. **TDD** (Red-Green-Refactor)
3. **Mocking** pour isolation
4. **Tests d'intégration** avec vraies dépendances
5. **Coverage** pour mesurer les tests
6. **Qualité de code** avec outils
7. **CI/CD** pour automatisation


---

*Fin du CM7 - Tests et Qualité de Code*