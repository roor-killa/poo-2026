# CM6 - Architecture Logicielle (Partie 2)
## Hexagonal Architecture, DDD, Microservices et Applications Pratiques

---

## Rappel Partie 1

**Architectures vues :**
- ✅ Architecture en Couches (3-tier)
- ✅ MVC (Model-View-Controller)
- ✅ Clean Architecture (Uncle Bob)

**Aujourd'hui :**
- Hexagonal Architecture
- Domain-Driven Design (DDD)
- Microservices vs Monolithe
- Event-Driven Architecture
- Applications pour vos projets

---

## 6. Hexagonal Architecture (Ports & Adapters)

### Concept

> **Aussi appelée "Ports and Adapters"**, cette architecture isole complètement la logique métier (le "noyau") des détails techniques (infrastructure).

**Inventeur :** Alistair Cockburn (2005)

### Structure

```
         ┌──────────────────────────┐
         │      ADAPTERS            │
         │   (Infrastructure)       │
         │                          │
    ┌────┤  • Web API              ├────┐
    │    │  • CLI                  │    │
    │    │  • Message Queue        │    │
    │    └──────────┬───────────────┘    │
    │               │                    │
    │               ↓                    │
    │    ┌──────────────────────┐       │
    │    │       PORTS          │       │
    │    │   (Interfaces)       │       │
    │    └──────────┬───────────┘       │
    │               │                    │
    │               ↓                    │
    │    ┌──────────────────────┐       │
    │    │     APPLICATION       │       │
    │    │   (Use Cases/Core)    │       │
    │    │                       │       │
    │    │  ← Logique métier     │       │
    │    └──────────┬────────────┘       │
    │               │                    │
    │               ↓                    │
    │    ┌──────────────────────┐       │
    │    │       PORTS          │       │
    │    │   (Interfaces)       │       │
    │    └──────────┬───────────┘       │
    │               │                    │
    │               ↓                    │
    └────┤  • PostgreSQL          ├────┘
         │  • Redis               │
         │  • Email Service       │
         │                        │
         │      ADAPTERS          │
         │   (Infrastructure)     │
         └────────────────────────┘

Ports = Interfaces (contrat)
Adapters = Implémentations (détails)
```

### Principes clés

1. **Le domaine au centre** : Logique métier isolée
2. **Ports** : Interfaces définies par le domaine
3. **Adapters** : Implémentations techniques interchangeables
4. **Symétrie** : Adapters primaires (entrée) et secondaires (sortie)

### Implémentation

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


# ============================================================================
# DOMAIN / CORE (Centre de l'hexagone)
# ============================================================================

@dataclass
class Book:
    """Entity : Livre"""
    isbn: str
    title: str
    author: str
    available: bool = True
    borrower: Optional[str] = None
    
    def borrow(self, user_id: str) -> bool:
        """Règle métier : Emprunter un livre"""
        if not self.available:
            return False
        
        self.available = False
        self.borrower = user_id
        return True
    
    def return_book(self) -> bool:
        """Règle métier : Retourner un livre"""
        if self.available:
            return False
        
        self.available = True
        self.borrower = None
        return True


# ============================================================================
# PORTS (Interfaces définies par le domaine)
# ============================================================================

# --- Ports primaires (côté utilisateur / entrée) ---

class LibraryService(ABC):
    """
    Port primaire : Interface du service bibliothèque
    Défini ce que l'application peut faire
    """
    
    @abstractmethod
    def add_book(self, isbn: str, title: str, author: str) -> Book:
        pass
    
    @abstractmethod
    def borrow_book(self, isbn: str, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def return_book(self, isbn: str) -> bool:
        pass
    
    @abstractmethod
    def search_books(self, query: str) -> List[Book]:
        pass


# --- Ports secondaires (côté infrastructure / sortie) ---

class BookRepository(ABC):
    """
    Port secondaire : Interface pour la persistance
    Défini par le domaine, implémenté par l'infrastructure
    """
    
    @abstractmethod
    def save(self, book: Book) -> None:
        pass
    
    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Book]:
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Book]:
        pass


class NotificationPort(ABC):
    """
    Port secondaire : Interface pour les notifications
    """
    
    @abstractmethod
    def notify_borrow(self, user_id: str, book_title: str) -> None:
        pass
    
    @abstractmethod
    def notify_return(self, user_id: str, book_title: str) -> None:
        pass


class LoggingPort(ABC):
    """
    Port secondaire : Interface pour le logging
    """
    
    @abstractmethod
    def log_action(self, action: str, details: dict) -> None:
        pass


# ============================================================================
# APPLICATION / USE CASES (Cœur de l'hexagone)
# ============================================================================

class LibraryServiceImpl(LibraryService):
    """
    Implémentation du service (logique applicative)
    Dépend UNIQUEMENT des ports (abstractions)
    """
    
    def __init__(self, 
                 book_repo: BookRepository,
                 notifier: NotificationPort,
                 logger: LoggingPort):
        self.book_repo = book_repo
        self.notifier = notifier
        self.logger = logger
    
    def add_book(self, isbn: str, title: str, author: str) -> Book:
        """Use case : Ajouter un livre"""
        # Vérifier si le livre existe déjà
        existing = self.book_repo.find_by_isbn(isbn)
        if existing:
            raise ValueError(f"Livre {isbn} déjà dans la bibliothèque")
        
        # Créer le livre
        book = Book(isbn=isbn, title=title, author=author)
        
        # Sauvegarder
        self.book_repo.save(book)
        
        # Logger
        self.logger.log_action("ADD_BOOK", {
            'isbn': isbn,
            'title': title,
            'author': author
        })
        
        return book
    
    def borrow_book(self, isbn: str, user_id: str) -> bool:
        """Use case : Emprunter un livre"""
        # Récupérer le livre
        book = self.book_repo.find_by_isbn(isbn)
        if not book:
            raise ValueError(f"Livre {isbn} introuvable")
        
        # Emprunter (logique métier dans l'Entity)
        if not book.borrow(user_id):
            raise ValueError(f"Livre {book.title} non disponible")
        
        # Sauvegarder
        self.book_repo.save(book)
        
        # Notifier
        self.notifier.notify_borrow(user_id, book.title)
        
        # Logger
        self.logger.log_action("BORROW_BOOK", {
            'isbn': isbn,
            'user_id': user_id,
            'title': book.title
        })
        
        return True
    
    def return_book(self, isbn: str) -> bool:
        """Use case : Retourner un livre"""
        # Récupérer le livre
        book = self.book_repo.find_by_isbn(isbn)
        if not book:
            raise ValueError(f"Livre {isbn} introuvable")
        
        borrower = book.borrower
        
        # Retourner (logique métier dans l'Entity)
        if not book.return_book():
            raise ValueError(f"Livre {book.title} n'était pas emprunté")
        
        # Sauvegarder
        self.book_repo.save(book)
        
        # Notifier
        self.notifier.notify_return(borrower, book.title)
        
        # Logger
        self.logger.log_action("RETURN_BOOK", {
            'isbn': isbn,
            'user_id': borrower,
            'title': book.title
        })
        
        return True
    
    def search_books(self, query: str) -> List[Book]:
        """Use case : Rechercher des livres"""
        return self.book_repo.search(query)


# ============================================================================
# ADAPTERS SECONDAIRES (Infrastructure / Sortie)
# ============================================================================

class InMemoryBookRepository(BookRepository):
    """Adapter : Repository en mémoire"""
    
    def __init__(self):
        self._books: dict[str, Book] = {}
    
    def save(self, book: Book) -> None:
        self._books[book.isbn] = book
    
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return self._books.get(isbn)
    
    def find_all(self) -> List[Book]:
        return list(self._books.values())
    
    def search(self, query: str) -> List[Book]:
        query_lower = query.lower()
        return [
            book for book in self._books.values()
            if query_lower in book.title.lower() or query_lower in book.author.lower()
        ]


class JSONFileBookRepository(BookRepository):
    """Adapter : Repository fichier JSON"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._load()
    
    def _load(self):
        """Charge les données du fichier"""
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self._books = {
                    book_data['isbn']: Book(**book_data)
                    for book_data in data
                }
        except FileNotFoundError:
            self._books = {}
    
    def _persist(self):
        """Sauvegarde dans le fichier"""
        data = [
            {
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'available': book.available,
                'borrower': book.borrower
            }
            for book in self._books.values()
        ]
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save(self, book: Book) -> None:
        self._books[book.isbn] = book
        self._persist()
    
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return self._books.get(isbn)
    
    def find_all(self) -> List[Book]:
        return list(self._books.values())
    
    def search(self, query: str) -> List[Book]:
        query_lower = query.lower()
        return [
            book for book in self._books.values()
            if query_lower in book.title.lower() or query_lower in book.author.lower()
        ]


class ConsoleNotificationAdapter(NotificationPort):
    """Adapter : Notifications console"""
    
    def notify_borrow(self, user_id: str, book_title: str) -> None:
        print(f"📧 [Notification] Utilisateur {user_id} a emprunté '{book_title}'")
    
    def notify_return(self, user_id: str, book_title: str) -> None:
        print(f"📧 [Notification] Utilisateur {user_id} a retourné '{book_title}'")


class EmailNotificationAdapter(NotificationPort):
    """Adapter : Notifications par email (simulation)"""
    
    def notify_borrow(self, user_id: str, book_title: str) -> None:
        # En réalité : appel à un service SMTP
        print(f"📨 [Email] Envoi email à {user_id}: Emprunt de '{book_title}'")
    
    def notify_return(self, user_id: str, book_title: str) -> None:
        print(f"📨 [Email] Envoi email à {user_id}: Retour de '{book_title}'")


class ConsoleLoggingAdapter(LoggingPort):
    """Adapter : Logging console"""
    
    def log_action(self, action: str, details: dict) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {timestamp}] {action} - {details}")


class FileLoggingAdapter(LoggingPort):
    """Adapter : Logging fichier"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def log_action(self, action: str, details: dict) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action} - {json.dumps(details)}\n"
        
        with open(self.filepath, 'a') as f:
            f.write(log_entry)


# ============================================================================
# ADAPTERS PRIMAIRES (Interface utilisateur / Entrée)
# ============================================================================

class CLIAdapter:
    """Adapter primaire : Interface ligne de commande"""
    
    def __init__(self, library_service: LibraryService):
        self.service = library_service
    
    def run(self):
        """Lance l'interface CLI"""
        while True:
            print("\n" + "=" * 60)
            print("BIBLIOTHÈQUE - SYSTÈME DE GESTION")
            print("=" * 60)
            print("1. Ajouter un livre")
            print("2. Emprunter un livre")
            print("3. Retourner un livre")
            print("4. Rechercher des livres")
            print("5. Quitter")
            
            choice = input("\nChoix : ").strip()
            
            if choice == "1":
                self._add_book()
            elif choice == "2":
                self._borrow_book()
            elif choice == "3":
                self._return_book()
            elif choice == "4":
                self._search_books()
            elif choice == "5":
                print("Au revoir!")
                break
    
    def _add_book(self):
        isbn = input("ISBN : ")
        title = input("Titre : ")
        author = input("Auteur : ")
        
        try:
            book = self.service.add_book(isbn, title, author)
            print(f"✓ Livre '{book.title}' ajouté")
        except ValueError as e:
            print(f"✗ Erreur : {e}")
    
    def _borrow_book(self):
        isbn = input("ISBN : ")
        user_id = input("ID utilisateur : ")
        
        try:
            self.service.borrow_book(isbn, user_id)
            print(f"✓ Livre emprunté")
        except ValueError as e:
            print(f"✗ Erreur : {e}")
    
    def _return_book(self):
        isbn = input("ISBN : ")
        
        try:
            self.service.return_book(isbn)
            print(f"✓ Livre retourné")
        except ValueError as e:
            print(f"✗ Erreur : {e}")
    
    def _search_books(self):
        query = input("Recherche : ")
        books = self.service.search_books(query)
        
        if not books:
            print("Aucun livre trouvé")
        else:
            print(f"\n{len(books)} livre(s) trouvé(s):")
            for book in books:
                status = "✓ Disponible" if book.available else f"✗ Emprunté par {book.borrower}"
                print(f"  [{book.isbn}] {book.title} par {book.author} - {status}")


class RESTAPIAdapter:
    """Adapter primaire : API REST (simulation)"""
    
    def __init__(self, library_service: LibraryService):
        self.service = library_service
    
    def handle_add_book(self, request_data: dict) -> dict:
        """POST /books"""
        try:
            book = self.service.add_book(
                request_data['isbn'],
                request_data['title'],
                request_data['author']
            )
            return {
                'status': 'success',
                'book': {
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author
                }
            }
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    
    def handle_borrow_book(self, isbn: str, user_id: str) -> dict:
        """POST /books/{isbn}/borrow"""
        try:
            self.service.borrow_book(isbn, user_id)
            return {'status': 'success'}
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}


# ============================================================================
# CONFIGURATION & MAIN
# ============================================================================

def main():
    """
    Configuration de l'application
    C'est ici qu'on "branche" les adapters
    """
    
    print("=" * 70)
    print("HEXAGONAL ARCHITECTURE - DÉMONSTRATION")
    print("=" * 70)
    
    # Configuration 1 : Adapters en mémoire + console
    print("\n--- Configuration 1: In-Memory + Console ---")
    
    book_repo = InMemoryBookRepository()
    notifier = ConsoleNotificationAdapter()
    logger = ConsoleLoggingAdapter()
    
    service = LibraryServiceImpl(book_repo, notifier, logger)
    
    # Ajouter des livres
    service.add_book("978-0134685991", "Effective Java", "Joshua Bloch")
    service.add_book("978-0135957059", "Clean Architecture", "Robert Martin")
    
    # Emprunter
    service.borrow_book("978-0134685991", "alice@ua.fr")
    
    # Retourner
    service.return_book("978-0134685991")
    
    print("\n" + "=" * 70)
    print("AVANTAGES DE L'HEXAGONAL ARCHITECTURE:")
    print("- Logique métier 100% isolée de l'infrastructure")
    print("- Changement de DB transparent (InMemory → JSON → PostgreSQL)")
    print("- Changement de notification transparent (Console → Email → SMS)")
    print("- Testabilité maximale (mocks faciles des adapters)")
    print("- Symétrie : adapters primaires et secondaires")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

### Avantages de l'Hexagonal Architecture

**✅ Testabilité**
```python
# Tests faciles avec des mocks
def test_borrow_book():
    # Arrange
    mock_repo = MockBookRepository()
    mock_notifier = MockNotificationAdapter()
    mock_logger = MockLoggingAdapter()
    
    service = LibraryServiceImpl(mock_repo, mock_notifier, mock_logger)
    
    # Act & Assert
    # Tests sans dépendances réelles
```

**✅ Flexibilité**
```python
# Changer d'infrastructure sans toucher la logique métier
# Version 1 : InMemory
service = LibraryServiceImpl(InMemoryBookRepository(), ...)

# Version 2 : JSON
service = LibraryServiceImpl(JSONFileBookRepository("books.json"), ...)

# Version 3 : PostgreSQL
service = LibraryServiceImpl(PostgreSQLBookRepository(), ...)

# Logique métier INCHANGÉE !
```

---

## 7. Domain-Driven Design (DDD)

### Introduction

> **DDD est une approche de développement logiciel qui place le domaine métier au centre.**
>
> *— Eric Evans, 2003*

### Concepts Clés

#### 1. Ubiquitous Language (Langage Omniprésent)

Un langage commun entre développeurs et experts métier.

```python
# ❌ Langage technique
class DataRecord:
    def process(self): pass

# ✅ Langage métier (Ubiquitous Language)
class StudentEnrollment:
    def submit_application(self): pass
    def approve(self): pass
    def reject(self): pass
```

#### 2. Bounded Context (Contexte Délimité)

Chaque sous-domaine a son propre modèle.

```
┌─────────────────────┐   ┌─────────────────────┐
│  ACADEMIC CONTEXT   │   │  FINANCIAL CONTEXT  │
│                     │   │                     │
│  Student            │   │  Student            │
│  - student_id       │   │  - student_id       │
│  - name             │   │  - account_balance  │
│  - enrolled_courses │   │  - payment_history  │
│                     │   │                     │
└─────────────────────┘   └─────────────────────┘

Même entité "Student" mais contextes différents !
```

#### 3. Entities vs Value Objects

**Entity** : Identité importante
```python
class Student:
    """Entity : l'identité (student_id) est importante"""
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id  # Identifiant unique
        self.name = name
    
    def __eq__(self, other):
        return self.student_id == other.student_id
```

**Value Object** : Valeur importante, pas l'identité
```python
@dataclass(frozen=True)
class Address:
    """Value Object : seule la valeur compte"""
    street: str
    city: str
    postal_code: str
    
    # Immutable, pas d'identité
    # Deux adresses identiques sont interchangeables
```

#### 4. Aggregates (Agrégats)

Un cluster d'objets traités comme une unité.

```python
class CourseAggregate:
    """
    Aggregate Root : Course
    L'accès aux Lessons passe par Course
    """
    
    def __init__(self, course_id: str, name: str):
        self.course_id = course_id  # Aggregate Root ID
        self.name = name
        self._lessons: List[Lesson] = []  # Partie de l'agrégat
    
    def add_lesson(self, title: str, duration: int):
        """
        Règle métier : On ajoute des leçons via le Course
        Pas d'accès direct à Lesson depuis l'extérieur
        """
        lesson_id = f"{self.course_id}-L{len(self._lessons) + 1}"
        lesson = Lesson(lesson_id, title, duration)
        self._lessons.append(lesson)
    
    def get_total_duration(self) -> int:
        """Logique métier de l'agrégat"""
        return sum(lesson.duration for lesson in self._lessons)
```

#### 5. Repositories (Référentiels)

Abstraction pour l'accès aux agrégats.

```python
class CourseRepository(ABC):
    """Repository : accès aux aggregates Course"""
    
    @abstractmethod
    def save(self, course: CourseAggregate) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, course_id: str) -> Optional[CourseAggregate]:
        pass
    
    # Pas de méthode pour sauvegarder Lesson directement
    # Car Lesson fait partie de l'agrégat Course
```

#### 6. Domain Services

Logique métier qui ne rentre pas dans une Entity.

```python
class EnrollmentService:
    """
    Domain Service : logique métier entre plusieurs entités
    """
    
    def can_enroll(self, student: Student, course: Course) -> bool:
        """
        Règle métier complexe impliquant Student et Course
        """
        # Vérifier les prérequis
        if not self._has_prerequisites(student, course):
            return False
        
        # Vérifier la capacité
        if course.is_full():
            return False
        
        # Vérifier les conflits d'horaire
        if self._has_schedule_conflict(student, course):
            return False
        
        return True
```

### Exemple DDD Complet

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


# ============================================================================
# VALUE OBJECTS
# ============================================================================

@dataclass(frozen=True)
class Email:
    """Value Object : Email"""
    value: str
    
    def __post_init__(self):
        if '@' not in self.value:
            raise ValueError("Email invalide")


@dataclass(frozen=True)
class Grade:
    """Value Object : Note"""
    value: float
    
    def __post_init__(self):
        if not 0 <= self.value <= 20:
            raise ValueError("Note doit être entre 0 et 20")
    
    def is_passing(self) -> bool:
        return self.value >= 10.0


# ============================================================================
# ENTITIES
# ============================================================================

class Student:
    """Entity : Étudiant"""
    
    def __init__(self, student_id: str, name: str, email: Email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self._enrolled_courses: List[str] = []
    
    def enroll_in_course(self, course_id: str):
        """Règle métier : Inscription"""
        if course_id not in self._enrolled_courses:
            self._enrolled_courses.append(course_id)
    
    def is_enrolled_in(self, course_id: str) -> bool:
        return course_id in self._enrolled_courses


# ============================================================================
# AGGREGATE
# ============================================================================

class CourseEnrollment:
    """Entity dans l'agrégat"""
    
    def __init__(self, student_id: str, enrolled_at: datetime):
        self.student_id = student_id
        self.enrolled_at = enrolled_at
        self.grade: Optional[Grade] = None
    
    def assign_grade(self, grade: Grade):
        self.grade = grade


class Course:
    """Aggregate Root : Cours"""
    
    def __init__(self, course_id: str, name: str, max_students: int):
        self.course_id = course_id
        self.name = name
        self.max_students = max_students
        self._enrollments: List[CourseEnrollment] = []
    
    def enroll_student(self, student_id: str) -> bool:
        """
        Règle métier : Inscrire un étudiant
        Invariant : Pas plus de max_students
        """
        # Vérifier la capacité
        if len(self._enrollments) >= self.max_students:
            return False
        
        # Vérifier si déjà inscrit
        if self._is_student_enrolled(student_id):
            return False
        
        # Inscrire
        enrollment = CourseEnrollment(student_id, datetime.now())
        self._enrollments.append(enrollment)
        return True
    
    def assign_grade(self, student_id: str, grade: Grade) -> bool:
        """Règle métier : Attribuer une note"""
        enrollment = self._find_enrollment(student_id)
        if not enrollment:
            return False
        
        enrollment.assign_grade(grade)
        return True
    
    def get_passing_rate(self) -> float:
        """Logique métier : Taux de réussite"""
        graded = [e for e in self._enrollments if e.grade is not None]
        if not graded:
            return 0.0
        
        passing = sum(1 for e in graded if e.grade.is_passing())
        return (passing / len(graded)) * 100
    
    def _is_student_enrolled(self, student_id: str) -> bool:
        return any(e.student_id == student_id for e in self._enrollments)
    
    def _find_enrollment(self, student_id: str) -> Optional[CourseEnrollment]:
        for enrollment in self._enrollments:
            if enrollment.student_id == student_id:
                return enrollment
        return None


# ============================================================================
# DOMAIN SERVICE
# ============================================================================

class AcademicService:
    """
    Domain Service : Logique métier transversale
    """
    
    def calculate_gpa(self, student_id: str, courses: List[Course]) -> float:
        """Calcule la GPA (moyenne générale)"""
        total_grade = 0.0
        count = 0
        
        for course in courses:
            enrollment = course._find_enrollment(student_id)
            if enrollment and enrollment.grade:
                total_grade += enrollment.grade.value
                count += 1
        
        return total_grade / count if count > 0 else 0.0


# ============================================================================
# REPOSITORY
# ============================================================================

class CourseRepository(ABC):
    """Repository : Accès aux agrégats Course"""
    
    @abstractmethod
    def save(self, course: Course) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, course_id: str) -> Optional[Course]:
        pass


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DOMAIN-DRIVEN DESIGN - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer un cours (Aggregate Root)
    poo_course = Course("POO-L2", "Programmation Orientée Objet", max_students=30)
    
    # Inscrire des étudiants
    poo_course.enroll_student("STU001")
    poo_course.enroll_student("STU002")
    poo_course.enroll_student("STU003")
    
    # Attribuer des notes (Value Objects)
    poo_course.assign_grade("STU001", Grade(15.5))
    poo_course.assign_grade("STU002", Grade(12.0))
    poo_course.assign_grade("STU003", Grade(8.5))
    
    # Logique métier de l'agrégat
    passing_rate = poo_course.get_passing_rate()
    print(f"\nTaux de réussite : {passing_rate:.1f}%")
    
    print("\n" + "=" * 70)
    print("PRINCIPES DDD APPLIQUÉS:")
    print("- Value Objects : Email, Grade (immutables)")
    print("- Entities : Student (identité)")
    print("- Aggregate : Course + CourseEnrollment")
    print("- Domain Service : AcademicService (logique transversale)")
    print("- Repository : Abstraction pour persistance")
    print("- Ubiquitous Language : enroll, grade, GPA, etc.")
    print("=" * 70)
```

---

## 8. Microservices vs Monolithe

### Architecture Monolithique

```
┌─────────────────────────────────────┐
│         APPLICATION                 │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │   UI     │  │   API    │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    BUSINESS LOGIC            │  │
│  │  • Students  • Courses       │  │
│  │  • Grades    • Payments      │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      DATABASE                │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
     Tout dans une seule application
```

**✅ Avantages :**
- Simple à développer et déployer
- Performances (pas de latence réseau)
- Transactions ACID simples
- Debugging facile

**❌ Inconvénients :**
- Scalabilité limitée (tout ou rien)
- Couplage fort
- Déploiements risqués (tout redémarre)
- Technologie unique

### Architecture Microservices

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Student    │  │   Course     │  │   Payment    │
│   Service    │  │   Service    │  │   Service    │
│              │  │              │  │              │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │ API    │  │  │  │ API    │  │  │  │ API    │  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │ Logic  │  │  │  │ Logic  │  │  │  │ Logic  │  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │   DB   │  │  │  │   DB   │  │  │  │   DB   │  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
└──────────────┘  └──────────────┘  └──────────────┘
   Services indépendants avec leurs propres bases
```

**✅ Avantages :**
- Scalabilité fine (scale un service spécifique)
- Déploiements indépendants
- Technologies différentes par service
- Équipes autonomes
- Résilience (un service down ≠ tout down)

**❌ Inconvénients :**
- Complexité (réseau, latence, failles)
- Transactions distribuées difficiles
- Debugging complexe
- Overhead opérationnel

### Quand utiliser quoi ?

**Monolithe si :**
- Petite équipe
- Application simple
- MVP rapide
- Domaine bien défini et stable

**Microservices si :**
- Équipes multiples
- Besoin de scalabilité différenciée
- Domaine complexe avec contextes multiples
- Évolution rapide et indépendante

---

## 9. Event-Driven Architecture

### Concept

Les composants communiquent via des **événements** plutôt que des appels directs.

```
┌──────────────┐                    ┌──────────────┐
│   Service A  │                    │   Service B  │
│              │                    │              │
│  Publish ────┼────→ [EVENT] ─────→│  Subscribe   │
│  Event       │      Queue         │  to Event    │
└──────────────┘                    └──────────────┘
```

### Exemple

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# EVENTS (Domain Events)
# ============================================================================

@dataclass
class Event:
    """Événement de base"""
    event_id: str
    timestamp: datetime
    event_type: str


@dataclass
class StudentEnrolledEvent(Event):
    """Événement : Étudiant inscrit"""
    student_id: str
    course_id: str
    
    def __init__(self, student_id: str, course_id: str):
        super().__init__(
            event_id=f"ENR-{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            event_type="STUDENT_ENROLLED"
        )
        self.student_id = student_id
        self.course_id = course_id


@dataclass
class GradeAssignedEvent(Event):
    """Événement : Note attribuée"""
    student_id: str
    course_id: str
    grade: float
    
    def __init__(self, student_id: str, course_id: str, grade: float):
        super().__init__(
            event_id=f"GRD-{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            event_type="GRADE_ASSIGNED"
        )
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade


# ============================================================================
# EVENT BUS
# ============================================================================

class EventBus:
    """Bus d'événements (publish/subscribe)"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        """S'abonner à un type d'événement"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(handler)
        print(f"[EventBus] Handler inscrit pour {event_type}")
    
    def publish(self, event: Event):
        """Publier un événement"""
        print(f"\n[EventBus] 📢 Publication: {event.event_type}")
        
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            handler(event)


# ============================================================================
# SERVICES (Event Publishers & Subscribers)
# ============================================================================

class EnrollmentService:
    """Service d'inscription (Publisher)"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def enroll_student(self, student_id: str, course_id: str):
        """Inscrire un étudiant"""
        # Logique métier
        print(f"[Enrollment] Inscription {student_id} au cours {course_id}")
        
        # Publier l'événement
        event = StudentEnrolledEvent(student_id, course_id)
        self.event_bus.publish(event)


class NotificationService:
    """Service de notification (Subscriber)"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        # S'abonner aux événements
        self.event_bus.subscribe("STUDENT_ENROLLED", self.on_student_enrolled)
        self.event_bus.subscribe("GRADE_ASSIGNED", self.on_grade_assigned)
    
    def on_student_enrolled(self, event: StudentEnrolledEvent):
        """Réagir à une inscription"""
        print(f"[Notification] 📧 Email envoyé à {event.student_id}")
        print(f"   Confirmation inscription au cours {event.course_id}")
    
    def on_grade_assigned(self, event: GradeAssignedEvent):
        """Réagir à une note"""
        print(f"[Notification] 📧 Email envoyé à {event.student_id}")
        print(f"   Note attribuée: {event.grade}/20 pour {event.course_id}")


class AnalyticsService:
    """Service d'analytique (Subscriber)"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.enrollment_count = 0
        self.grade_count = 0
        
        # S'abonner
        self.event_bus.subscribe("STUDENT_ENROLLED", self.on_student_enrolled)
        self.event_bus.subscribe("GRADE_ASSIGNED", self.on_grade_assigned)
    
    def on_student_enrolled(self, event: StudentEnrolledEvent):
        """Compter les inscriptions"""
        self.enrollment_count += 1
        print(f"[Analytics] 📊 Total inscriptions: {self.enrollment_count}")
    
    def on_grade_assigned(self, event: GradeAssignedEvent):
        """Compter les notes"""
        self.grade_count += 1
        print(f"[Analytics] 📊 Total notes attribuées: {self.grade_count}")


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EVENT-DRIVEN ARCHITECTURE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer le bus d'événements
    event_bus = EventBus()
    
    # Créer les services (auto-registration aux événements)
    notification_service = NotificationService(event_bus)
    analytics_service = AnalyticsService(event_bus)
    enrollment_service = EnrollmentService(event_bus)
    
    # Déclencher des actions
    print("\n--- Scénario: Inscriptions ---")
    enrollment_service.enroll_student("STU001", "POO-L2")
    enrollment_service.enroll_student("STU002", "POO-L2")
    
    # Publier d'autres événements
    print("\n--- Scénario: Attribution de notes ---")
    grade_event1 = GradeAssignedEvent("STU001", "POO-L2", 15.5)
    event_bus.publish(grade_event1)
    
    grade_event2 = GradeAssignedEvent("STU002", "POO-L2", 14.0)
    event_bus.publish(grade_event2)
    
    print("\n" + "=" * 70)
    print("AVANTAGES EVENT-DRIVEN:")
    print("- Découplage total des services")
    print("- Ajout de nouveaux subscribers sans modifier publishers")
    print("- Scalabilité (traitement asynchrone)")
    print("- Audit trail (historique des événements)")
    print("=" * 70)
```

---

## 10. Applications pour vos Projets

### Projet E-Commerce Campus

**Architecture recommandée :** Hexagonal + DDD

```python
# Bounded Contexts
- Catalog Context (produits)
- Order Context (commandes)
- Payment Context (paiements)
- Shipping Context (livraison)

# Aggregates
- Product (root)
- Order (root) + OrderItem
- Payment (root)

# Events
- ProductAddedToCart
- OrderPlaced
- PaymentProcessed
- OrderShipped
```

### Projet Plateforme de Cours

**Architecture recommandée :** Clean Architecture + Event-Driven

```python
# Layers
- Domain (Entities, Use Cases)
- Application (Services)
- Infrastructure (DB, APIs)
- Presentation (Web, Mobile)

# Events
- CoursePublished
- StudentEnrolled
- LessonCompleted
- CertificateIssued
```

### Projet Réseau Social

**Architecture recommandée :** Microservices

```python
# Services
- User Service
- Post Service
- Feed Service
- Notification Service
- Search Service

# Communication
- Synchrone (REST) pour queries
- Asynchrone (Events) pour updates
```

---