# CM2 - Héritage, Composition et MRO (Partie 2)
## Héritage Multiple et Method Resolution Order

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ Héritage simple
- ✅ super() et surcharge
- ✅ Hiérarchies complexes
- ✅ Composition vs Héritage
- ✅ Attributs protégés/privés

**Aujourd'hui - Partie 2 :**
- Héritage multiple
- MRO (Method Resolution Order)
- Problème du diamant
- Mixins
- Classes abstraites (preview CM3)

---

## 7. Héritage Multiple

### Définition

> **L'héritage multiple permet à une classe d'hériter de plusieurs classes parentes.**

```python
class Parent1:
    pass

class Parent2:
    pass

class Enfant(Parent1, Parent2):
    """Hérite de Parent1 ET Parent2"""
    pass
```

### 7.1 Exemple Simple

```python
class Flyable:
    """Capacité de voler"""
    
    def fly(self):
        print(f"{self.name} vole dans le ciel")


class Swimmable:
    """Capacité de nager"""
    
    def swim(self):
        print(f"{self.name} nage dans l'eau")


class Animal:
    """Animal de base"""
    
    def __init__(self, name):
        self.name = name
    
    def eat(self):
        print(f"{self.name} mange")


class Duck(Animal, Flyable, Swimmable):
    """
    Canard : hérite de Animal, Flyable et Swimmable
    Un canard EST un animal qui peut voler ET nager
    """
    
    def __init__(self, name):
        super().__init__(name)
    
    def quack(self):
        print(f"{self.name} fait coin-coin!")


class Fish(Animal, Swimmable):
    """
    Poisson : hérite de Animal et Swimmable
    Un poisson EST un animal qui peut nager
    """
    
    def __init__(self, name):
        super().__init__(name)


class Bird(Animal, Flyable):
    """
    Oiseau : hérite de Animal et Flyable
    Un oiseau EST un animal qui peut voler
    """
    
    def __init__(self, name):
        super().__init__(name)


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CM2 - HÉRITAGE MULTIPLE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer un canard
    print("\n--- Canard (vole ET nage) ---")
    donald = Duck("Donald")
    donald.eat()   # de Animal
    donald.fly()   # de Flyable
    donald.swim()  # de Swimmable
    donald.quack() # propre à Duck
    
    # Créer un poisson
    print("\n--- Poisson (nage uniquement) ---")
    nemo = Fish("Nemo")
    nemo.eat()   # de Animal
    nemo.swim()  # de Swimmable
    # nemo.fly()  # ✗ Erreur : Fish ne peut pas voler
    
    # Créer un oiseau
    print("\n--- Oiseau (vole uniquement) ---")
    tweety = Bird("Tweety")
    tweety.eat()   # de Animal
    tweety.fly()   # de Flyable
    # tweety.swim()  # ✗ Erreur : Bird ne peut pas nager
```

**Sortie :**
```
======================================================================
CM2 - HÉRITAGE MULTIPLE - DÉMONSTRATION
======================================================================

--- Canard (vole ET nage) ---
Donald mange
Donald vole dans le ciel
Donald nage dans l'eau
Donald fait coin-coin!

--- Poisson (nage uniquement) ---
Nemo mange
Nemo nage dans l'eau

--- Oiseau (vole uniquement) ---
Tweety mange
Tweety vole dans le ciel
```

### 7.2 Ordre d'héritage important

```python
class A:
    def method(self):
        print("Méthode de A")


class B:
    def method(self):
        print("Méthode de B")


class C(A, B):  # A d'abord, puis B
    pass


class D(B, A):  # B d'abord, puis A
    pass


# Test
c = C()
c.method()  # Méthode de A (A est avant B)

d = D()
d.method()  # Méthode de B (B est avant A)
```

---

## 8. MRO (Method Resolution Order)

### Qu'est-ce que le MRO ?

> **Le MRO est l'ordre dans lequel Python recherche les méthodes dans la hiérarchie d'héritage.**

**Algorithme utilisé : C3 Linearization**

### 8.1 Voir le MRO d'une classe

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass


# Afficher le MRO
print("\n--- MRO de la classe D ---")
print(D.__mro__)
print()

# Ou de manière plus lisible
print("--- MRO (lisible) ---")
for cls in D.__mro__:
    print(f"  → {cls.__name__}")
```

**Sortie :**
```
--- MRO de la classe D ---
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, 
 <class '__main__.A'>, <class 'object'>)

--- MRO (lisible) ---
  → D
  → B
  → C
  → A
  → object
```

### 8.2 Le Problème du Diamant

```python
class A:
    """Classe racine"""
    def method(self):
        print("Méthode de A")


class B(A):
    """Première branche"""
    def method(self):
        print("Méthode de B")
        super().method()


class C(A):
    """Deuxième branche"""
    def method(self):
        print("Méthode de C")
        super().method()


class D(B, C):
    """
    Problème du diamant:
        A
       / \
      B   C
       \ /
        D
    """
    def method(self):
        print("Méthode de D")
        super().method()


# Démonstration
print("\n--- Problème du Diamant ---")
d = D()
d.method()

print("\n--- MRO de D ---")
for cls in D.__mro__:
    print(f"  {cls.__name__}")
```

**Sortie :**
```
--- Problème du Diamant ---
Méthode de D
Méthode de B
Méthode de C
Méthode de A

--- MRO de D ---
  D
  B
  C
  A
  object
```

**Explication :**
- Python garantit qu'aucune classe n'est appelée deux fois
- L'algorithme C3 résout le diamant intelligemment
- `super()` suit toujours le MRO

### 8.3 Exemple Pratique : Système de Permissions

```python
class Readable:
    """Mixin pour la lecture"""
    
    def read(self):
        print(f"[{self.__class__.__name__}] Lecture autorisée")
        return True


class Writable:
    """Mixin pour l'écriture"""
    
    def write(self):
        print(f"[{self.__class__.__name__}] Écriture autorisée")
        return True


class Executable:
    """Mixin pour l'exécution"""
    
    def execute(self):
        print(f"[{self.__class__.__name__}] Exécution autorisée")
        return True


class File:
    """Fichier de base"""
    
    def __init__(self, name):
        self.name = name
    
    def get_info(self):
        return f"Fichier: {self.name}"


class TextFile(File, Readable, Writable):
    """Fichier texte : lecture + écriture"""
    
    def __init__(self, name):
        super().__init__(name)


class ScriptFile(File, Readable, Writable, Executable):
    """Script : lecture + écriture + exécution"""
    
    def __init__(self, name):
        super().__init__(name)


class ReadOnlyFile(File, Readable):
    """Fichier en lecture seule"""
    
    def __init__(self, name):
        super().__init__(name)


# Démonstration
print("\n--- Fichier Texte ---")
txt = TextFile("document.txt")
print(txt.get_info())
txt.read()
txt.write()
# txt.execute()  # ✗ Erreur

print("\n--- Script ---")
script = ScriptFile("script.sh")
print(script.get_info())
script.read()
script.write()
script.execute()

print("\n--- Fichier Read-Only ---")
readonly = ReadOnlyFile("config.cfg")
print(readonly.get_info())
readonly.read()
# readonly.write()  # ✗ Erreur
```

---

## 9. Mixins

### Définition

> **Un mixin est une classe conçue pour être héritée avec d'autres classes afin d'ajouter des fonctionnalités spécifiques.**

**Caractéristiques d'un mixin :**
- Ne se suffit pas à lui-même
- Ajoute une fonctionnalité précise
- Nom généralement en -able ou -Mixin
- Pas de `__init__` ou très simple

### 9.1 Exemple : Mixins de Logging

```python
import json
from datetime import datetime


class LoggingMixin:
    """Mixin pour ajouter le logging"""
    
    def log(self, message):
        """Ajoute un log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.__class__.__name__}] {message}")


class SerializableMixin:
    """Mixin pour la sérialisation JSON"""
    
    def to_json(self):
        """Convertit en JSON"""
        # Récupère tous les attributs qui ne commencent pas par _
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str):
        """Crée une instance depuis JSON"""
        data = json.loads(json_str)
        return cls(**data)


class ComparableMixin:
    """Mixin pour la comparaison"""
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self.__eq__(other)


class Student(LoggingMixin, SerializableMixin, ComparableMixin):
    """
    Étudiant avec mixins
    Hérite de 3 mixins + logique propre
    """
    
    def __init__(self, name, email, student_id):
        self.name = name
        self.email = email
        self.student_id = student_id
        self.log(f"Étudiant {name} créé")
    
    def enroll(self, course):
        """Inscrit à un cours"""
        self.log(f"Inscription au cours: {course}")
        print(f"✓ {self.name} inscrit à {course}")


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MIXINS - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer un étudiant
    print("\n--- Création et logging ---")
    marie = Student("Marie Lafleur", "marie@ua.fr", "20231001")
    marie.enroll("POO")
    
    # Sérialisation
    print("\n--- Sérialisation JSON ---")
    json_data = marie.to_json()
    print(json_data)
    
    # Désérialisation
    print("\n--- Désérialisation JSON ---")
    marie_copy = Student.from_json(json_data)
    marie_copy.log("Créé depuis JSON")
    
    # Comparaison
    print("\n--- Comparaison ---")
    jean = Student("Jean Martin", "jean@ua.fr", "20231002")
    
    print(f"marie == marie_copy ? {marie == marie_copy}")
    print(f"marie == jean ? {marie == jean}")
    
    # MRO
    print("\n--- MRO de Student ---")
    for cls in Student.__mro__:
        print(f"  → {cls.__name__}")
```

### 9.2 Exemple : Mixin de Timestamp

```python
from datetime import datetime


class TimestampMixin:
    """Mixin pour ajouter created_at et updated_at"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def touch(self):
        """Met à jour le timestamp"""
        self.updated_at = datetime.now()


class SoftDeleteMixin:
    """Mixin pour soft delete (suppression logique)"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deleted_at = None
        self.is_deleted = False
    
    def delete(self):
        """Suppression logique"""
        self.deleted_at = datetime.now()
        self.is_deleted = True
        print(f"✓ {self} marqué comme supprimé")
    
    def restore(self):
        """Restauration"""
        self.deleted_at = None
        self.is_deleted = False
        print(f"✓ {self} restauré")


class Model(TimestampMixin, SoftDeleteMixin):
    """Classe de base avec timestamps et soft delete"""
    
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


class User(Model):
    """Utilisateur"""
    
    def __init__(self, name, email):
        super().__init__(name=name, email=email)
    
    def __str__(self):
        return f"User({self.name})"


# Démonstration
print("\n--- Model avec Mixins ---")
user = User("Marie", "marie@ua.fr")
print(f"Créé à: {user.created_at}")

user.touch()
print(f"Modifié à: {user.updated_at}")

user.delete()
print(f"Supprimé ? {user.is_deleted}")

user.restore()
print(f"Supprimé ? {user.is_deleted}")
```

---

## 10. Classes Abstraites (Preview CM3)

### Introduction

> **Une classe abstraite est une classe qui ne peut pas être instanciée et qui définit une interface que les classes dérivées doivent implémenter.**

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Forme géométrique abstraite"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """Méthode abstraite : doit être implémentée"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Méthode abstraite : doit être implémentée"""
        pass
    
    def describe(self):
        """Méthode concrète : peut être utilisée telle quelle"""
        return f"{self.name} - Aire: {self.area():.2f}, Périmètre: {self.perimeter():.2f}"


class Rectangle(Shape):
    """Rectangle : implémente Shape"""
    
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        """Implémentation de area()"""
        return self.width * self.height
    
    def perimeter(self):
        """Implémentation de perimeter()"""
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Cercle : implémente Shape"""
    
    def __init__(self, radius):
        super().__init__("Cercle")
        self.radius = radius
    
    def area(self):
        """Implémentation de area()"""
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """Implémentation de perimeter()"""
        import math
        return 2 * math.pi * self.radius


# Démonstration
print("\n--- Classes Abstraites ---")

# ✗ Impossible de créer une Shape directement
# shape = Shape("Test")  # TypeError

# ✓ Créer des classes concrètes
rect = Rectangle(5, 3)
circle = Circle(4)

print(rect.describe())
print(circle.describe())
```

---

## 11. Cas Pratique Complet : Système de Personnages de Jeu

```python
from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================================
# MIXINS
# ============================================================================

class LoggableMixin:
    """Mixin pour le logging"""
    
    def log(self, action):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.name}: {action}")


class DamagableMixin:
    """Mixin pour gérer les dégâts"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_hp = 100
        self.current_hp = 100
    
    def take_damage(self, amount):
        """Prend des dégâts"""
        self.current_hp = max(0, self.current_hp - amount)
        self.log(f"Prend {amount} dégâts! HP: {self.current_hp}/{self.max_hp}")
        
        if self.current_hp == 0:
            self.log("Est vaincu!")
            return True
        return False
    
    def heal(self, amount):
        """Se soigne"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        healed = self.current_hp - old_hp
        self.log(f"Récupère {healed} HP! HP: {self.current_hp}/{self.max_hp}")


# ============================================================================
# CLASSES DE BASE
# ============================================================================

class Character(ABC, LoggableMixin, DamagableMixin):
    """Personnage de base (abstrait)"""
    
    def __init__(self, name, level=1):
        super().__init__()
        self.name = name
        self.level = level
        self.experience = 0
        self.log("Créé")
    
    @abstractmethod
    def attack(self, target):
        """Attaque : méthode abstraite"""
        pass
    
    def gain_experience(self, amount):
        """Gagne de l'expérience"""
        self.experience += amount
        self.log(f"Gagne {amount} XP (Total: {self.experience})")
        
        # Level up tous les 100 XP
        if self.experience >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        """Monte de niveau"""
        self.level += 1
        self.max_hp += 20
        self.current_hp = self.max_hp
        self.log(f"LEVEL UP! Niveau {self.level}")


# ============================================================================
# MIXINS DE CAPACITÉS
# ============================================================================

class MagicAbility:
    """Capacité de magie"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mana = 100
        self.max_mana = 100
    
    def cast_spell(self, spell_name, mana_cost, target):
        """Lance un sort"""
        if self.mana < mana_cost:
            self.log(f"Pas assez de mana pour {spell_name}!")
            return False
        
        self.mana -= mana_cost
        self.log(f"Lance {spell_name}! (Mana: {self.mana}/{self.max_mana})")
        return True


class RangedAbility:
    """Capacité d'attaque à distance"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrows = 20
    
    def shoot(self, target):
        """Tire une flèche"""
        if self.arrows <= 0:
            self.log("Plus de flèches!")
            return False
        
        self.arrows -= 1
        damage = 15
        self.log(f"Tire sur {target.name}! (Flèches restantes: {self.arrows})")
        target.take_damage(damage)
        return True


class StealthAbility:
    """Capacité de furtivité"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_hidden = False
    
    def hide(self):
        """Se cache"""
        self.is_hidden = True
        self.log("Se cache dans les ombres...")
    
    def reveal(self):
        """Se révèle"""
        self.is_hidden = False
        self.log("Sort de l'ombre!")


# ============================================================================
# CLASSES DE PERSONNAGES
# ============================================================================

class Warrior(Character):
    """Guerrier : combat au corps-à-corps"""
    
    def __init__(self, name):
        super().__init__(name)
        self.strength = 20
    
    def attack(self, target):
        """Attaque au corps-à-corps"""
        damage = self.strength + (self.level * 2)
        self.log(f"Attaque {target.name} avec l'épée!")
        target.take_damage(damage)
        self.gain_experience(10)


class Mage(Character, MagicAbility):
    """Mage : magie"""
    
    def __init__(self, name):
        super().__init__(name)
        self.intelligence = 25
    
    def attack(self, target):
        """Attaque magique"""
        if self.cast_spell("Boule de feu", 20, target):
            damage = self.intelligence + (self.level * 3)
            target.take_damage(damage)
            self.gain_experience(15)


class Archer(Character, RangedAbility):
    """Archer : attaque à distance"""
    
    def __init__(self, name):
        super().__init__(name)
        self.dexterity = 18
    
    def attack(self, target):
        """Attaque à l'arc"""
        if self.shoot(target):
            self.gain_experience(12)


class Rogue(Character, StealthAbility, RangedAbility):
    """Voleur : furtivité + attaque à distance"""
    
    def __init__(self, name):
        super().__init__(name)
        self.agility = 22
    
    def attack(self, target):
        """Attaque sournoise"""
        damage = self.agility
        
        if self.is_hidden:
            damage *= 2  # Double dégâts si caché
            self.log(f"Attaque sournoise sur {target.name}!")
            self.reveal()
        else:
            self.log(f"Attaque {target.name} avec une dague!")
        
        target.take_damage(damage)
        self.gain_experience(13)


class Paladin(Character, MagicAbility):
    """Paladin : guerrier + magie de soin"""
    
    def __init__(self, name):
        super().__init__(name)
        self.strength = 18
        self.faith = 20
    
    def attack(self, target):
        """Attaque sacrée"""
        damage = self.strength + (self.level * 2)
        self.log(f"Frappe divine sur {target.name}!")
        target.take_damage(damage)
        self.gain_experience(11)
    
    def heal_ally(self, ally):
        """Soigne un allié"""
        if self.cast_spell("Soin", 15, ally):
            heal_amount = self.faith
            ally.heal(heal_amount)


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("JEU RPG - SYSTÈME DE PERSONNAGES")
    print("=" * 70)
    
    # Créer des personnages
    print("\n--- Création des personnages ---")
    warrior = Warrior("Conan")
    mage = Mage("Gandalf")
    archer = Archer("Legolas")
    rogue = Rogue("Shadow")
    paladin = Paladin("Arthur")
    
    # Combat 1 : Warrior vs Mage
    print("\n--- Combat 1: Warrior vs Mage ---")
    warrior.attack(mage)
    mage.attack(warrior)
    
    # Combat 2 : Archer
    print("\n--- Combat 2: Archer ---")
    archer.attack(mage)
    archer.attack(mage)
    
    # Combat 3 : Rogue (furtivité)
    print("\n--- Combat 3: Rogue avec furtivité ---")
    rogue.hide()
    rogue.attack(warrior)
    
    # Paladin soigne
    print("\n--- Paladin soigne ---")
    paladin.heal_ally(warrior)
    paladin.heal_ally(mage)
    
    # Afficher les MRO
    print("\n--- MRO du Paladin ---")
    for i, cls in enumerate(Paladin.__mro__, 1):
        print(f"  {i}. {cls.__name__}")
    
    print("\n--- MRO du Rogue ---")
    for i, cls in enumerate(Rogue.__mro__, 1):
        print(f"  {i}. {cls.__name__}")
```

---

## 12. Exercices Pratiques

### Exercice 1 : Système de Véhicules

Créez un système avec héritage multiple :

**Classes de base :**
- `Vehicle` : classe abstraite
- `ElectricPowered` : mixin pour véhicules électriques
- `GasPowered` : mixin pour véhicules à essence

**Classes concrètes :**
- `ElectricCar` (Vehicle + ElectricPowered)
- `GasCar` (Vehicle + GasPowered)
- `HybridCar` (Vehicle + ElectricPowered + GasPowered)

### Exercice 2 : Système de Notifications

**Mixins :**
- `EmailNotifiable`
- `SMSNotifiable`
- `PushNotifiable`

**Classes :**
- `User` avec différentes combinaisons de mixins
- Implémentez l'envoi de notifications selon les capacités

### Exercice 3 : ORM Simple

Créez un mini-ORM avec mixins :
- `TimestampMixin` (created_at, updated_at)
- `SoftDeleteMixin` (deleted_at)
- `ValidatableMixin` (validation)

---

## 13. Conclusion du CM2

### Récapitulatif

**Partie 1 :**
- ✅ Héritage simple
- ✅ super() et surcharge
- ✅ Composition vs Héritage
- ✅ Attributs protégés/privés

**Partie 2 :**
- ✅ Héritage multiple
- ✅ MRO (Method Resolution Order)
- ✅ Problème du diamant
- ✅ Mixins
- ✅ Classes abstraites (preview)

### Concepts maîtrisés

1. **Héritage simple** : Relation is-a
2. **Héritage multiple** : Plusieurs parents
3. **MRO** : Ordre de résolution (C3)
4. **Mixins** : Fonctionnalités réutilisables
5. **super()** : Navigation dans le MRO
6. **Composition** : Alternative à l'héritage

### Règles d'Or

**Héritage :**
- ✅ "est un" (is-a)
- ✅ Partage de comportements
- ✅ Hiérarchie logique
- ❌ Éviter >3 niveaux

**Composition :**
- ✅ "a un" (has-a)
- ✅ Flexibilité
- ✅ Favor composition over inheritance

**Héritage Multiple :**
- ✅ Mixins pour fonctionnalités
- ✅ Ordre important
- ✅ Comprendre le MRO

---

*Fin du CM2 - Héritage, Composition et MRO*