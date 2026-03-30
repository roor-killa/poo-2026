# CM3 - Polymorphisme et Abstraction (Partie 1)
## Programmation Orientée Objet

---

## Introduction

### Rappel des cours précédents

**CM1 - Classes et Objets :**
- ✅ Classes, objets, attributs, méthodes
- ✅ Méthodes spéciales (`__str__`, `__eq__`, etc.)
- ✅ Encapsulation et propriétés

**CM2 - Héritage et Composition :**
- ✅ Héritage simple et multiple
- ✅ MRO (Method Resolution Order)
- ✅ Mixins
- ✅ Composition vs Héritage

**Aujourd'hui - CM3 :**
- **Polymorphisme** : Un objet, plusieurs formes
- **Abstraction** : Cacher les détails, exposer l'essentiel
- **Classes abstraites** : Interfaces et contrats
- **Duck typing** : "Si ça marche comme un canard..."
- **Protocols** : Type hints avancés

---

## 1. Qu'est-ce que le Polymorphisme ?

### Définition

> **Le polymorphisme permet à des objets de types différents d'être traités de manière uniforme via une interface commune.**

**Étymologie :** Du grec *poly* (plusieurs) et *morphe* (forme)

**En pratique :**
```python
# Même méthode, comportements différents
animal1.make_sound()  # "Woof!"
animal2.make_sound()  # "Miaou!"
animal3.make_sound()  # "Meuuuh!"
```

### Analogie : Télécommande Universelle

```
┌─────────────────────────┐
│   TÉLÉCOMMANDE          │
│                         │
│   [POWER]  [VOL+]       │  ← Interface commune
│   [MUTE]   [VOL-]       │
└─────────────────────────┘
         │
         ├──→ TV (réagit différemment)
         ├──→ Climatisation (réagit différemment)
         └──→ Chaîne Hi-Fi (réagit différemment)
```

**Même bouton, comportements différents = Polymorphisme**

---

## 2. Polymorphisme par Héritage

### 2.1 Premier Exemple

```python
class Animal:
    """Classe de base"""
    
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        """Méthode à redéfinir"""
        return "Un son quelconque"
    
    def move(self):
        """Méthode à redéfinir"""
        return f"{self.name} se déplace"


class Dog(Animal):
    """Chien"""
    
    def make_sound(self):
        return "Woof! Woof!"
    
    def move(self):
        return f"{self.name} court en remuant la queue"


class Cat(Animal):
    """Chat"""
    
    def make_sound(self):
        return "Miaou!"
    
    def move(self):
        return f"{self.name} se déplace silencieusement"


class Bird(Animal):
    """Oiseau"""
    
    def make_sound(self):
        return "Cui cui!"
    
    def move(self):
        return f"{self.name} vole dans le ciel"


# ============================================================================
# DÉMONSTRATION DU POLYMORPHISME
# ============================================================================

def make_animal_perform(animal: Animal):
    """
    Fonction polymorphique
    Accepte n'importe quel Animal et appelle ses méthodes
    """
    print(f"\n{animal.name}:")
    print(f"  Son: {animal.make_sound()}")
    print(f"  Mouvement: {animal.move()}")


if __name__ == "__main__":
    print("=" * 70)
    print("CM3 - POLYMORPHISME PAR HÉRITAGE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer différents animaux
    animals = [
        Dog("Rex"),
        Cat("Minou"),
        Bird("Tweety"),
        Dog("Médor")
    ]
    
    # Polymorphisme en action
    print("\n--- Polymorphisme: même fonction, comportements différents ---")
    for animal in animals:
        make_animal_perform(animal)
    
    # Tous sont des Animal
    print("\n--- Vérification de type ---")
    for animal in animals:
        print(f"{animal.name} est un Animal ? {isinstance(animal, Animal)}")
```

**Sortie :**
```
======================================================================
CM3 - POLYMORPHISME PAR HÉRITAGE - DÉMONSTRATION
======================================================================

--- Polymorphisme: même fonction, comportements différents ---

Rex:
  Son: Woof! Woof!
  Mouvement: Rex court en remuant la queue

Minou:
  Son: Miaou!
  Mouvement: Minou se déplace silencieusement

Tweety:
  Son: Cui cui!
  Mouvement: Tweety vole dans le ciel

Médor:
  Son: Woof! Woof!
  Mouvement: Médor court en remuant la queue

--- Vérification de type ---
Rex est un Animal ? True
Minou est un Animal ? True
Tweety est un Animal ? True
Médor est un Animal ? True
```

**Avantages :**
- ✅ Code générique et réutilisable
- ✅ Facile à étendre (ajouter de nouveaux animaux)
- ✅ Maintenance simplifiée

### 2.2 Exemple Pratique : Système de Paiement

```python
from abc import ABC, abstractmethod
from typing import List


class PaymentMethod(ABC):
    """Interface pour les méthodes de paiement"""
    
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """Traite un paiement"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retourne le nom de la méthode"""
        pass


class CreditCard(PaymentMethod):
    """Paiement par carte de crédit"""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def process_payment(self, amount: float) -> dict:
        print(f"💳 Traitement CB de {amount}€")
        print(f"   Carte: ****{self.card_number[-4:]}")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"CC-{self.card_number[-4:]}-001"
        }
    
    def get_name(self) -> str:
        return "Carte de Crédit"


class PayPal(PaymentMethod):
    """Paiement via PayPal"""
    
    def __init__(self, email: str):
        self.email = email
    
    def process_payment(self, amount: float) -> dict:
        print(f"💰 Traitement PayPal de {amount}€")
        print(f"   Compte: {self.email}")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"PP-{hash(self.email) % 10000}"
        }
    
    def get_name(self) -> str:
        return "PayPal"


class BankTransfer(PaymentMethod):
    """Paiement par virement"""
    
    def __init__(self, iban: str):
        self.iban = iban
    
    def process_payment(self, amount: float) -> dict:
        print(f"🏦 Traitement virement de {amount}€")
        print(f"   IBAN: {self.iban[:10]}...")
        return {
            'status': 'pending',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"BT-{self.iban[-4:]}-001",
            'estimated_days': 3
        }
    
    def get_name(self) -> str:
        return "Virement Bancaire"


class Cryptocurrency(PaymentMethod):
    """Paiement en crypto-monnaie"""
    
    def __init__(self, wallet_address: str, crypto_type: str = "Bitcoin"):
        self.wallet_address = wallet_address
        self.crypto_type = crypto_type
    
    def process_payment(self, amount: float) -> dict:
        print(f"₿ Traitement {self.crypto_type} de {amount}€")
        print(f"   Wallet: {self.wallet_address[:10]}...")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"CRYPTO-{self.wallet_address[-6:]}"
        }
    
    def get_name(self) -> str:
        return f"Crypto ({self.crypto_type})"


# ============================================================================
# SYSTÈME DE COMMERCE - UTILISE LE POLYMORPHISME
# ============================================================================

class Order:
    """Commande"""
    
    def __init__(self, order_id: str, items: List[str], total: float):
        self.order_id = order_id
        self.items = items
        self.total = total
        self.payment_method = None
        self.payment_result = None
    
    def process_payment(self, payment_method: PaymentMethod):
        """
        Traite le paiement - POLYMORPHISME !
        Accepte n'importe quelle PaymentMethod
        """
        print(f"\n--- Commande {self.order_id} ---")
        print(f"Articles: {', '.join(self.items)}")
        print(f"Total: {self.total}€")
        print(f"Méthode: {payment_method.get_name()}")
        
        # Le polymorphisme en action
        self.payment_result = payment_method.process_payment(self.total)
        self.payment_method = payment_method
        
        if self.payment_result['status'] == 'success':
            print(f"✓ Paiement réussi!")
        else:
            print(f"⏳ Paiement en cours...")
        
        return self.payment_result


class ECommercePlatform:
    """Plateforme e-commerce"""
    
    def __init__(self):
        self.orders: List[Order] = []
    
    def create_order(self, order_id: str, items: List[str], 
                    total: float, payment_method: PaymentMethod):
        """
        Crée et traite une commande
        Le polymorphisme permet d'accepter n'importe quelle méthode de paiement
        """
        order = Order(order_id, items, total)
        order.process_payment(payment_method)
        self.orders.append(order)
        return order


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE PAIEMENT - POLYMORPHISME EN ACTION")
    print("=" * 70)
    
    # Créer la plateforme
    platform = ECommercePlatform()
    
    # Différentes méthodes de paiement
    payment_methods = [
        CreditCard("1234567890123456", "123"),
        PayPal("marie@example.com"),
        BankTransfer("FR7612345678901234567890123"),
        Cryptocurrency("1A2B3C4D5E6F7G8H9I0J", "Bitcoin")
    ]
    
    # Traiter des commandes avec différentes méthodes
    items_list = [
        ["Livre POO", "Clavier"],
        ["Écran", "Souris"],
        ["Chaise de bureau"],
        ["GPU", "RAM 32GB"]
    ]
    
    for i, payment_method in enumerate(payment_methods, 1):
        order_id = f"ORD{i:03d}"
        platform.create_order(order_id, items_list[i-1], 
                            50.0 * i, payment_method)
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU POLYMORPHISME:")
    print("- Code générique (Order ne connaît pas les détails)")
    print("- Facile d'ajouter de nouvelles méthodes de paiement")
    print("- Pas de if/elif pour chaque type")
    print("- Respect du principe Open/Closed (SOLID)")
    print("=" * 70)
```

---

## 3. Polymorphisme et Collections

### Collections Hétérogènes

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Forme géométrique"""
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
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
    
    def get_name(self) -> str:
        return f"Rectangle {self.width}x{self.height}"


class Circle(Shape):
    """Cercle"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius
    
    def get_name(self) -> str:
        return f"Cercle rayon {self.radius}"


class Triangle(Shape):
    """Triangle"""
    
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self) -> float:
        # Formule de Héron
        s = self.perimeter() / 2
        import math
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c
    
    def get_name(self) -> str:
        return f"Triangle ({self.a}, {self.b}, {self.c})"


# ============================================================================
# TRAITEMENT POLYMORPHIQUE DE COLLECTIONS
# ============================================================================

def calculate_total_area(shapes: List[Shape]) -> float:
    """Calcule l'aire totale - polymorphisme sur une liste"""
    return sum(shape.area() for shape in shapes)


def display_shapes_info(shapes: List[Shape]):
    """Affiche les infos - polymorphisme sur une liste"""
    print("\n--- Informations des formes ---")
    for i, shape in enumerate(shapes, 1):
        print(f"{i}. {shape.get_name()}")
        print(f"   Aire: {shape.area():.2f}")
        print(f"   Périmètre: {shape.perimeter():.2f}")


def find_largest_shape(shapes: List[Shape]) -> Shape:
    """Trouve la forme avec la plus grande aire"""
    return max(shapes, key=lambda s: s.area())


# Démonstration
print("\n" + "=" * 70)
print("POLYMORPHISME AVEC COLLECTIONS")
print("=" * 70)

# Collection hétérogène de formes
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(3, 4, 5),
    Rectangle(10, 2),
    Circle(2.5)
]

# Opérations polymorphiques
display_shapes_info(shapes)

print(f"\n--- Statistiques ---")
print(f"Aire totale: {calculate_total_area(shapes):.2f}")

largest = find_largest_shape(shapes)
print(f"Plus grande forme: {largest.get_name()} (aire: {largest.area():.2f})")
```

---

## 4. Surcharge d'Opérateurs

### Polymorphisme des Opérateurs

```python
class Vector2D:
    """Vecteur 2D avec surcharge d'opérateurs"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Addition de vecteurs (+)"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Soustraction de vecteurs (-)"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiplication par un scalaire (*)"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        """Multiplication inversée (scalar * vector)"""
        return self.__mul__(scalar)
    
    def __eq__(self, other):
        """Égalité (==)"""
        return self.x == other.x and self.y == other.y
    
    def __abs__(self):
        """Magnitude abs()"""
        import math
        return math.sqrt(self.x**2 + self.y**2)
    
    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"


# Démonstration
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print("\n--- Polymorphisme avec opérateurs ---")
print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"3 * v1 = {3 * v1}")
print(f"|v1| = {abs(v1):.2f}")
print(f"v1 == v2 ? {v1 == v2}")
```

---

## 5. Strategy Pattern (Design Pattern)

### Polymorphisme pour Algorithmes

```python
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    """Interface pour les stratégies de tri"""
    
    @abstractmethod
    def sort(self, data: List) -> List:
        pass


class BubbleSortStrategy(SortStrategy):
    """Tri à bulles"""
    
    def sort(self, data: List) -> List:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        print("Trié avec Bubble Sort")
        return arr


class QuickSortStrategy(SortStrategy):
    """Tri rapide"""
    
    def sort(self, data: List) -> List:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        print("Trié avec Quick Sort")
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    """Contexte utilisant une stratégie"""
    
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        """Change la stratégie à la volée"""
        self.strategy = strategy
    
    def sort(self, data: List) -> List:
        """Délègue le tri à la stratégie"""
        return self.strategy.sort(data)


# Démonstration
data = [64, 34, 25, 12, 22, 11, 90]

print("\n--- Strategy Pattern ---")
print(f"Données: {data}")

sorter = Sorter(BubbleSortStrategy())
result1 = sorter.sort(data)
print(f"Résultat: {result1}")

# Changer de stratégie
sorter.set_strategy(QuickSortStrategy())
result2 = sorter.sort(data)
print(f"Résultat: {result2}")
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **Définition du polymorphisme** : Un objet, plusieurs formes  
✅ **Polymorphisme par héritage** : Surcharge de méthodes  
✅ **Collections hétérogènes** : Listes polymorphiques  
✅ **Surcharge d'opérateurs** : `__add__`, `__mul__`, etc.  
✅ **Applications pratiques** : Paiement, Formes  
✅ **Strategy Pattern** : Polymorphisme pour algorithmes  

### Concepts clés

- **Polymorphisme** = Même interface, comportements différents
- **Interface commune** = Méthodes avec mêmes signatures
- **Collections hétérogènes** = Différents types, même traitement
- **Extensibilité** = Ajouter des types sans modifier le code client

### Dans la Partie 2, nous verrons :

- Classes abstraites en profondeur (ABC)
- Méthodes abstraites et concrètes
- Duck typing vs typing statique
- Protocols (Python 3.8+)
- Type hints avancés
- Cas pratiques complets

---

*Suite dans la Partie 2...*