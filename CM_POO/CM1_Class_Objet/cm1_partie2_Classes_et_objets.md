# CM1 - Classes et Objets (Partie 2)
## Méthodes de Classe, Relations entre Objets et Patterns

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ Classes et objets
- ✅ Attributs (classe vs instance)
- ✅ Méthodes et `self`
- ✅ Méthodes spéciales (`__init__`, `__str__`, `__eq__`, etc.)
- ✅ Propriétés et encapsulation

**Aujourd'hui :**
- Méthodes de classe et méthodes statiques
- Relations entre objets
- Composition et Agrégation
- Patterns de conception de base
- Exercices pratiques

---

## 6. Méthodes de Classe et Méthodes Statiques

### 6.1 Méthodes de Classe (@classmethod)

> **Une méthode de classe reçoit la classe (pas l'instance) comme premier paramètre.**

**Utilisation typique :**
- Factory methods (méthodes de construction alternatives)
- Opérations sur des attributs de classe
- Compteurs globaux

```python
from datetime import datetime


class Student:
    """Étudiant avec méthodes de classe"""
    
    # Attributs de classe
    university = "Université des Antilles"
    student_count = 0
    all_students = []
    
    def __init__(self, student_id, name, email, birth_year):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.birth_year = birth_year
        
        # Incrémenter le compteur
        Student.student_count += 1
        Student.all_students.append(self)
    
    # Méthode d'instance classique
    def get_age(self):
        """Calcule l'âge (méthode d'instance)"""
        current_year = datetime.now().year
        return current_year - self.birth_year
    
    # Méthode de classe
    @classmethod
    def from_email(cls, email):
        """
        Factory method : crée un étudiant à partir de l'email
        cls = la classe Student
        """
        # Extraire les infos de l'email
        # Format: prenom.nom.ANNEE@etudiant.ua.fr
        local_part = email.split('@')[0]
        parts = local_part.split('.')
        
        first_name = parts[0].capitalize()
        last_name = parts[1].capitalize()
        birth_year = int(parts[2]) if len(parts) > 2 else 2000
        
        # Générer un ID
        student_id = f"STU{cls.student_count + 1:04d}"
        
        # Créer l'instance
        return cls(student_id, f"{first_name} {last_name}", email, birth_year)
    
    @classmethod
    def from_dict(cls, data):
        """
        Factory method : crée un étudiant à partir d'un dictionnaire
        """
        return cls(
            data['student_id'],
            data['name'],
            data['email'],
            data.get('birth_year', 2000)
        )
    
    @classmethod
    def get_total_students(cls):
        """Retourne le nombre total d'étudiants"""
        return cls.student_count
    
    @classmethod
    def get_students_by_year(cls, birth_year):
        """Filtre les étudiants par année de naissance"""
        return [s for s in cls.all_students if s.birth_year == birth_year]
    
    @classmethod
    def reset_counter(cls):
        """Réinitialise le compteur (pour les tests)"""
        cls.student_count = 0
        cls.all_students = []
    
    def __str__(self):
        return f"{self.name} (ID: {self.student_id}, Age: {self.get_age()})"


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MÉTHODES DE CLASSE - DÉMONSTRATION")
    print("=" * 70)
    
    # Création classique
    print("\n--- Création classique ---")
    marie = Student("STU0001", "Marie Lafleur", "marie@ua.fr", 2003)
    print(f"✓ {marie}")
    
    # Factory method : from_email
    print("\n--- Factory method: from_email ---")
    jean = Student.from_email("jean.martin.2002@etudiant.ua.fr")
    print(f"✓ {jean}")
    
    sophie = Student.from_email("sophie.bernard.2003@etudiant.ua.fr")
    print(f"✓ {sophie}")
    
    # Factory method : from_dict
    print("\n--- Factory method: from_dict ---")
    data = {
        'student_id': 'STU0004',
        'name': 'Paul Dubois',
        'email': 'paul@ua.fr',
        'birth_year': 2002
    }
    paul = Student.from_dict(data)
    print(f"✓ {paul}")
    
    # Méthodes de classe pour statistiques
    print("\n--- Statistiques (méthodes de classe) ---")
    print(f"Total d'étudiants: {Student.get_total_students()}")
    
    students_2003 = Student.get_students_by_year(2003)
    print(f"Étudiants nés en 2003: {len(students_2003)}")
    for student in students_2003:
        print(f"  - {student}")
```

**Différence clé :**
```python
class MyClass:
    count = 0
    
    def instance_method(self):
        # self = instance spécifique
        return self
    
    @classmethod
    def class_method(cls):
        # cls = la classe MyClass
        return cls
    
    @staticmethod
    def static_method():
        # Aucun accès automatique à la classe ou l'instance
        return "static"
```

### 6.2 Méthodes Statiques (@staticmethod)

> **Une méthode statique n'a accès ni à l'instance ni à la classe. C'est une fonction normale dans l'espace de noms de la classe.**

**Utilisation typique :**
- Fonctions utilitaires liées conceptuellement à la classe
- Validation
- Conversions

```python
class Student:
    """Étudiant avec méthodes statiques"""
    
    def __init__(self, student_id, name, email):
        # Validation avec méthode statique
        if not Student.is_valid_email(email):
            raise ValueError(f"Email invalide: {email}")
        
        if not Student.is_valid_student_id(student_id):
            raise ValueError(f"ID invalide: {student_id}")
        
        self.student_id = student_id
        self.name = name
        self.email = email
    
    @staticmethod
    def is_valid_email(email):
        """
        Valide le format d'un email
        Pas besoin de self ou cls
        """
        if '@' not in email:
            return False
        
        local, domain = email.split('@', 1)
        
        if len(local) < 1 or len(domain) < 3:
            return False
        
        if '.' not in domain:
            return False
        
        return True
    
    @staticmethod
    def is_valid_student_id(student_id):
        """Valide le format d'un ID étudiant"""
        # Format attendu: STU suivi de 4 chiffres
        if len(student_id) != 7:
            return False
        
        if not student_id.startswith('STU'):
            return False
        
        if not student_id[3:].isdigit():
            return False
        
        return True
    
    @staticmethod
    def format_name(first_name, last_name):
        """Formate un nom correctement"""
        return f"{first_name.strip().title()} {last_name.strip().title()}"
    
    @staticmethod
    def calculate_grade_category(grade):
        """
        Catégorise une note
        Fonction utilitaire liée aux étudiants
        """
        if grade >= 16:
            return "Très Bien"
        elif grade >= 14:
            return "Bien"
        elif grade >= 12:
            return "Assez Bien"
        elif grade >= 10:
            return "Passable"
        else:
            return "Insuffisant"

# Démonstration
print("\n--- Méthodes statiques ---")

# Utilisation sans créer d'instance
print(f"Email valide ? {Student.is_valid_email('marie@ua.fr')}")  # True
print(f"Email valide ? {Student.is_valid_email('invalid')}")      # False

print(f"ID valide ? {Student.is_valid_student_id('STU0001')}")    # True
print(f"ID valide ? {Student.is_valid_student_id('ABC1234')}")    # False

# Formatage
name = Student.format_name("  marie  ", "  LAFLEUR  ")
print(f"Nom formaté: {name}")  # Marie Lafleur

# Catégorisation
print(f"Note 15: {Student.calculate_grade_category(15)}")  # Bien
```

### 6.3 Comparaison des 3 types de méthodes

```python
class Example:
    class_var = "classe"
    
    def __init__(self, value):
        self.instance_var = value
    
    # MÉTHODE D'INSTANCE
    def instance_method(self):
        """
        - Reçoit self (l'instance)
        - Peut accéder aux attributs d'instance
        - Peut accéder aux attributs de classe
        - Cas d'usage : opérations sur l'instance
        """
        return f"Instance: {self.instance_var}, Classe: {self.class_var}"
    
    # MÉTHODE DE CLASSE
    @classmethod
    def class_method(cls):
        """
        - Reçoit cls (la classe)
        - Ne peut PAS accéder aux attributs d'instance
        - Peut accéder aux attributs de classe
        - Cas d'usage : factory methods, opérations sur la classe
        """
        return f"Classe: {cls.class_var}, Instance: impossible"
    
    # MÉTHODE STATIQUE
    @staticmethod
    def static_method():
        """
        - Ne reçoit ni self ni cls
        - Ne peut accéder ni aux attributs d'instance ni de classe
        - Cas d'usage : fonctions utilitaires
        """
        return "Fonction utilitaire indépendante"


# Utilisation
obj = Example("valeur")

print(obj.instance_method())  # Méthode d'instance
print(obj.class_method())     # Méthode de classe (via instance)
print(Example.class_method()) # Méthode de classe (via classe)
print(obj.static_method())    # Méthode statique (via instance)
print(Example.static_method())# Méthode statique (via classe)
```

**Quand utiliser quoi ?**

| Type | Accès à | Utilisation |
|------|---------|-------------|
| **Instance** | `self`, attributs instance & classe | Opérations sur l'objet |
| **Classe** | `cls`, attributs classe seulement | Factory methods, stats globales |
| **Statique** | Rien automatiquement | Fonctions utilitaires |

---

## 7. Relations entre Objets

### 7.1 Association

> **Relation la plus générale : un objet "connaît" un autre objet.**

```python
class Student:
    """Étudiant"""
    def __init__(self, name):
        self.name = name
        self.enrolled_courses = []  # Association avec Course
    
    def enroll(self, course):
        self.enrolled_courses.append(course)
        course.add_student(self)


class Course:
    """Cours"""
    def __init__(self, name):
        self.name = name
        self.students = []  # Association avec Student
    
    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)


# Association bidirectionnelle
marie = Student("Marie")
poo = Course("POO")

marie.enroll(poo)  # Marie connaît POO, POO connaît Marie

print(f"{marie.name} inscrit dans: {[c.name for c in marie.enrolled_courses]}")
print(f"{poo.name} a {len(poo.students)} étudiant(s)")
```

### 7.2 Agrégation

> **Relation "a un" (has-a) où les parties peuvent exister indépendamment du tout.**

**Exemple :** Un département a des professeurs, mais les professeurs peuvent exister sans le département.

```python
class Professor:
    """Professeur (existe indépendamment)"""
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
    
    def __str__(self):
        return f"Prof. {self.name} ({self.specialty})"


class Department:
    """Département (agrège des professeurs)"""
    def __init__(self, name):
        self.name = name
        self.professors = []  # Agrégation
    
    def add_professor(self, professor):
        """Ajoute un professeur au département"""
        if professor not in self.professors:
            self.professors.append(professor)
    
    def remove_professor(self, professor):
        """Retire un professeur"""
        if professor in self.professors:
            self.professors.remove(professor)
    
    def list_professors(self):
        """Liste les professeurs"""
        print(f"\nProfesseurs du département {self.name}:")
        for prof in self.professors:
            print(f"  - {prof}")


# Démonstration
cs_dept = Department("Informatique")
math_dept = Department("Mathématiques")

# Créer des professeurs (existent indépendamment)
prof_roor = Professor("Roor", "POO")
prof_smith = Professor("Smith", "Algorithmes")

# Ajouter aux départements
cs_dept.add_professor(prof_roor)
cs_dept.add_professor(prof_smith)

cs_dept.list_professors()

# Le professeur peut changer de département
cs_dept.remove_professor(prof_smith)
math_dept.add_professor(prof_smith)

# Les professeurs existent toujours même si on supprime le département
del cs_dept
print(f"\n{prof_roor} existe toujours!")
print(f"{prof_smith} existe toujours!")
```

### 7.3 Composition

> **Relation "fait partie de" (part-of) forte : les parties n'existent pas sans le tout.**

**Exemple :** Un cours a des chapitres. Si on supprime le cours, les chapitres disparaissent.

```python
class Chapter:
    """Chapitre (n'existe que dans le contexte d'un cours)"""
    def __init__(self, number, title, content):
        self.number = number
        self.title = title
        self.content = content
    
    def __str__(self):
        return f"Chapitre {self.number}: {self.title}"


class Course:
    """Cours (possède des chapitres)"""
    def __init__(self, name):
        self.name = name
        self._chapters = []  # Composition (forte)
    
    def add_chapter(self, title, content):
        """
        Crée et ajoute un chapitre
        Le chapitre est créé À L'INTÉRIEUR du cours
        """
        chapter_number = len(self._chapters) + 1
        chapter = Chapter(chapter_number, title, content)
        self._chapters.append(chapter)
        return chapter
    
    def get_chapter(self, number):
        """Récupère un chapitre par son numéro"""
        for chapter in self._chapters:
            if chapter.number == number:
                return chapter
        return None
    
    def list_chapters(self):
        """Liste tous les chapitres"""
        print(f"\nChapitre du cours {self.name}:")
        for chapter in self._chapters:
            print(f"  {chapter}")
    
    def __del__(self):
        """Quand le cours est supprimé, les chapitres aussi"""
        print(f"\n[Destruction] Cours {self.name} supprimé")
        print(f"[Destruction] Ses {len(self._chapters)} chapitres sont aussi supprimés")


# Démonstration
poo_course = Course("Programmation Orientée Objet")

# Les chapitres sont créés DANS le cours
poo_course.add_chapter("Introduction", "Qu'est-ce que la POO...")
poo_course.add_chapter("Classes et Objets", "Définition d'une classe...")
poo_course.add_chapter("Héritage", "Principe de l'héritage...")

poo_course.list_chapters()

# Si on supprime le cours, les chapitres disparaissent
del poo_course
# [Destruction] Cours POO supprimé
# [Destruction] Ses 3 chapitres sont aussi supprimés
```

### 7.4 Comparaison Agrégation vs Composition

```python
# AGRÉGATION (relation faible)
class Team:
    def __init__(self):
        self.members = []  # Les membres existent indépendamment
    
    def add_member(self, member):
        self.members.append(member)

member = Player("Marie")  # Existe avant
team = Team()
team.add_member(member)   # Ajouté au team
del team                  # Team supprimée, mais Marie existe toujours


# COMPOSITION (relation forte)
class House:
    def __init__(self):
        self.rooms = []
    
    def add_room(self, name, size):
        # La pièce est créée DANS la maison
        room = Room(name, size)  # Créé ici
        self.rooms.append(room)

house = House()
house.add_room("Salon", 30)  # Room créée dans House
del house                     # House ET rooms supprimés
```

**Résumé :**

| Relation | Signification | Vie du composant | Exemple |
|----------|---------------|------------------|---------|
| **Association** | "connaît" | Indépendante | Student - Course |
| **Agrégation** | "a un" (faible) | Indépendante | Department - Professor |
| **Composition** | "fait partie de" (forte) | Dépendante | Course - Chapter |

---

## 8. Patterns de Conception de Base

### 8.1 Pattern Singleton (preview du CM4)

> **Garantir qu'une classe n'a qu'une seule instance.**

```python
class DatabaseConnection:
    """Connexion unique à la base de données"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.host = "localhost"
            self.port = 5432
            self.connected = False
            self._initialized = True
            print("[DB] Nouvelle connexion créée")
    
    def connect(self):
        if not self.connected:
            print(f"[DB] Connexion à {self.host}:{self.port}")
            self.connected = True
        else:
            print("[DB] Déjà connecté")


# Démonstration
db1 = DatabaseConnection()  # Crée l'instance
db2 = DatabaseConnection()  # Retourne la même instance
db3 = DatabaseConnection()  # Retourne la même instance

print(f"db1 is db2 ? {db1 is db2}")  # True
print(f"db2 is db3 ? {db2 is db3}")  # True

db1.connect()
db2.connect()  # Déjà connecté (car c'est le même objet)
```

### 8.2 Pattern Factory (preview du CM4)

> **Déléguer la création d'objets à une méthode dédiée.**

```python
from enum import Enum


class StudentType(Enum):
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    PHD = "phd"


class Student:
    """Étudiant de base"""
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
    
    def get_info(self):
        return f"Student: {self.name}"


class UndergraduateStudent(Student):
    """Étudiant en Licence"""
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self.level = "Licence"
    
    def get_info(self):
        return f"Licence: {self.name}"


class GraduateStudent(Student):
    """Étudiant en Master"""
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self.level = "Master"
    
    def get_info(self):
        return f"Master: {self.name}"


class PhDStudent(Student):
    """Doctorant"""
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self.level = "Doctorat"
        self.thesis_topic = None
    
    def get_info(self):
        return f"Doctorat: {self.name}"


class StudentFactory:
    """Factory pour créer des étudiants"""
    
    @staticmethod
    def create_student(student_type: StudentType, name: str, student_id: str):
        """Crée un étudiant selon son type"""
        if student_type == StudentType.UNDERGRADUATE:
            return UndergraduateStudent(name, student_id)
        elif student_type == StudentType.GRADUATE:
            return GraduateStudent(name, student_id)
        elif student_type == StudentType.PHD:
            return PhDStudent(name, student_id)
        else:
            raise ValueError(f"Type inconnu: {student_type}")


# Démonstration
factory = StudentFactory()

marie = factory.create_student(StudentType.UNDERGRADUATE, "Marie", "L1001")
jean = factory.create_student(StudentType.GRADUATE, "Jean", "M2001")
sophie = factory.create_student(StudentType.PHD, "Sophie", "D3001")

for student in [marie, jean, sophie]:
    print(student.get_info())
```

---

## 9. Exercices Pratiques

### Exercice 1 : Bibliothèque

Créez un système de gestion de bibliothèque avec :

**Classes :**
- `Book` : ISBN, titre, auteur, disponible
- `Member` : ID, nom, livres empruntés (max 5)
- `Library` : nom, livres, membres

**Fonctionnalités :**
- Ajouter/retirer des livres
- Inscrire des membres
- Emprunter/retourner des livres
- Lister les livres disponibles
- Statistiques (total livres, emprunts en cours, etc.)

```python
# À compléter
class Book:
    # Votre code ici
    pass

class Member:
    # Votre code ici
    pass

class Library:
    # Votre code ici
    pass
```

### Exercice 2 : Restaurant Universitaire

Créez un système de gestion de restaurant universitaire :

**Classes :**
- `Dish` : nom, prix, catégorie (entrée/plat/dessert), allergènes
- `Menu` : date, liste de plats
- `Order` : étudiant, plats commandés, total
- `Cafeteria` : menus, commandes

**Méthodes spéciales à implémenter :**
- `__str__` et `__repr__` pour tous
- `__len__` pour Menu et Order
- `__add__` pour combiner des menus

### Exercice 3 : Système de Réservation

Créez un système de réservation de salles :

**Classes :**
- `Room` : nom, capacité, équipement
- `Reservation` : salle, date, heure début/fin, organisateur
- `ReservationSystem` : salles, réservations

**Utiliser :**
- Méthodes de classe pour créer des réservations standards
- Méthodes statiques pour valider les créneaux
- Propriétés pour calculer la durée
- Composition pour les équipements

---

## 10. Cas Pratique Complet

```python
from datetime import datetime, timedelta
from typing import List, Optional


class Book:
    """Livre de bibliothèque"""
    
    book_count = 0
    
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = True
        self.borrower = None
        self.due_date = None
        
        Book.book_count += 1
    
    @classmethod
    def from_dict(cls, data):
        """Factory method depuis dictionnaire"""
        return cls(data['isbn'], data['title'], data['author'])
    
    @staticmethod
    def is_valid_isbn(isbn):
        """Valide un ISBN-13"""
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        return True
    
    def borrow(self, member: 'Member', days: int = 14):
        """Emprunte le livre"""
        if not self.available:
            return False
        
        self.available = False
        self.borrower = member
        self.due_date = datetime.now() + timedelta(days=days)
        return True
    
    def return_book(self):
        """Retourne le livre"""
        if self.available:
            return False
        
        self.available = True
        self.borrower = None
        self.due_date = None
        return True
    
    def is_overdue(self):
        """Vérifie si le livre est en retard"""
        if self.available or not self.due_date:
            return False
        return datetime.now() > self.due_date
    
    def __str__(self):
        status = "✓ Disponible" if self.available else f"✗ Emprunté"
        return f"{self.title} par {self.author} - {status}"
    
    def __repr__(self):
        return f"Book('{self.isbn}', '{self.title}', '{self.author}')"


class Member:
    """Membre de la bibliothèque"""
    
    MAX_BOOKS = 5
    member_count = 0
    
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_books: List[Book] = []
        
        Member.member_count += 1
    
    @property
    def can_borrow(self):
        """Vérifie si le membre peut emprunter"""
        return len(self.borrowed_books) < self.MAX_BOOKS
    
    def borrow_book(self, book: Book):
        """Emprunte un livre"""
        if not self.can_borrow:
            print(f"✗ {self.name} a atteint la limite ({self.MAX_BOOKS} livres)")
            return False
        
        if book.borrow(self):
            self.borrowed_books.append(book)
            print(f"✓ {self.name} a emprunté '{book.title}'")
            return True
        else:
            print(f"✗ '{book.title}' non disponible")
            return False
    
    def return_book(self, book: Book):
        """Retourne un livre"""
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            print(f"✓ {self.name} a retourné '{book.title}'")
            return True
        else:
            print(f"✗ {self.name} n'a pas emprunté ce livre")
            return False
    
    def get_overdue_books(self):
        """Liste les livres en retard"""
        return [book for book in self.borrowed_books if book.is_overdue()]
    
    def __len__(self):
        return len(self.borrowed_books)
    
    def __str__(self):
        return f"{self.name} ({self.member_id}) - {len(self)} livre(s)"


class Library:
    """Bibliothèque"""
    
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []
        self.members: List[Member] = []
    
    def add_book(self, book: Book):
        """Ajoute un livre au catalogue"""
        if book not in self.books:
            self.books.append(book)
            print(f"✓ Livre ajouté: {book.title}")
    
    def register_member(self, member: Member):
        """Inscrit un membre"""
        if member not in self.members:
            self.members.append(member)
            print(f"✓ Membre inscrit: {member.name}")
    
    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Recherche un livre par ISBN"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_books_by_author(self, author: str) -> List[Book]:
        """Recherche par auteur"""
        return [b for b in self.books if author.lower() in b.author.lower()]
    
    def get_available_books(self) -> List[Book]:
        """Liste des livres disponibles"""
        return [b for b in self.books if b.available]
    
    def get_statistics(self):
        """Statistiques de la bibliothèque"""
        total_books = len(self.books)
        available = len(self.get_available_books())
        borrowed = total_books - available
        total_members = len(self.members)
        
        print(f"\n{'=' * 60}")
        print(f"STATISTIQUES - {self.name}")
        print(f"{'=' * 60}")
        print(f"Livres au catalogue: {total_books}")
        print(f"Livres disponibles: {available}")
        print(f"Livres empruntés: {borrowed}")
        print(f"Membres inscrits: {total_members}")
        print(f"{'=' * 60}\n")


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE BIBLIOTHÈQUE - CAS PRATIQUE COMPLET")
    print("=" * 70)
    
    # Créer la bibliothèque
    library = Library("Bibliothèque Universitaire des Antilles")
    
    # Ajouter des livres
    print("\n--- Ajout de livres ---")
    book1 = Book("9780134685991", "Effective Java", "Joshua Bloch")
    book2 = Book("9780135957059", "Clean Code", "Robert Martin")
    book3 = Book("9780201633610", "Design Patterns", "Gang of Four")
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    
    # Inscrire des membres
    print("\n--- Inscription de membres ---")
    marie = Member("M001", "Marie Lafleur")
    jean = Member("M002", "Jean Martin")
    
    library.register_member(marie)
    library.register_member(jean)
    
    # Emprunts
    print("\n--- Emprunts ---")
    marie.borrow_book(book1)
    marie.borrow_book(book2)
    jean.borrow_book(book3)
    
    # Tentative d'emprunt d'un livre déjà emprunté
    jean.borrow_book(book1)
    
    # Statistiques
    library.get_statistics()
    
    # Retour
    print("--- Retours ---")
    marie.return_book(book1)
    
    # Statistiques finales
    library.get_statistics()
    
    print(f"\nTotal de livres créés: {Book.book_count}")
    print(f"Total de membres inscrits: {Member.member_count}")
```

---

## 11. Conclusion du CM1

### Récapitulatif complet

**Partie 1 :**
- ✅ Introduction à la POO
- ✅ Classes et objets
- ✅ Attributs et méthodes
- ✅ Méthodes spéciales
- ✅ Encapsulation et propriétés

**Partie 2 :**
- ✅ Méthodes de classe (@classmethod)
- ✅ Méthodes statiques (@staticmethod)
- ✅ Relations entre objets (Association, Agrégation, Composition)
- ✅ Patterns de base (Singleton, Factory)
- ✅ Cas pratique complet

### Concepts maîtrisés

1. **Classe** = Modèle pour créer des objets
2. **Objet** = Instance d'une classe
3. **`self`** = Référence à l'instance
4. **`cls`** = Référence à la classe
5. **Méthodes spéciales** = Comportements personnalisés
6. **Propriétés** = Getters/setters élégants
7. **Relations** = Comment les objets interagissent

### Prochains cours

**CM2 : Héritage, Composition et MRO**
- Héritage simple et multiple
- Surcharge de méthodes
- `super()` et MRO
- Composition vs Héritage

**CM3 : Polymorphisme et Abstraction**
- Polymorphisme
- Classes abstraites
- Interfaces (protocols)
- Duck typing

---

*Fin du CM1 - Classes et Objets*