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