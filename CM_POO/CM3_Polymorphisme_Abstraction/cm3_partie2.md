# CM3 - Polymorphisme et Abstraction (Partie 2)
## Classes Abstraites, Duck Typing et Protocols

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ Polymorphisme par héritage
- ✅ Collections hétérogènes
- ✅ Surcharge d'opérateurs
- ✅ Strategy Pattern

**Aujourd'hui - Partie 2 :**
- **Classes abstraites** (ABC)
- **Duck typing**
- **Protocols** (Python 3.8+)
- **Type hints avancés**
- **Cas pratiques complets**

---

## 6. Classes Abstraites (ABC)

### 6.1 Introduction

> **Une classe abstraite définit une interface que les classes dérivées DOIVENT implémenter.**

**Caractéristiques :**
- ❌ Ne peut PAS être instanciée directement
- ✅ Contient des méthodes abstraites (sans implémentation)
- ✅ Peut contenir des méthodes concrètes (avec implémentation)
- ✅ Définit un "contrat" pour les sous-classes

### 6.2 Syntaxe de Base

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    """Classe abstraite"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def make_sound(self):
        """Méthode abstraite : DOIT être implémentée"""
        pass
    
    @abstractmethod
    def move(self):
        """Méthode abstraite : DOIT être implémentée"""
        pass
    
    def sleep(self):
        """Méthode concrète : peut être utilisée telle quelle"""
        print(f"{self.name} dort")


# ✗ Impossible d'instancier une classe abstraite
# animal = Animal("Test")  # TypeError


class Dog(Animal):
    """Classe concrète : implémente TOUTES les méthodes abstraites"""
    
    def make_sound(self):
        """Implémentation obligatoire"""
        print(f"{self.name} aboie: Woof!")
    
    def move(self):
        """Implémentation obligatoire"""
        print(f"{self.name} court")


class Cat(Animal):
    """Classe concrète"""
    
    def make_sound(self):
        print(f"{self.name} miaule: Miaou!")
    
    def move(self):
        print(f"{self.name} marche silencieusement")


# ✓ On peut maintenant instancier les classes concrètes
dog = Dog("Rex")
cat = Cat("Minou")

dog.make_sound()  # Woof!
dog.move()        # court
dog.sleep()       # dort (méthode concrète héritée)

cat.make_sound()  # Miaou!
cat.move()        # marche
cat.sleep()       # dort
```

### 6.3 Pourquoi utiliser des Classes Abstraites ?

**1. Définir un contrat**
```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """
    Contrat : toute classe de paiement DOIT implémenter ces méthodes
    """
    
    @abstractmethod
    def validate(self) -> bool:
        """Valide les informations de paiement"""
        pass
    
    @abstractmethod
    def process(self, amount: float) -> dict:
        """Traite le paiement"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Rembourse une transaction"""
        pass


# ✗ Si on oublie une méthode, erreur au moment de l'instanciation
class IncompletePayment(PaymentProcessor):
    def validate(self) -> bool:
        return True
    
    # Oubli de process() et refund()

# payment = IncompletePayment()  # TypeError: Can't instantiate abstract class
```

**2. Forcer l'implémentation**

```python
class Database(ABC):
    """Base de données abstraite"""
    
    @abstractmethod
    def connect(self):
        """Connexion obligatoire"""
        pass
    
    @abstractmethod
    def query(self, sql: str):
        """Requête obligatoire"""
        pass
    
    def log(self, message: str):
        """Méthode concrète : logging par défaut"""
        print(f"[DB] {message}")


class PostgreSQL(Database):
    """Implémentation PostgreSQL"""
    
    def connect(self):
        self.log("Connexion à PostgreSQL")
        # Code de connexion spécifique
    
    def query(self, sql: str):
        self.log(f"Exécution: {sql}")
        # Code de requête spécifique


class MongoDB(Database):
    """Implémentation MongoDB"""
    
    def connect(self):
        self.log("Connexion à MongoDB")
    
    def query(self, sql: str):
        self.log(f"Exécution NoSQL: {sql}")
```

---

## 7. Exemple Complet : Système de Repository

```python
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic


T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """
    Repository abstrait générique
    Définit l'interface CRUD de base
    """
    
    @abstractmethod
    def save(self, entity: T) -> None:
        """Sauvegarde une entité"""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Trouve par ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Trouve tous"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Supprime une entité"""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Compte le nombre d'entités"""
        pass


# ============================================================================
# ENTITÉS
# ============================================================================

class Student:
    """Étudiant"""
    
    def __init__(self, student_id: str, name: str, email: str):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
    
    def __str__(self):
        return f"Student({self.student_id}, {self.name})"


class Course:
    """Cours"""
    
    def __init__(self, course_id: str, name: str, credits: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits
    
    def __str__(self):
        return f"Course({self.course_id}, {self.name})"


# ============================================================================
# IMPLÉMENTATIONS CONCRÈTES
# ============================================================================

class InMemoryStudentRepository(Repository[Student]):
    """Repository en mémoire pour Student"""
    
    def __init__(self):
        self._students: dict[str, Student] = {}
    
    def save(self, entity: Student) -> None:
        self._students[entity.student_id] = entity
        print(f"✓ {entity} sauvegardé")
    
    def find_by_id(self, entity_id: str) -> Optional[Student]:
        return self._students.get(entity_id)
    
    def find_all(self) -> List[Student]:
        return list(self._students.values())
    
    def delete(self, entity_id: str) -> bool:
        if entity_id in self._students:
            del self._students[entity_id]
            return True
        return False
    
    def count(self) -> int:
        return len(self._students)


class InMemoryCourseRepository(Repository[Course]):
    """Repository en mémoire pour Course"""
    
    def __init__(self):
        self._courses: dict[str, Course] = {}
    
    def save(self, entity: Course) -> None:
        self._courses[entity.course_id] = entity
        print(f"✓ {entity} sauvegardé")
    
    def find_by_id(self, entity_id: str) -> Optional[Course]:
        return self._courses.get(entity_id)
    
    def find_all(self) -> List[Course]:
        return list(self._courses.values())
    
    def delete(self, entity_id: str) -> bool:
        if entity_id in self._courses:
            del self._courses[entity_id]
            return True
        return False
    
    def count(self) -> int:
        return len(self._courses)


# ============================================================================
# SERVICE UTILISANT LES REPOSITORIES
# ============================================================================

class UniversityService:
    """Service universitaire utilisant les repositories"""
    
    def __init__(self, 
                 student_repo: Repository[Student],
                 course_repo: Repository[Course]):
        self.student_repo = student_repo
        self.course_repo = course_repo
    
    def register_student(self, student_id: str, name: str, email: str):
        """Inscrit un nouvel étudiant"""
        student = Student(student_id, name, email)
        self.student_repo.save(student)
    
    def create_course(self, course_id: str, name: str, credits: int):
        """Crée un nouveau cours"""
        course = Course(course_id, name, credits)
        self.course_repo.save(course)
    
    def get_statistics(self):
        """Statistiques"""
        return {
            'total_students': self.student_repo.count(),
            'total_courses': self.course_repo.count()
        }


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CLASSES ABSTRAITES - REPOSITORY PATTERN")
    print("=" * 70)
    
    # Créer les repositories
    student_repo = InMemoryStudentRepository()
    course_repo = InMemoryCourseRepository()
    
    # Créer le service
    service = UniversityService(student_repo, course_repo)
    
    # Utiliser le service
    print("\n--- Inscriptions ---")
    service.register_student("20231001", "Marie Lafleur", "marie@ua.fr")
    service.register_student("20231002", "Jean Martin", "jean@ua.fr")
    service.register_student("20231003", "Sophie Bernard", "sophie@ua.fr")
    
    print("\n--- Création de cours ---")
    service.create_course("POO", "Programmation Orientée Objet", 6)
    service.create_course("WEB", "Développement Web", 6)
    
    # Statistiques
    stats = service.get_statistics()
    print(f"\n--- Statistiques ---")
    print(f"Étudiants: {stats['total_students']}")
    print(f"Cours: {stats['total_courses']}")
    
    print("\n" + "=" * 70)
    print("AVANTAGES DES CLASSES ABSTRAITES:")
    print("- Contrat clair et forcé")
    print("- Facilite les tests (mock repositories)")
    print("- Changement d'implémentation transparent")
    print("- Documentation vivante du code")
    print("=" * 70)
```

---

## 8. Duck Typing

### 8.1 Principe

> **"If it walks like a duck and quacks like a duck, it must be a duck."**

**En Python, on ne vérifie pas le TYPE, on vérifie le COMPORTEMENT.**

```python
class Duck:
    """Canard réel"""
    
    def swim(self):
        print("Le canard nage")
    
    def quack(self):
        print("Coin coin!")


class Person:
    """Personne qui imite un canard"""
    
    def swim(self):
        print("La personne nage")
    
    def quack(self):
        print("La personne fait coin coin!")


class Robot:
    """Robot qui imite un canard"""
    
    def swim(self):
        print("Le robot flotte")
    
    def quack(self):
        print("BEEP BOOP (coin coin)")


def make_it_duck(thing):
    """
    Duck typing : on ne vérifie PAS isinstance(thing, Duck)
    On essaie juste d'utiliser les méthodes
    """
    thing.swim()
    thing.quack()


# Démonstration
print("\n--- Duck Typing ---")

for thing in [Duck(), Person(), Robot()]:
    print(f"\n{thing.__class__.__name__}:")
    make_it_duck(thing)
```

**Sortie :**
```
--- Duck Typing ---

Duck:
Le canard nage
Coin coin!

Person:
La personne nage
La personne fait coin coin!

Robot:
Le robot flotte
BEEP BOOP (coin coin)
```

### 8.2 Duck Typing vs Classes Abstraites

```python
# ============================================================================
# APPROCHE 1 : Duck Typing (Python way)
# ============================================================================

class FileWriter:
    """Écrit dans un fichier"""
    
    def write(self, data: str):
        print(f"[File] Écriture: {data}")


class DatabaseWriter:
    """Écrit dans une base de données"""
    
    def write(self, data: str):
        print(f"[DB] Insertion: {data}")


class NetworkWriter:
    """Envoie sur le réseau"""
    
    def write(self, data: str):
        print(f"[Network] Envoi: {data}")


def save_data(writer, data: str):
    """Duck typing : accepte tout ce qui a write()"""
    writer.write(data)


# ============================================================================
# APPROCHE 2 : Classes Abstraites (strict way)
# ============================================================================

from abc import ABC, abstractmethod


class Writer(ABC):
    """Interface Writer"""
    
    @abstractmethod
    def write(self, data: str):
        pass


class FileWriterStrict(Writer):
    """Implémentation stricte"""
    
    def write(self, data: str):
        print(f"[File] Écriture: {data}")


def save_data_strict(writer: Writer, data: str):
    """Approche stricte : writer DOIT hériter de Writer"""
    writer.write(data)


# Démonstration
print("\n--- Duck Typing vs Classes Abstraites ---")

# Duck typing : flexible
save_data(FileWriter(), "test1")
save_data(DatabaseWriter(), "test2")

# Classes abstraites : stricte mais plus sûre
save_data_strict(FileWriterStrict(), "test3")
```

**Avantages/Inconvénients :**

| Approche | Avantages | Inconvénients |
|----------|-----------|---------------|
| **Duck Typing** | Flexible, pythonique | Erreurs au runtime |
| **Classes Abstraites** | Sûr, vérifié | Plus verbeux |

---

## 9. Protocols (Python 3.8+)

### 9.1 Introduction

> **Les Protocols permettent le duck typing avec vérification statique (type checking).**

**Meilleur des deux mondes :**
- ✅ Flexibilité du duck typing
- ✅ Sécurité des classes abstraites
- ✅ Pas besoin d'héritage explicite

```python
from typing import Protocol


class Drawable(Protocol):
    """
    Protocol : définit une interface structurelle
    Pas besoin d'hériter explicitement
    """
    
    def draw(self) -> None:
        ...


class Circle:
    """N'hérite PAS de Drawable, mais est compatible"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def draw(self) -> None:
        print(f"🔵 Cercle (rayon: {self.radius})")


class Rectangle:
    """N'hérite PAS de Drawable, mais est compatible"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def draw(self) -> None:
        print(f"🟦 Rectangle ({self.width}x{self.height})")


def render(shape: Drawable) -> None:
    """
    Accepte n'importe quoi avec draw()
    Type checker vérifie statiquement
    """
    shape.draw()


# Démonstration
circle = Circle(5)
rectangle = Rectangle(10, 5)

render(circle)     # ✓ OK (a draw())
render(rectangle)  # ✓ OK (a draw())
```

### 9.2 Protocols vs ABC

```python
from typing import Protocol
from abc import ABC, abstractmethod


# ============================================================================
# APPROCHE 1 : Protocol (structural typing)
# ============================================================================

class Comparable(Protocol):
    """Protocol : pas besoin d'héritage"""
    
    def __lt__(self, other) -> bool:
        ...


class Student:
    """Compatible avec Comparable sans héritage"""
    
    def __init__(self, name: str, grade: float):
        self.name = name
        self.grade = grade
    
    def __lt__(self, other: 'Student') -> bool:
        return self.grade < other.grade


def find_min(items: list[Comparable]) -> Comparable:
    """Fonctionne avec tout ce qui a __lt__"""
    return min(items)


# ============================================================================
# APPROCHE 2 : ABC (nominal typing)
# ============================================================================

class ComparableABC(ABC):
    """ABC : DOIT hériter explicitement"""
    
    @abstractmethod
    def __lt__(self, other) -> bool:
        pass


class StudentStrict(ComparableABC):
    """DOIT hériter de ComparableABC"""
    
    def __init__(self, name: str, grade: float):
        self.name = name
        self.grade = grade
    
    def __lt__(self, other: 'StudentStrict') -> bool:
        return self.grade < other.grade


# Démonstration
students = [
    Student("Marie", 15),
    Student("Jean", 12),
    Student("Sophie", 18)
]

# Protocol : fonctionne avec Student
best = find_min(students)
print(f"Meilleur étudiant: {best.name}")

# ABC : nécessite héritage explicite
students_strict = [
    StudentStrict("Marie", 15),
    StudentStrict("Jean", 12)
]
```

### 9.3 Protocols Complexes

```python
from typing import Protocol, Iterator


class Container(Protocol):
    """Protocol pour conteneurs"""
    
    def __len__(self) -> int:
        ...
    
    def __contains__(self, item) -> bool:
        ...
    
    def __iter__(self) -> Iterator:
        ...


class CustomList:
    """Compatible avec Container sans héritage"""
    
    def __init__(self):
        self._items = []
    
    def add(self, item):
        self._items.append(item)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __contains__(self, item) -> bool:
        return item in self._items)
    
    def __iter__(self) -> Iterator:
        return iter(self._items)


def process_container(container: Container):
    """Fonctionne avec tout Container"""
    print(f"Longueur: {len(container)}")
    print(f"Contient 'test': {'test' in container}")
    for item in container:
        print(f"  - {item}")


# Utilisation
custom_list = CustomList()
custom_list.add("test")
custom_list.add("data")

process_container(custom_list)  # ✓ Compatible
```

---

## 10. Cas Pratique Complet : Système de Stockage

```python
from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict, List, Optional
import json
import pickle


# ============================================================================
# PROTOCOLS (Duck typing formel)
# ============================================================================

class Serializable(Protocol):
    """Protocol pour objets sérialisables"""
    
    def to_dict(self) -> Dict[str, Any]:
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        ...


# ============================================================================
# CLASSE ABSTRAITE (Storage)
# ============================================================================

class Storage(ABC):
    """Interface de stockage abstraite"""
    
    @abstractmethod
    def save(self, key: str, obj: Serializable) -> None:
        """Sauvegarde un objet"""
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Serializable]:
        """Charge un objet"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Supprime un objet"""
        pass
    
    @abstractmethod
    def list_keys(self) -> List[str]:
        """Liste toutes les clés"""
        pass
    
    def exists(self, key: str) -> bool:
        """Méthode concrète : vérifie l'existence"""
        return key in self.list_keys()


# ============================================================================
# ENTITÉS (Implémentent Serializable via Protocol)
# ============================================================================

class Student:
    """Étudiant - compatible Serializable"""
    
    def __init__(self, student_id: str, name: str, email: str):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'grades': self.grades
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Désérialisation"""
        student = cls(data['student_id'], data['name'], data['email'])
        student.grades = data.get('grades', [])
        return student
    
    def __str__(self):
        return f"Student({self.student_id}, {self.name})"


class Course:
    """Cours - compatible Serializable"""
    
    def __init__(self, course_id: str, name: str, credits: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'course_id': self.course_id,
            'name': self.name,
            'credits': self.credits
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Course':
        return cls(data['course_id'], data['name'], data['credits'])
    
    def __str__(self):
        return f"Course({self.course_id}, {self.name})"


# ============================================================================
# IMPLÉMENTATIONS CONCRÈTES DE STORAGE
# ============================================================================

class JSONStorage(Storage):
    """Stockage JSON"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data: Dict[str, Dict] = {}
        self._load_file()
    
    def _load_file(self):
        try:
            with open(self.filepath, 'r') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}
    
    def _save_file(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._data, f, indent=2)
    
    def save(self, key: str, obj: Serializable) -> None:
        self._data[key] = obj.to_dict()
        self._save_file()
        print(f"✓ [JSON] {key} sauvegardé")
    
    def load(self, key: str) -> Optional[Dict]:
        return self._data.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._save_file()
            return True
        return False
    
    def list_keys(self) -> List[str]:
        return list(self._data.keys())


class InMemoryStorage(Storage):
    """Stockage en mémoire"""
    
    def __init__(self):
        self._storage: Dict[str, Serializable] = {}
    
    def save(self, key: str, obj: Serializable) -> None:
        self._storage[key] = obj
        print(f"✓ [Memory] {key} sauvegardé")
    
    def load(self, key: str) -> Optional[Serializable]:
        return self._storage.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
            return True
        return False
    
    def list_keys(self) -> List[str]:
        return list(self._storage.keys())


# ============================================================================
# SERVICE UTILISANT LE POLYMORPHISME
# ============================================================================

class DataService:
    """Service de données polymorphe"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def save_student(self, student: Student):
        """Sauvegarde un étudiant"""
        key = f"student:{student.student_id}"
        self.storage.save(key, student)
    
    def save_course(self, course: Course):
        """Sauvegarde un cours"""
        key = f"course:{course.course_id}"
        self.storage.save(key, course)
    
    def get_all_students(self) -> List[Student]:
        """Récupère tous les étudiants"""
        students = []
        for key in self.storage.list_keys():
            if key.startswith("student:"):
                data = self.storage.load(key)
                if data:
                    students.append(Student.from_dict(data))
        return students
    
    def get_statistics(self) -> Dict[str, int]:
        """Statistiques"""
        keys = self.storage.list_keys()
        return {
            'total_items': len(keys),
            'students': sum(1 for k in keys if k.startswith("student:")),
            'courses': sum(1 for k in keys if k.startswith("course:"))
        }


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CAS PRATIQUE - SYSTÈME DE STOCKAGE POLYMORPHE")
    print("=" * 70)
    
    # Test avec InMemory
    print("\n--- Stockage en Mémoire ---")
    memory_storage = InMemoryStorage()
    service1 = DataService(memory_storage)
    
    service1.save_student(Student("20231001", "Marie", "marie@ua.fr"))
    service1.save_student(Student("20231002", "Jean", "jean@ua.fr"))
    service1.save_course(Course("POO", "Programmation OO", 6))
    
    print(f"\nStatistiques: {service1.get_statistics()}")
    
    # Test avec JSON (même interface!)
    print("\n--- Stockage JSON ---")
    json_storage = JSONStorage("/tmp/university_data.json")
    service2 = DataService(json_storage)
    
    service2.save_student(Student("20231003", "Sophie", "sophie@ua.fr"))
    service2.save_course(Course("WEB", "Développement Web", 6))
    
    print(f"\nStatistiques: {service2.get_statistics()}")
    
    print("\n" + "=" * 70)
    print("CONCEPTS DÉMONTRÉS:")
    print("- Storage = Classe abstraite (contrat)")
    print("- Serializable = Protocol (duck typing formel)")
    print("- JSONStorage/InMemoryStorage = Implémentations concrètes")
    print("- DataService = Polymorphisme (accepte n'importe quel Storage)")
    print("=" * 70)
```

---

## 11. Résumé et Bonnes Pratiques

### Quand utiliser quoi ?

| Situation | Solution | Exemple |
|-----------|----------|---------|
| **Interface stricte** | ABC | PaymentProcessor, Database |
| **Duck typing formel** | Protocol | Drawable, Comparable |
| **Python simple** | Duck typing | file-like objects |
| **Générique** | TypeVar + Generic | Repository[T] |

### Bonnes Pratiques

**1. Préférer les Protocols pour le duck typing**
```python
# ✅ Bon : Protocol
class Drawable(Protocol):
    def draw(self): ...

# ❌ Moins bon : forcer l'héritage
class Drawable(ABC):
    @abstractmethod
    def draw(self): pass
```

**2. Utiliser ABC pour les contrats stricts**
```python
# ✅ Bon : ABC quand l'interface est critique
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount): pass
```

**3. Méthodes concrètes dans les ABC**
```python
class Shape(ABC):
    @abstractmethod
    def area(self): pass
    
    def describe(self):  # Méthode concrète
        return f"Aire: {self.area()}"
```

---

## 12. Conclusion du CM3

### Récapitulatif Complet

**Partie 1 :**
- ✅ Polymorphisme par héritage
- ✅ Collections hétérogènes
- ✅ Surcharge d'opérateurs
- ✅ Strategy Pattern

**Partie 2 :**
- ✅ Classes abstraites (ABC)
- ✅ Duck typing
- ✅ Protocols
- ✅ Type hints avancés
- ✅ Cas pratique complet

### Concepts Maîtrisés

1. **Polymorphisme** = Même interface, comportements différents
2. **Abstraction** = Cacher les détails d'implémentation
3. **ABC** = Contrat strict avec héritage
4. **Protocol** = Duck typing formel
5. **Duck typing** = "Si ça marche comme..."

### Hiérarchie des Concepts

```
POLYMORPHISME
    ├── Par héritage (ABC)
    │   ├── Méthodes abstraites
    │   └── Méthodes concrètes
    │
    ├── Duck typing
    │   ├── Informel (Python pur)
    │   └── Formel (Protocols)
    │
    └── Surcharge d'opérateurs
        ├── __add__, __mul__, etc.
        └── Opérateurs personnalisés
```

### Prochains Cours

**✅ CM1 - Classes et Objets** (Fait)  
**✅ CM2 - Héritage et Composition** (Fait)  
**✅ CM3 - Polymorphisme et Abstraction** (Fait)  
**➡️ CM4 - Design Patterns** (Déjà créé)  
**➡️ CM5 - SOLID** (Déjà créé)  
**➡️ CM6 - Architecture** (Déjà créé)  

---

*Fin du CM3 - Polymorphisme et Abstraction*