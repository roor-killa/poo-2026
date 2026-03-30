# CM1 - Classes et Objets (Partie 1) - roor@nasdy.fr
## Programmation Orientée Objet - Fondamentaux

---

## Introduction à la Programmation Orientée Objet

### Qu'est-ce que la POO ?

> **La Programmation Orientée Objet (POO) est un paradigme de programmation basé sur le concept d'objets, qui peuvent contenir des données (attributs) et du code (méthodes).**

### Pourquoi la POO ?

**Avant la POO (Programmation Procédurale) :**
```python
# ❌ Code procédural - difficile à maintenir
student_id_1 = "20231001"
student_name_1 = "Marie Lafleur"
student_email_1 = "marie@ua.fr"
student_grades_1 = [15, 16, 14]

student_id_2 = "20231002"
student_name_2 = "Jean Martin"
student_email_2 = "jean@ua.fr"
student_grades_2 = [12, 13, 11]

def calculate_average(grades):
    return sum(grades) / len(grades)

# Pour chaque étudiant, beaucoup de variables séparées
avg_1 = calculate_average(student_grades_1)
avg_2 = calculate_average(student_grades_2)
```

**Problèmes :**
- Variables dispersées
- Pas de lien entre les données
- Difficile de passer toutes les infos d'un étudiant
- Code répétitif
- Risque d'erreurs (mélanger les données)

**Avec la POO :**
```python
# ✅ Code orienté objet - structuré et maintenable
class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
    
    def add_grade(self, grade):
        self.grades.append(grade)
    
    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

# Utilisation simple et claire
marie = Student("20231001", "Marie Lafleur", "marie@ua.fr")
marie.add_grade(15)
marie.add_grade(16)
marie.add_grade(14)

jean = Student("20231002", "Jean Martin", "jean@ua.fr")
jean.add_grade(12)
jean.add_grade(13)
jean.add_grade(11)

print(f"Moyenne de {marie.name}: {marie.calculate_average()}")
print(f"Moyenne de {jean.name}: {jean.calculate_average()}")
```

**Avantages :**
- ✅ Données et comportements regroupés
- ✅ Code réutilisable
- ✅ Plus facile à comprendre et maintenir
- ✅ Modélise le monde réel

---

## 1. Qu'est-ce qu'une Classe ?

### Définition

> **Une classe est un modèle (blueprint) qui définit la structure et le comportement des objets.**

**Analogie :** Une classe est comme un **plan architectural** pour construire des maisons.

```
┌─────────────────────────────────┐
│      CLASSE : Maison            │  ← Plan architectural
│                                 │
│  Attributs:                     │
│  - nombre_pieces                │
│  - surface                      │
│  - adresse                      │
│                                 │
│  Méthodes:                      │
│  - ouvrir_porte()               │
│  - allumer_lumiere()            │
│  - calculer_prix()              │
└─────────────────────────────────┘
         │
         ├──→ Objet 1: Maison A (12 rue X, 100m²)
         ├──→ Objet 2: Maison B (45 rue Y, 85m²)
         └──→ Objet 3: Maison C (7 rue Z, 120m²)
```

### Syntaxe de base

```python
class NomDeLaClasse:
    """Documentation de la classe (docstring)"""
    
    # Attributs de classe (partagés par toutes les instances)
    attribut_classe = "valeur"
    
    # Constructeur (méthode spéciale)
    def __init__(self, param1, param2):
        """Initialise une nouvelle instance"""
        self.attribut1 = param1  # Attribut d'instance
        self.attribut2 = param2
    
    # Méthode d'instance
    def methode(self):
        """Fait quelque chose"""
        return self.attribut1 + self.attribut2
```

### Premier exemple : Classe Student

```python
class Student:
    """
    Représente un étudiant de l'université
    """
    
    # Attribut de classe (partagé par tous les étudiants)
    university = "Université des Antilles"
    
    def __init__(self, student_id, name, email):
        """
        Constructeur : initialise un nouvel étudiant
        
        Args:
            student_id: Identifiant unique de l'étudiant
            name: Nom complet de l'étudiant
            email: Adresse email
        """
        # Attributs d'instance (propres à chaque étudiant)
        self.student_id = student_id
        self.name = name
        self.email = email
        self.grades = []
        self.enrolled_courses = []
    
    def add_grade(self, course, grade):
        """
        Ajoute une note pour un cours
        
        Args:
            course: Nom du cours
            grade: Note obtenue (0-20)
        """
        self.grades.append({'course': course, 'grade': grade})
        print(f"✓ Note de {grade}/20 ajoutée pour {course}")
    
    def calculate_average(self):
        """
        Calcule la moyenne générale
        
        Returns:
            float: Moyenne des notes
        """
        if not self.grades:
            return 0.0
        
        total = sum(item['grade'] for item in self.grades)
        return total / len(self.grades)
    
    def enroll_in_course(self, course_name):
        """
        Inscrit l'étudiant à un cours
        
        Args:
            course_name: Nom du cours
        """
        if course_name not in self.enrolled_courses:
            self.enrolled_courses.append(course_name)
            print(f"✓ Inscription au cours: {course_name}")
        else:
            print(f"⚠ Déjà inscrit au cours: {course_name}")
    
    def get_info(self):
        """
        Retourne les informations de l'étudiant
        
        Returns:
            str: Informations formatées
        """
        info = f"""
{'=' * 50}
INFORMATIONS ÉTUDIANT
{'=' * 50}
ID: {self.student_id}
Nom: {self.name}
Email: {self.email}
Université: {Student.university}
Nombre de cours: {len(self.enrolled_courses)}
Moyenne: {self.calculate_average():.2f}/20
{'=' * 50}
"""
        return info


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CM1 - CLASSES ET OBJETS - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer des objets (instances de la classe Student)
    print("\n--- Création d'étudiants ---")
    marie = Student("20231001", "Marie Lafleur", "marie.lafleur@etudiant.ua.fr")
    jean = Student("20231002", "Jean Martin", "jean.martin@etudiant.ua.fr")
    sophie = Student("20231003", "Sophie Bernard", "sophie.bernard@etudiant.ua.fr")
    
    print(f"✓ {marie.name} créé(e)")
    print(f"✓ {jean.name} créé(e)")
    print(f"✓ {sophie.name} créé(e)")
    
    # Inscrire aux cours
    print("\n--- Inscriptions aux cours ---")
    marie.enroll_in_course("Programmation Orientée Objet")
    marie.enroll_in_course("Développement Web")
    marie.enroll_in_course("Base de Données")
    
    jean.enroll_in_course("Programmation Orientée Objet")
    jean.enroll_in_course("Algorithmes")
    
    # Ajouter des notes
    print("\n--- Attribution des notes ---")
    marie.add_grade("POO", 16)
    marie.add_grade("Web", 15)
    marie.add_grade("BD", 17)
    
    jean.add_grade("POO", 14)
    jean.add_grade("Algo", 13)
    
    # Afficher les informations
    print("\n--- Informations des étudiants ---")
    print(marie.get_info())
    print(jean.get_info())
    
    # Démonstration : attribut de classe
    print("\n--- Attribut de classe ---")
    print(f"Université de Marie: {marie.university}")
    print(f"Université de Jean: {jean.university}")
    print(f"Université (classe): {Student.university}")
    
    # Modifier l'attribut de classe
    Student.university = "UA - Campus de Schoelcher"
    print(f"\nAprès modification:")
    print(f"Université de Marie: {marie.university}")
    print(f"Université de Jean: {jean.university}")
```

**Sortie :**
```
======================================================================
CM1 - CLASSES ET OBJETS - DÉMONSTRATION
======================================================================

--- Création d'étudiants ---
✓ Marie Lafleur créé(e)
✓ Jean Martin créé(e)
✓ Sophie Bernard créé(e)

--- Inscriptions aux cours ---
✓ Inscription au cours: Programmation Orientée Objet
✓ Inscription au cours: Développement Web
✓ Inscription au cours: Base de Données
✓ Inscription au cours: Programmation Orientée Objet
✓ Inscription au cours: Algorithmes

--- Attribution des notes ---
✓ Note de 16/20 ajoutée pour POO
✓ Note de 15/20 ajoutée pour Web
✓ Note de 17/20 ajoutée pour BD
✓ Note de 14/20 ajoutée pour POO
✓ Note de 13/20 ajoutée pour Algo

--- Informations des étudiants ---

==================================================
INFORMATIONS ÉTUDIANT
==================================================
ID: 20231001
Nom: Marie Lafleur
Email: marie.lafleur@etudiant.ua.fr
Université: Université des Antilles
Nombre de cours: 3
Moyenne: 16.00/20
==================================================
```

---

## 2. Anatomie d'une Classe

### 2.1 Le mot-clé `self`

> **`self` représente l'instance courante de la classe.**

```python
class Student:
    def __init__(self, name):
        self.name = name  # self.name = attribut de l'instance
    
    def greet(self):
        # self permet d'accéder aux attributs de l'instance
        print(f"Bonjour, je suis {self.name}")

# Quand on appelle une méthode
marie = Student("Marie")
marie.greet()  # Python transforme en: Student.greet(marie)
               # self devient automatiquement marie
```

**Pourquoi `self` ?**
- Accéder aux attributs de l'instance
- Appeler d'autres méthodes de l'instance
- Distinguer variables locales et attributs

### 2.2 Le constructeur `__init__`

> **`__init__` est une méthode spéciale appelée automatiquement lors de la création d'un objet.**

```python
class Course:
    def __init__(self, code, name, credits):
        """
        Constructeur : initialise les attributs
        Appelé automatiquement lors de Course(...)
        """
        print(f"[Constructeur] Création du cours {name}")
        self.code = code
        self.name = name
        self.credits = credits
        self.students = []
    
    def __str__(self):
        """
        Méthode spéciale pour l'affichage (print)
        """
        return f"{self.code} - {self.name} ({self.credits} crédits)"

# Utilisation
poo = Course("INF201", "Programmation Orientée Objet", 6)
# [Constructeur] Création du cours Programmation Orientée Objet

print(poo)  # Appelle __str__()
# INF201 - Programmation Orientée Objet (6 crédits)
```

### 2.3 Attributs d'instance vs Attributs de classe

```python
class Student:
    # Attribut de CLASSE (partagé par toutes les instances)
    university = "Université des Antilles"
    student_count = 0  # Compteur global
    
    def __init__(self, name):
        # Attributs d'INSTANCE (propres à chaque objet)
        self.name = name
        self.student_id = Student.student_count + 1
        
        # Incrémenter le compteur de classe
        Student.student_count += 1

# Démonstration
marie = Student("Marie")
jean = Student("Jean")
sophie = Student("Sophie")

print(f"Nombre total d'étudiants: {Student.student_count}")  # 3

# Chaque instance a son propre student_id
print(f"ID de Marie: {marie.student_id}")  # 1
print(f"ID de Jean: {jean.student_id}")    # 2
print(f"ID de Sophie: {sophie.student_id}") # 3

# Mais tous partagent le même university
print(f"Université de Marie: {marie.university}")  # UA
print(f"Université de Jean: {jean.university}")    # UA
```

**Différences importantes :**

| Attribut de Classe | Attribut d'Instance |
|-------------------|---------------------|
| Défini dans la classe | Défini dans `__init__` |
| Partagé par toutes les instances | Propre à chaque instance |
| Accès via `ClassName.attr` | Accès via `self.attr` |
| Exemple : constantes, compteurs | Exemple : nom, email, notes |

### 2.4 Méthodes

```python
class BankAccount:
    """Compte bancaire"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
    
    # Méthode d'instance (utilise self)
    def deposit(self, amount):
        """Déposer de l'argent"""
        if amount <= 0:
            print("⚠ Montant invalide")
            return False
        
        self.balance += amount
        self.transactions.append(f"Dépôt: +{amount}€")
        print(f"✓ Dépôt de {amount}€. Nouveau solde: {self.balance}€")
        return True
    
    def withdraw(self, amount):
        """Retirer de l'argent"""
        if amount <= 0:
            print("⚠ Montant invalide")
            return False
        
        if amount > self.balance:
            print(f"✗ Solde insuffisant (disponible: {self.balance}€)")
            return False
        
        self.balance -= amount
        self.transactions.append(f"Retrait: -{amount}€")
        print(f"✓ Retrait de {amount}€. Nouveau solde: {self.balance}€")
        return True
    
    def get_statement(self):
        """Afficher le relevé"""
        print(f"\n{'=' * 50}")
        print(f"RELEVÉ DE COMPTE - {self.owner}")
        print(f"{'=' * 50}")
        print(f"Solde actuel: {self.balance}€")
        print(f"\nDernières transactions:")
        for transaction in self.transactions[-5:]:
            print(f"  - {transaction}")
        print(f"{'=' * 50}\n")

# Utilisation
account = BankAccount("Marie Lafleur", 1000)
account.deposit(500)
account.withdraw(200)
account.deposit(100)
account.withdraw(50)
account.get_statement()
```

---

## 3. Méthodes Spéciales (Magic Methods)

### Introduction

Python offre des **méthodes spéciales** (aussi appelées "dunder methods" pour **d**ouble **under**score) qui permettent de définir le comportement des objets avec les opérateurs Python.

### 3.1 Méthodes de Représentation

```python
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
    
    def __str__(self):
        """
        Représentation "lisible" pour print()
        Destinée à l'utilisateur final
        """
        return f"Étudiant: {self.name} (ID: {self.student_id})"
    
    def __repr__(self):
        """
        Représentation "technique" pour le débogage
        Devrait idéalement permettre de recréer l'objet
        """
        return f"Student('{self.student_id}', '{self.name}')"

# Démonstration
marie = Student("20231001", "Marie Lafleur")

print(marie)        # Appelle __str__()
# Étudiant: Marie Lafleur (ID: 20231001)

print(repr(marie))  # Appelle __repr__()
# Student('20231001', 'Marie Lafleur')

# Dans une liste, c'est __repr__() qui est utilisé
students = [marie]
print(students)
# [Student('20231001', 'Marie Lafleur')]
```

### 3.2 Méthodes de Comparaison

```python
class Student:
    def __init__(self, name, average):
        self.name = name
        self.average = average
    
    def __eq__(self, other):
        """Égalité (==)"""
        if not isinstance(other, Student):
            return False
        return self.average == other.average
    
    def __lt__(self, other):
        """Inférieur à (<)"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.average < other.average
    
    def __le__(self, other):
        """Inférieur ou égal (<=)"""
        return self == other or self < other
    
    def __gt__(self, other):
        """Supérieur à (>)"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.average > other.average
    
    def __ge__(self, other):
        """Supérieur ou égal (>=)"""
        return self == other or self > other
    
    def __str__(self):
        return f"{self.name} (moyenne: {self.average})"

# Démonstration
marie = Student("Marie", 15.5)
jean = Student("Jean", 12.0)
sophie = Student("Sophie", 15.5)

print(f"Marie > Jean ? {marie > jean}")        # True
print(f"Marie == Sophie ? {marie == sophie}")  # True
print(f"Jean < Marie ? {jean < marie}")        # True

# Trier des étudiants
students = [marie, jean, sophie]
students_sorted = sorted(students)  # Utilise __lt__()

print("\nÉtudiants triés par moyenne:")
for student in students_sorted:
    print(f"  {student}")
```

### 3.3 Méthodes de Conteneur

```python
class Classroom:
    """Classe qui se comporte comme un conteneur"""
    
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.students = []
    
    def __len__(self):
        """Longueur (len())"""
        return len(self.students)
    
    def __getitem__(self, index):
        """Accès par index (classroom[0])"""
        return self.students[index]
    
    def __setitem__(self, index, value):
        """Modification par index (classroom[0] = ...)"""
        self.students[index] = value
    
    def __contains__(self, student):
        """Test d'appartenance (student in classroom)"""
        return student in self.students
    
    def __iter__(self):
        """Rend l'objet itérable (for student in classroom)"""
        return iter(self.students)
    
    def add_student(self, student):
        """Ajoute un étudiant"""
        if len(self) >= self.capacity:
            print(f"✗ Salle {self.name} pleine (capacité: {self.capacity})")
            return False
        
        self.students.append(student)
        print(f"✓ {student} ajouté à {self.name}")
        return True

# Démonstration
classroom = Classroom("Salle A101", 3)

classroom.add_student("Marie")
classroom.add_student("Jean")
classroom.add_student("Sophie")

# Utiliser len()
print(f"\nNombre d'étudiants: {len(classroom)}")  # 3

# Utiliser l'indexation
print(f"Premier étudiant: {classroom[0]}")  # Marie

# Utiliser in
print(f"Marie dans la salle ? {'Marie' in classroom}")  # True

# Itérer
print("\nListe des étudiants:")
for student in classroom:  # Utilise __iter__()
    print(f"  - {student}")
```

### 3.4 Méthodes Arithmétiques

```python
class Grade:
    """Représente une note"""
    
    def __init__(self, value, coefficient=1):
        if not 0 <= value <= 20:
            raise ValueError("Note doit être entre 0 et 20")
        self.value = value
        self.coefficient = coefficient
    
    def __add__(self, other):
        """Addition (+)"""
        if isinstance(other, Grade):
            # Moyenne pondérée
            total = (self.value * self.coefficient + 
                    other.value * other.coefficient)
            total_coef = self.coefficient + other.coefficient
            return Grade(total / total_coef, total_coef)
        return NotImplemented
    
    def __mul__(self, coefficient):
        """Multiplication (*)"""
        return Grade(self.value, self.coefficient * coefficient)
    
    def __str__(self):
        return f"{self.value:.2f}/20 (coef: {self.coefficient})"

# Démonstration
grade1 = Grade(15, coefficient=1)
grade2 = Grade(12, coefficient=2)

print(f"Note 1: {grade1}")
print(f"Note 2: {grade2}")

# Addition (moyenne pondérée)
average = grade1 + grade2
print(f"Moyenne: {average}")

# Multiplication
grade3 = grade1 * 3
print(f"Note avec coef 3: {grade3}")
```

---

## 4. Encapsulation et Propriétés

### 4.1 Convention de nommage en Python

Python utilise une **convention** pour indiquer la visibilité :

```python
class Student:
    def __init__(self, name):
        self.public_attr = "public"      # Public
        self._protected_attr = "protected"  # Protégé (convention)
        self.__private_attr = "private"     # Privé (name mangling)
```

**Conventions :**
- `public` : Accessible partout
- `_protected` : Usage interne (mais toujours accessible)
- `__private` : Name mangling (difficile d'accès)

### 4.2 Propriétés (@property)

Les propriétés permettent d'avoir des "getters" et "setters" élégants.

```python
class Student:
    """Étudiant avec validation"""
    
    def __init__(self, name, email):
        self._name = name
        self._email = email
        self._grades = []
    
    # Getter pour name
    @property
    def name(self):
        """Récupère le nom"""
        return self._name
    
    # Setter pour name
    @name.setter
    def name(self, value):
        """Modifie le nom avec validation"""
        if not value or len(value) < 2:
            raise ValueError("Nom invalide")
        self._name = value.strip().title()
    
    # Getter pour email
    @property
    def email(self):
        """Récupère l'email"""
        return self._email
    
    # Setter pour email
    @email.setter
    def email(self, value):
        """Modifie l'email avec validation"""
        if '@' not in value:
            raise ValueError("Email invalide")
        self._email = value.lower()
    
    # Propriété calculée (lecture seule)
    @property
    def average(self):
        """Calcule la moyenne (lecture seule)"""
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)
    
    def add_grade(self, grade):
        """Ajoute une note"""
        if 0 <= grade <= 20:
            self._grades.append(grade)
        else:
            raise ValueError("Note doit être entre 0 et 20")

# Démonstration
marie = Student("marie lafleur", "MARIE@UA.FR")

# Utilisation comme attributs simples (mais avec validation)
print(f"Nom: {marie.name}")      # marie lafleur → Marie Lafleur
print(f"Email: {marie.email}")    # MARIE@UA.FR → marie@ua.fr

# Modification avec validation
marie.name = "marie-claire lafleur"
print(f"Nouveau nom: {marie.name}")  # Marie-Claire Lafleur

# Propriété calculée (lecture seule)
marie.add_grade(15)
marie.add_grade(16)
marie.add_grade(14)
print(f"Moyenne: {marie.average}")  # 15.0

# Erreur : average est en lecture seule
# marie.average = 18  # ✗ AttributeError
```

---

## 5. Exemple Complet : Système de Gestion de Cours

```python
from datetime import datetime
from typing import List


class Student:
    """Représente un étudiant"""
    
    student_count = 0
    
    def __init__(self, student_id: str, name: str, email: str):
        self.student_id = student_id
        self._name = name
        self._email = email
        self.enrolled_courses: List['Course'] = []
        self.grades = {}
        
        Student.student_count += 1
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if len(value) < 2:
            raise ValueError("Nom trop court")
        self._name = value.strip().title()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if '@' not in value:
            raise ValueError("Email invalide")
        self._email = value.lower()
    
    def enroll(self, course: 'Course'):
        """Inscrit l'étudiant au cours"""
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            course.add_student(self)
    
    def add_grade(self, course: 'Course', grade: float):
        """Ajoute une note pour un cours"""
        if not 0 <= grade <= 20:
            raise ValueError("Note invalide")
        self.grades[course.code] = grade
    
    def get_average(self):
        """Calcule la moyenne générale"""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
    def __repr__(self):
        return f"Student('{self.student_id}', '{self.name}', '{self.email}')"


class Course:
    """Représente un cours"""
    
    def __init__(self, code: str, name: str, credits: int, max_students: int = 30):
        self.code = code
        self.name = name
        self.credits = credits
        self.max_students = max_students
        self.students: List[Student] = []
        self.instructor = None
    
    def add_student(self, student: Student):
        """Ajoute un étudiant au cours"""
        if len(self.students) >= self.max_students:
            raise ValueError(f"Cours {self.name} complet")
        
        if student not in self.students:
            self.students.append(student)
    
    def is_full(self):
        """Vérifie si le cours est complet"""
        return len(self.students) >= self.max_students
    
    def get_enrollment_rate(self):
        """Taux de remplissage"""
        return (len(self.students) / self.max_students) * 100
    
    def __len__(self):
        return len(self.students)
    
    def __contains__(self, student):
        return student in self.students
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits} crédits)"
    
    def __repr__(self):
        return f"Course('{self.code}', '{self.name}', {self.credits})"


class Instructor:
    """Représente un enseignant"""
    
    def __init__(self, instructor_id: str, name: str, department: str):
        self.instructor_id = instructor_id
        self.name = name
        self.department = department
        self.courses: List[Course] = []
    
    def assign_course(self, course: Course):
        """Assigne un cours à l'enseignant"""
        if course not in self.courses:
            self.courses.append(course)
            course.instructor = self
    
    def get_total_students(self):
        """Nombre total d'étudiants"""
        return sum(len(course) for course in self.courses)
    
    def __str__(self):
        return f"Prof. {self.name} ({self.department})"


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE GESTION DE COURS - DÉMONSTRATION COMPLÈTE")
    print("=" * 70)
    
    # Créer un enseignant
    print("\n--- Création d'un enseignant ---")
    prof = Instructor("PROF001", "Roor", "Informatique")
    print(f"✓ {prof} créé")
    
    # Créer des cours
    print("\n--- Création de cours ---")
    poo = Course("INF201", "Programmation Orientée Objet", 6, max_students=30)
    web = Course("INF202", "Développement Web", 6, max_students=25)
    bd = Course("INF203", "Bases de Données", 6, max_students=30)
    
    print(f"✓ {poo}")
    print(f"✓ {web}")
    print(f"✓ {bd}")
    
    # Assigner les cours à l'enseignant
    print("\n--- Assignation des cours ---")
    prof.assign_course(poo)
    prof.assign_course(web)
    prof.assign_course(bd)
    print(f"✓ {len(prof.courses)} cours assignés à {prof.name}")
    
    # Créer des étudiants
    print("\n--- Inscription d'étudiants ---")
    marie = Student("20231001", "Marie Lafleur", "marie@ua.fr")
    jean = Student("20231002", "Jean Martin", "jean@ua.fr")
    sophie = Student("20231003", "Sophie Bernard", "sophie@ua.fr")
    
    # Inscrire aux cours
    marie.enroll(poo)
    marie.enroll(web)
    marie.enroll(bd)
    
    jean.enroll(poo)
    jean.enroll(bd)
    
    sophie.enroll(poo)
    sophie.enroll(web)
    
    print(f"✓ {len(poo)} étudiants inscrits à {poo.name}")
    print(f"✓ {len(web)} étudiants inscrits à {web.name}")
    print(f"✓ {len(bd)} étudiants inscrits à {bd.name}")
    
    # Ajouter des notes
    print("\n--- Attribution des notes ---")
    marie.add_grade(poo, 16)
    marie.add_grade(web, 15)
    marie.add_grade(bd, 17)
    
    jean.add_grade(poo, 14)
    jean.add_grade(bd, 13)
    
    sophie.add_grade(poo, 18)
    sophie.add_grade(web, 16)
    
    # Afficher les statistiques
    print("\n--- Statistiques ---")
    print(f"\nTotal d'étudiants créés: {Student.student_count}")
    print(f"Total d'étudiants de {prof.name}: {prof.get_total_students()}")
    
    print(f"\nTaux de remplissage:")
    for course in prof.courses:
        rate = course.get_enrollment_rate()
        print(f"  {course.code}: {rate:.1f}% ({len(course)}/{course.max_students})")
    
    print(f"\nMoyennes:")
    for student in [marie, jean, sophie]:
        avg = student.get_average()
        print(f"  {student.name}: {avg:.2f}/20")
    
    # Test d'appartenance
    print(f"\n--- Tests ---")
    print(f"Marie dans POO ? {marie in poo}")
    print(f"Jean dans Web ? {jean in web}")
    
    print("\n" + "=" * 70)
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **Introduction à la POO** : Pourquoi et comment  
✅ **Classes et Objets** : Définition et syntaxe  
✅ **Attributs** : de classe vs d'instance  
✅ **Méthodes** : `self`, `__init__`, méthodes d'instance  
✅ **Méthodes spéciales** : `__str__`, `__repr__`, `__eq__`, etc.  
✅ **Encapsulation** : Propriétés et validation  
✅ **Exemple complet** : Système de gestion de cours  

### Concepts clés

- **Classe** = Modèle/Plan
- **Objet** = Instance d'une classe
- **`self`** = Référence à l'instance courante
- **`__init__`** = Constructeur
- **Méthodes spéciales** = Comportement avec opérateurs Python

### Dans la Partie 2, nous verrons :

- Méthodes de classe et méthodes statiques
- Composition vs Agrégation
- Relations entre objets
- Patterns de conception orientés objet
- Exercices avancés

---