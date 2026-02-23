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