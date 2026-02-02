# CM2 - Héritage, Composition et MRO (Partie 1)
## Programmation Orientée Objet

---

## Introduction

### Rappel du CM1

**Ce que nous avons vu :**
- ✅ Classes et objets
- ✅ Attributs et méthodes  
- ✅ Méthodes spéciales
- ✅ Encapsulation et propriétés
- ✅ Méthodes de classe et statiques
- ✅ Relations entre objets (Association, Agrégation, Composition)

**Aujourd'hui - CM2 :**
- **Héritage simple** : Créer des classes dérivées
- **Surcharge de méthodes** : Redéfinir le comportement
- **super()** : Appeler la classe parente
- **Composition vs Héritage** : Quand utiliser quoi ?
- **Héritage multiple** : Plusieurs parents
- **MRO** : Ordre de résolution des méthodes

---

## 1. Qu'est-ce que l'Héritage ?

### Définition

> **L'héritage permet à une classe (classe dérivée/enfant) de récupérer les attributs et méthodes d'une autre classe (classe de base/parent).**

**Principe fondamental :** **"est un"** (is-a relationship)

```
Un Chat EST UN Animal
Une Voiture EST UN Véhicule
Un Étudiant EST UNE Personne
```

### Analogie : Arbre Généalogique

```
           Person (classe de base)
             /    \
            /      \
      Student    Teacher (classes dérivées)
        /  \
       /    \
 Bachelor  Master (sous-classes)
```

### Syntaxe de base

```python
class ClasseDeBase:
    """Classe parente"""
    def methode_parente(self):
        return "Méthode du parent"

class ClasseDerivee(ClasseDeBase):
    """Classe enfant qui hérite de ClasseDeBase"""
    def methode_enfant(self):
        return "Méthode de l'enfant"

# Utilisation
obj = ClasseDerivee()
obj.methode_parente()  # Héritée du parent
obj.methode_enfant()   # Propre à l'enfant
```

---

## 2. Héritage Simple

### 2.1 Premier Exemple

```python
class Person:
    """Classe de base : Personne"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def get_info(self):
        """Retourne les informations"""
        return f"Nom: {self.name}, Email: {self.email}"
    
    def send_email(self, message):
        """Envoie un email"""
        print(f"📧 Email envoyé à {self.email}: {message}")


class Student(Person):
    """Classe dérivée : Étudiant hérite de Personne"""
    
    def __init__(self, name, email, student_id):
        # Appeler le constructeur du parent
        super().__init__(name, email)
        # Ajouter des attributs spécifiques
        self.student_id = student_id
        self.grades = []
    
    def add_grade(self, grade):
        """Méthode spécifique aux étudiants"""
        self.grades.append(grade)
    
    def calculate_average(self):
        """Méthode spécifique aux étudiants"""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


class Teacher(Person):
    """Classe dérivée : Enseignant hérite de Personne"""
    
    def __init__(self, name, email, department):
        super().__init__(name, email)
        self.department = department
        self.courses = []
    
    def assign_course(self, course_name):
        """Méthode spécifique aux enseignants"""
        self.courses.append(course_name)
        print(f"✓ Cours '{course_name}' assigné à {self.name}")


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CM2 - HÉRITAGE SIMPLE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer un étudiant
    print("\n--- Étudiant ---")
    marie = Student("Marie Lafleur", "marie@ua.fr", "20231001")
    
    # Méthodes héritées de Person
    print(marie.get_info())  # Hérité
    marie.send_email("Bienvenue à l'université!")  # Hérité
    
    # Méthodes propres à Student
    marie.add_grade(15)
    marie.add_grade(16)
    marie.add_grade(14)
    print(f"Moyenne: {marie.calculate_average():.2f}")
    
    # Créer un enseignant
    print("\n--- Enseignant ---")
    prof = Teacher("Prof. Roor", "roor@ua.fr", "Informatique")
    
    # Méthodes héritées de Person
    print(prof.get_info())  # Hérité
    
    # Méthodes propres à Teacher
    prof.assign_course("Programmation Orientée Objet")
    prof.assign_course("Développement Web")
    
    # Vérifier l'héritage
    print("\n--- Vérification de l'héritage ---")
    print(f"marie est une instance de Student ? {isinstance(marie, Student)}")
    print(f"marie est une instance de Person ? {isinstance(marie, Person)}")
    print(f"prof est une instance de Teacher ? {isinstance(prof, Teacher)}")
    print(f"prof est une instance de Person ? {isinstance(prof, Person)}")
    print(f"marie est une instance de Teacher ? {isinstance(marie, Teacher)}")
```

**Sortie :**
```
======================================================================
CM2 - HÉRITAGE SIMPLE - DÉMONSTRATION
======================================================================

--- Étudiant ---
Nom: Marie Lafleur, Email: marie@ua.fr
📧 Email envoyé à marie@ua.fr: Bienvenue à l'université!
Moyenne: 15.00

--- Enseignant ---
Nom: Prof. Roor, Email: roor@ua.fr
✓ Cours 'Programmation Orientée Objet' assigné à Prof. Roor
✓ Cours 'Développement Web' assigné à Prof. Roor

--- Vérification de l'héritage ---
marie est une instance de Student ? True
marie est une instance de Person ? True
prof est une instance de Teacher ? True
prof est une instance de Person ? True
marie est une instance de Teacher ? False
```

### 2.2 Le mot-clé `super()`

> **`super()` permet d'appeler les méthodes de la classe parente.**

**Pourquoi utiliser `super()` ?**
- Évite de dupliquer du code
- Facilite la maintenance
- Essentiel pour l'héritage multiple (voir plus loin)

```python
class Vehicle:
    """Véhicule de base"""
    
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        print(f"[Vehicle.__init__] Création d'un véhicule {brand} {model}")
    
    def start(self):
        print(f"🔑 {self.brand} {self.model} démarre")
    
    def stop(self):
        print(f"🛑 {self.brand} {self.model} s'arrête")


class Car(Vehicle):
    """Voiture"""
    
    def __init__(self, brand, model, year, num_doors):
        # Appeler le constructeur du parent
        super().__init__(brand, model, year)
        # Ajouter des attributs spécifiques
        self.num_doors = num_doors
        print(f"[Car.__init__] Voiture avec {num_doors} portes")
    
    def open_trunk(self):
        print(f"🚗 Coffre de la {self.brand} ouvert")


class Motorcycle(Vehicle):
    """Moto"""
    
    def __init__(self, brand, model, year, engine_size):
        super().__init__(brand, model, year)
        self.engine_size = engine_size
        print(f"[Motorcycle.__init__] Moto avec moteur {engine_size}cc")
    
    def wheelie(self):
        print(f"🏍️  {self.brand} fait une roue arrière!")


# Démonstration
print("\n--- Création d'une voiture ---")
car = Car("Toyota", "Corolla", 2023, 4)
car.start()  # Méthode héritée
car.open_trunk()  # Méthode propre

print("\n--- Création d'une moto ---")
moto = Motorcycle("Yamaha", "R1", 2023, 1000)
moto.start()  # Méthode héritée
moto.wheelie()  # Méthode propre
```

**Sortie :**
```
--- Création d'une voiture ---
[Vehicle.__init__] Création d'un véhicule Toyota Corolla
[Car.__init__] Voiture avec 4 portes
🔑 Toyota Corolla démarre
🚗 Coffre de la Toyota ouvert

--- Création d'une moto ---
[Vehicle.__init__] Création d'un véhicule Yamaha R1
[Motorcycle.__init__] Moto avec moteur 1000cc
🔑 Yamaha R1 démarre
🏍️  Yamaha fait une roue arrière!
```

---

## 3. Surcharge de Méthodes (Method Overriding)

### Définition

> **La surcharge permet à une classe dérivée de redéfinir une méthode de la classe parente.**

```python
class Animal:
    """Animal de base"""
    
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        """Méthode à surcharger"""
        return "Un son quelconque"
    
    def eat(self):
        return f"{self.name} mange"


class Dog(Animal):
    """Chien"""
    
    def make_sound(self):
        """Surcharge de make_sound"""
        return "Woof! Woof!"
    
    def fetch(self):
        """Méthode spécifique"""
        return f"{self.name} rapporte la balle"


class Cat(Animal):
    """Chat"""
    
    def make_sound(self):
        """Surcharge de make_sound"""
        return "Miaou!"
    
    def climb(self):
        """Méthode spécifique"""
        return f"{self.name} grimpe à l'arbre"


class Cow(Animal):
    """Vache"""
    
    def make_sound(self):
        """Surcharge de make_sound"""
        return "Meuuuh!"


# Démonstration
animals = [
    Dog("Rex"),
    Cat("Minou"),
    Cow("Marguerite")
]

print("\n--- Polymorphisme via surcharge ---")
for animal in animals:
    # Même méthode, comportements différents
    print(f"{animal.name}: {animal.make_sound()}")
    print(f"{animal.eat()}")
    print()
```

### Surcharge avec appel au parent

```python
class BankAccount:
    """Compte bancaire de base"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        """Déposer de l'argent"""
        self.balance += amount
        print(f"✓ Dépôt de {amount}€. Solde: {self.balance}€")
    
    def withdraw(self, amount):
        """Retirer de l'argent"""
        if amount > self.balance:
            print(f"✗ Solde insuffisant")
            return False
        self.balance -= amount
        print(f"✓ Retrait de {amount}€. Solde: {self.balance}€")
        return True


class SavingsAccount(BankAccount):
    """Compte épargne avec intérêts"""
    
    def __init__(self, owner, balance=0, interest_rate=0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """Ajoute les intérêts"""
        interest = self.balance * self.interest_rate
        # Appeler la méthode deposit du parent
        super().deposit(interest)
        print(f"  (Intérêts: {interest:.2f}€ à {self.interest_rate*100}%)")


class CheckingAccount(BankAccount):
    """Compte courant avec frais de retrait"""
    
    WITHDRAWAL_FEE = 2.0
    
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)
    
    def withdraw(self, amount):
        """Retrait avec frais"""
        # Appeler la méthode du parent avec frais
        total = amount + self.WITHDRAWAL_FEE
        print(f"[Frais de retrait: {self.WITHDRAWAL_FEE}€]")
        return super().withdraw(total)


# Démonstration
print("\n--- Compte Épargne ---")
savings = SavingsAccount("Marie", 1000, interest_rate=0.03)
savings.add_interest()

print("\n--- Compte Courant ---")
checking = CheckingAccount("Jean", 500)
checking.withdraw(100)
```

---

## 4. Hiérarchies Complexes

### Exemple : Système Universitaire

```python
from datetime import datetime
from typing import List


class Person:
    """Classe de base : Personne"""
    
    person_count = 0
    
    def __init__(self, person_id: str, name: str, email: str, birth_year: int):
        self.person_id = person_id
        self.name = name
        self.email = email
        self.birth_year = birth_year
        
        Person.person_count += 1
    
    def get_age(self):
        """Calcule l'âge"""
        return datetime.now().year - self.birth_year
    
    def get_info(self):
        """Informations de base"""
        return f"{self.name} ({self.get_age()} ans)"
    
    def __str__(self):
        return f"{self.name}"


class Student(Person):
    """Étudiant"""
    
    def __init__(self, person_id: str, name: str, email: str, 
                 birth_year: int, student_id: str, level: str):
        super().__init__(person_id, name, email, birth_year)
        self.student_id = student_id
        self.level = level  # "Licence", "Master", "Doctorat"
        self.grades = []
        self.enrolled_courses = []
    
    def enroll(self, course_name):
        """Inscription à un cours"""
        if course_name not in self.enrolled_courses:
            self.enrolled_courses.append(course_name)
            print(f"✓ {self.name} inscrit à {course_name}")
    
    def add_grade(self, course, grade):
        """Ajoute une note"""
        self.grades.append({'course': course, 'grade': grade})
    
    def calculate_average(self):
        """Calcule la moyenne"""
        if not self.grades:
            return 0.0
        return sum(g['grade'] for g in self.grades) / len(self.grades)
    
    def get_info(self):
        """Surcharge : informations étudiant"""
        base_info = super().get_info()
        return f"{base_info} - {self.level} (ID: {self.student_id})"


class BachelorStudent(Student):
    """Étudiant en Licence"""
    
    def __init__(self, person_id: str, name: str, email: str, 
                 birth_year: int, student_id: str, year: int):
        super().__init__(person_id, name, email, birth_year, 
                        student_id, "Licence")
        self.year = year  # L1, L2, L3
    
    def can_graduate(self):
        """Peut obtenir son diplôme ?"""
        return self.year == 3 and self.calculate_average() >= 10
    
    def get_info(self):
        """Surcharge : ajoute l'année"""
        base_info = super().get_info()
        return f"{base_info} - L{self.year}"


class MasterStudent(Student):
    """Étudiant en Master"""
    
    def __init__(self, person_id: str, name: str, email: str, 
                 birth_year: int, student_id: str, year: int, thesis_topic: str = None):
        super().__init__(person_id, name, email, birth_year, 
                        student_id, "Master")
        self.year = year  # M1, M2
        self.thesis_topic = thesis_topic
    
    def set_thesis_topic(self, topic):
        """Définit le sujet de mémoire"""
        self.thesis_topic = topic
        print(f"✓ Sujet de mémoire: {topic}")
    
    def get_info(self):
        """Surcharge : ajoute l'année et le sujet"""
        base_info = super().get_info()
        info = f"{base_info} - M{self.year}"
        if self.thesis_topic:
            info += f" - Mémoire: {self.thesis_topic}"
        return info


class Teacher(Person):
    """Enseignant"""
    
    def __init__(self, person_id: str, name: str, email: str, 
                 birth_year: int, teacher_id: str, department: str):
        super().__init__(person_id, name, email, birth_year)
        self.teacher_id = teacher_id
        self.department = department
        self.courses = []
    
    def assign_course(self, course_name):
        """Assigne un cours"""
        if course_name not in self.courses:
            self.courses.append(course_name)
            print(f"✓ Cours '{course_name}' assigné à {self.name}")
    
    def get_info(self):
        """Surcharge : informations enseignant"""
        base_info = super().get_info()
        return f"Prof. {base_info} - Département {self.department}"


class Professor(Teacher):
    """Professeur (enseignant avec rang supérieur)"""
    
    def __init__(self, person_id: str, name: str, email: str, 
                 birth_year: int, teacher_id: str, department: str, rank: str):
        super().__init__(person_id, name, email, birth_year, 
                        teacher_id, department)
        self.rank = rank  # "Maître de Conférences", "Professeur"
        self.publications = []
    
    def add_publication(self, title, year):
        """Ajoute une publication"""
        self.publications.append({'title': title, 'year': year})
        print(f"✓ Publication ajoutée: {title}")
    
    def get_info(self):
        """Surcharge : ajoute le rang"""
        base_info = super().get_info()
        return f"{base_info} - {self.rank}"


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("HIÉRARCHIE UNIVERSITAIRE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer différents types de personnes
    print("\n--- Création de personnes ---")
    
    marie = BachelorStudent("P001", "Marie Lafleur", "marie@ua.fr", 
                           2003, "L20231001", year=2)
    jean = MasterStudent("P002", "Jean Martin", "jean@ua.fr", 
                        2001, "M20231002", year=2)
    prof_roor = Professor("P003", "Roor", "roor@ua.fr", 
                         1985, "T001", "Informatique", 
                         "Maître de Conférences")
    
    # Afficher les informations
    print("\n--- Informations ---")
    print(f"Marie: {marie.get_info()}")
    print(f"Jean: {jean.get_info()}")
    print(f"Prof: {prof_roor.get_info()}")
    
    # Actions spécifiques
    print("\n--- Actions ---")
    marie.enroll("POO")
    marie.enroll("Développement Web")
    marie.add_grade("POO", 15)
    marie.add_grade("Web", 16)
    
    jean.set_thesis_topic("Architecture Microservices en Python")
    
    prof_roor.assign_course("Programmation Orientée Objet")
    prof_roor.add_publication("Design Patterns in Python", 2023)
    
    # Vérifier les hiérarchies
    print("\n--- Hiérarchie d'héritage ---")
    print(f"Marie est Student ? {isinstance(marie, Student)}")
    print(f"Marie est Person ? {isinstance(marie, Person)}")
    print(f"Marie est BachelorStudent ? {isinstance(marie, BachelorStudent)}")
    print(f"Marie est Teacher ? {isinstance(marie, Teacher)}")
    
    print(f"\nProf est Teacher ? {isinstance(prof_roor, Teacher)}")
    print(f"Prof est Professor ? {isinstance(prof_roor, Professor)}")
    print(f"Prof est Person ? {isinstance(prof_roor, Person)}")
    
    # Polymorphisme
    print("\n--- Polymorphisme ---")
    people = [marie, jean, prof_roor]
    for person in people:
        # Même méthode get_info(), résultats différents
        print(f"  {person.get_info()}")
```

---

## 5. Composition vs Héritage

### Le Dilemme

**Quand utiliser l'héritage ?**
- Relation "**est un**" (is-a)
- Partage de comportements communs
- Hiérarchie logique

**Quand utiliser la composition ?**
- Relation "**a un**" (has-a)
- Flexibilité et réutilisation
- Éviter les hiérarchies profondes

### Exemple : Mauvais usage de l'héritage

```python
# ❌ MAUVAIS : Héritage inapproprié
class Stack(list):
    """
    Problème : Stack hérite de list, mais on veut limiter les opérations
    Un Stack N'EST PAS une liste complète
    """
    def push(self, item):
        self.append(item)
    
    def peek(self):
        return self[-1] if self else None
    
    # Mais on hérite aussi de méthodes qu'on ne veut pas:
    # - insert() ❌
    # - sort() ❌
    # - reverse() ❌
    # etc.
```

```python
# ✅ BON : Composition
class Stack:
    """
    Stack utilise une liste en interne (composition)
    Contrôle total sur l'interface
    """
    def __init__(self):
        self._items = []  # Composition
    
    def push(self, item):
        """Ajoute un élément"""
        self._items.append(item)
    
    def pop(self):
        """Retire et retourne le dernier élément"""
        if not self._items:
            raise IndexError("Stack vide")
        return self._items.pop()
    
    def peek(self):
        """Regarde le dernier élément sans le retirer"""
        if not self._items:
            return None
        return self._items[-1]
    
    def is_empty(self):
        """Vérifie si la stack est vide"""
        return len(self._items) == 0
    
    def __len__(self):
        return len(self._items)


# Démonstration
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)

print(f"Sommet: {stack.peek()}")  # 3
print(f"Pop: {stack.pop()}")      # 3
print(f"Nouveau sommet: {stack.peek()}")  # 2
```

### Exemple : Voiture (Composition appropriée)

```python
class Engine:
    """Moteur"""
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.running = False
    
    def start(self):
        self.running = True
        print(f"🔧 Moteur {self.horsepower}CV démarré")
    
    def stop(self):
        self.running = False
        print(f"🔧 Moteur arrêté")


class Wheel:
    """Roue"""
    def __init__(self, size):
        self.size = size
    
    def __str__(self):
        return f"Roue {self.size}\""


class Car:
    """
    Voiture utilise la composition
    Une voiture A UN moteur (pas EST UN moteur)
    Une voiture A DES roues (pas EST UNE roue)
    """
    def __init__(self, brand, model, horsepower, fuel_type):
        self.brand = brand
        self.model = model
        # Composition : créer les composants
        self.engine = Engine(horsepower, fuel_type)
        self.wheels = [Wheel(17) for _ in range(4)]
    
    def start(self):
        """Démarre la voiture"""
        print(f"🚗 Démarrage de la {self.brand} {self.model}")
        self.engine.start()
    
    def stop(self):
        """Arrête la voiture"""
        print(f"🚗 Arrêt de la {self.brand} {self.model}")
        self.engine.stop()
    
    def get_info(self):
        """Informations sur la voiture"""
        return f"{self.brand} {self.model} - Moteur {self.engine.horsepower}CV"


# Démonstration
car = Car("Toyota", "Corolla", 120, "Essence")
print(car.get_info())
car.start()
car.stop()
```

### Règle d'Or : "Favor Composition Over Inheritance"

```python
# ❌ Héritage inapproprié
class Employee:
    pass

class Manager(Employee):
    """Un manager EST-IL vraiment un type différent d'employé ?"""
    pass


# ✅ Composition appropriée
class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role  # Composition du rôle
        self.responsibilities = []

class Role:
    def __init__(self, title, permissions):
        self.title = title
        self.permissions = permissions

# Créer des employés avec différents rôles
employee1 = Employee("Marie", Role("Developer", ["code", "review"]))
employee2 = Employee("Jean", Role("Manager", ["code", "review", "hire"]))
```

---

## 6. Attributs Protégés et Privés dans l'Héritage

### Convention Python

```python
class Parent:
    def __init__(self):
        self.public = "Accessible partout"
        self._protected = "Convention: usage interne"
        self.__private = "Name mangling appliqué"
    
    def _protected_method(self):
        """Méthode protégée (convention)"""
        return "Protégée"
    
    def __private_method(self):
        """Méthode privée (name mangling)"""
        return "Privée"


class Child(Parent):
    def __init__(self):
        super().__init__()
    
    def access_attributes(self):
        print(f"Public: {self.public}")  # ✓ OK
        print(f"Protected: {self._protected}")  # ✓ OK (convention)
        # print(f"Private: {self.__private}")  # ✗ AttributeError
        
        # Pour accéder au privé (déconseillé):
        print(f"Private (mangled): {self._Parent__private}")  # ✓ Possible mais pas recommandé


# Démonstration
child = Child()
child.access_attributes()
```

### Bonnes Pratiques

```python
class BankAccount:
    """Exemple de bonnes pratiques"""
    
    def __init__(self, owner, balance):
        self.owner = owner  # Public
        self._balance = balance  # Protected (usage interne)
        self.__pin = "1234"  # Private (vraiment privé)
    
    @property
    def balance(self):
        """Getter pour balance (lecture seule)"""
        return self._balance
    
    def deposit(self, amount):
        """Méthode publique"""
        self._validate_amount(amount)  # Méthode protégée
        self._balance += amount
    
    def _validate_amount(self, amount):
        """Méthode protégée : validation interne"""
        if amount <= 0:
            raise ValueError("Montant invalide")
    
    def __verify_pin(self, pin):
        """Méthode privée : vérification PIN"""
        return pin == self.__pin


class SavingsAccount(BankAccount):
    """Compte épargne qui étend BankAccount"""
    
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """Ajoute les intérêts"""
        interest = self._balance * self.interest_rate  # ✓ Accès _balance OK
        # Utilise la méthode publique deposit
        self.deposit(interest)
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **Héritage simple** : Syntaxe et concept  
✅ **super()** : Appeler les méthodes du parent  
✅ **Surcharge de méthodes** : Redéfinir le comportement  
✅ **Hiérarchies complexes** : Plusieurs niveaux d'héritage  
✅ **Composition vs Héritage** : Quand utiliser quoi  
✅ **Attributs protégés/privés** : Convention et name mangling  

### Concepts clés

- **Héritage** = Relation "est un" (is-a)
- **Composition** = Relation "a un" (has-a)
- **super()** = Appel au parent
- **Surcharge** = Redéfinition de méthode
- **Favor composition over inheritance** = Règle d'or

### Dans la Partie 2, nous verrons :

- Héritage multiple
- MRO (Method Resolution Order)
- Mixins
- Classes abstraites (preview du CM3)
- Exercices et cas pratiques

---

*Suite dans la Partie 2...*