"""
Exercice 1.3 : Méthodes spéciales Python - Vecteur 2D
Implémentation d'une classe Vecteur2D avec surcharge d'opérateurs
"""

import math


class Vecteur2D:
    """
    Classe représentant un vecteur 2D mathématiquement correct.
    Supporte les opérations vectorielles et les surcharges d'opérateurs.
    """
    
    def __init__(self, x, y):
        """
        Initialise un vecteur 2D.
        
        Args:
            x (float): La composante x
            y (float): La composante y
        """
        self.x = x
        self.y = y
    
    def __str__(self):
        """Représentation lisible du vecteur."""
        return f"Vecteur({self.x}, {self.y})"
    
    def __repr__(self):
        """Représentation pour les développeurs."""
        return f"Vecteur2D({self.x}, {self.y})"
    
    def __add__(self, autre):
        """
        Surcharge de l'opérateur + pour l'addition de vecteurs.
        v1 + v2 = Vecteur(x1+x2, y1+y2)
        
        Args:
            autre (Vecteur2D): Le vecteur à ajouter
            
        Returns:
            Vecteur2D: Un nouveau vecteur résultant de l'addition
        """
        if not isinstance(autre, Vecteur2D):
            raise TypeError("On peut seulement ajouter un Vecteur2D à un Vecteur2D")
        
        return Vecteur2D(self.x + autre.x, self.y + autre.y)
    
    def __sub__(self, autre):
        """
        Surcharge de l'opérateur - pour la soustraction de vecteurs.
        v1 - v2 = Vecteur(x1-x2, y1-y2)
        
        Args:
            autre (Vecteur2D): Le vecteur à soustraire
            
        Returns:
            Vecteur2D: Un nouveau vecteur résultant de la soustraction
        """
        if not isinstance(autre, Vecteur2D):
            raise TypeError("On peut seulement soustraire un Vecteur2D d'un Vecteur2D")
        
        return Vecteur2D(self.x - autre.x, self.y - autre.y)
    
    def __mul__(self, scalaire):
        """
        Surcharge de l'opérateur * pour la multiplication par un scalaire.
        v * k = Vecteur(x*k, y*k)
        
        Args:
            scalaire (int, float): Le scalaire multiplicateur
            
        Returns:
            Vecteur2D: Un nouveau vecteur multiplié
        """
        if not isinstance(scalaire, (int, float)):
            raise TypeError("On peut seulement multiplier un vecteur par un nombre")
        
        return Vecteur2D(self.x * scalaire, self.y * scalaire)
    
    def __rmul__(self, scalaire):
        """
        Surcharge de l'opérateur * pour la multiplication à droite.
        k * v = Vecteur(x*k, y*k) (commutativité)
        
        Args:
            scalaire (int, float): Le scalaire multiplicateur
            
        Returns:
            Vecteur2D: Un nouveau vecteur multiplié
        """
        return self.__mul__(scalaire)
    
    def __truediv__(self, scalaire):
        """
        Surcharge de l'opérateur / pour la division par un scalaire.
        v / k = Vecteur(x/k, y/k)
        
        Args:
            scalaire (int, float): Le scalaire diviseur
            
        Returns:
            Vecteur2D: Un nouveau vecteur divisé
            
        Raises:
            ValueError: Si le scalaire est zéro
        """
        if not isinstance(scalaire, (int, float)):
            raise TypeError("On peut seulement diviser un vecteur par un nombre")
        
        if scalaire == 0:
            raise ValueError("Division par zéro impossible")
        
        return Vecteur2D(self.x / scalaire, self.y / scalaire)
    
    def __eq__(self, autre):
        """
        Surcharge de l'opérateur == pour l'égalité de vecteurs.
        v1 == v2 si x1==x2 et y1==y2
        
        Args:
            autre (Vecteur2D): Le vecteur à comparer
            
        Returns:
            bool: True si les vecteurs sont égaux, False sinon
        """
        if not isinstance(autre, Vecteur2D):
            return False
        
        # Utilisation d'une tolérance pour les comparaisons en virgule flottante
        epsilon = 1e-10
        return abs(self.x - autre.x) < epsilon and abs(self.y - autre.y) < epsilon
    
    def __ne__(self, autre):
        """Surcharge de l'opérateur != pour l'inégalité."""
        return not self.__eq__(autre)
    
    def __abs__(self):
        """
        Surcharge de l'opérateur abs() pour la norme du vecteur.
        |v| = sqrt(x² + y²)
        
        Returns:
            float: La norme euclidienne du vecteur
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def __neg__(self):
        """
        Surcharge de l'opérateur unaire - pour l'opposé du vecteur.
        -v = Vecteur(-x, -y)
        
        Returns:
            Vecteur2D: L'opposé du vecteur
        """
        return Vecteur2D(-self.x, -self.y)
    
    def __pos__(self):
        """
        Surcharge de l'opérateur unaire + pour conserver le vecteur.
        +v = Vecteur(x, y)
        
        Returns:
            Vecteur2D: Une copie du vecteur
        """
        return Vecteur2D(self.x, self.y)
    
    def produit_scalaire(self, autre):
        """
        Calcule le produit scalaire avec un autre vecteur.
        v1·v2 = x1*x2 + y1*y2
        
        Args:
            autre (Vecteur2D): L'autre vecteur
            
        Returns:
            float: Le produit scalaire
        """
        if not isinstance(autre, Vecteur2D):
            raise TypeError("Le produit scalaire nécessite deux Vecteur2D")
        
        return self.x * autre.x + self.y * autre.y
    
    def angle_avec(self, autre, en_degres=True):
        """
        Calcule l'angle entre deux vecteurs.
        cos(θ) = (v1·v2) / (|v1| * |v2|)
        
        Args:
            autre (Vecteur2D): L'autre vecteur
            en_degres (bool): Si True, retourne l'angle en degrés; sinon en radians
            
        Returns:
            float: L'angle entre les vecteurs
            
        Raises:
            ValueError: Si l'un des vecteurs est le vecteur nul
        """
        if not isinstance(autre, Vecteur2D):
            raise TypeError("L'angle nécessite deux Vecteur2D")
        
        norme_self = abs(self)
        norme_autre = abs(autre)
        
        # Cas limites : vecteurs nuls
        if norme_self == 0 or norme_autre == 0:
            raise ValueError("Impossible de calculer l'angle avec un vecteur nul")
        
        # Calcul du cosinus de l'angle
        cos_angle = self.produit_scalaire(autre) / (norme_self * norme_autre)
        
        # Ajustement pour les erreurs d'arrondi en virgule flottante
        cos_angle = max(-1, min(1, cos_angle))
        
        angle_rad = math.acos(cos_angle)
        
        if en_degres:
            return math.degrees(angle_rad)
        else:
            return angle_rad
    
    def normaliser(self):
        """
        Retourne un vecteur unitaire dans la même direction.
        
        Returns:
            Vecteur2D: Le vecteur normalisé
            
        Raises:
            ValueError: Si le vecteur est le vecteur nul
        """
        norme = abs(self)
        if norme == 0:
            raise ValueError("Impossible de normaliser un vecteur nul")
        
        return self / norme


# === TESTS DU CODE ===
print("=" * 70)
print("EXERCICE 1.3 : MÉTHODES SPÉCIALES - VECTEUR 2D")
print("=" * 70)

# Création de vecteurs
v1 = Vecteur2D(3, 4)
v2 = Vecteur2D(1, 2)

print(f"\nv1 = {v1}")
print(f"v2 = {v2}")

# Test 1: Addition
print("\n--- ADDITION ---")
v3 = v1 + v2
print(f"v1 + v2 = {v3} (Vecteur(4, 6))")

# Test 2: Soustraction
print("\n--- SOUSTRACTION ---")
v4 = v1 - v2
print(f"v1 - v2 = {v4} (Vecteur(2, 2))")

# Test 3: Multiplication par un scalaire
print("\n--- MULTIPLICATION PAR SCALAIRE ---")
v5 = v1 * 2
print(f"v1 * 2 = {v5} (Vecteur(6, 8))")

v6 = 3 * v1
print(f"3 * v1 = {v6} (Vecteur(9, 12))")

# Test 4: Division par un scalaire
print("\n--- DIVISION PAR SCALAIRE ---")
v7 = v1 / 2
print(f"v1 / 2 = {v7} (Vecteur(1.5, 2.0))")

# Test 5: Égalité
print("\n--- ÉGALITÉ ---")
v8 = Vecteur2D(3, 4)
print(f"v1 == Vecteur2D(3, 4): {v1 == v8}")
print(f"v1 == v2: {v1 == v2}")
print(f"v1 != v2: {v1 != v2}")

# Test 6: Norme (valeur absolue)
print("\n--- NORME (VALEUR ABSOLUE) ---")
norme_v1 = abs(v1)
print(f"|v1| = {norme_v1} (5.0)")
norme_v2 = abs(v2)
print(f"|v2| = {norme_v2:.4f}")

# Test 7: Opposé
print("\n--- OPPOSÉ ---")
v9 = -v1
print(f"-v1 = {v9} (Vecteur(-3, -4))")

# Test 8: Produit scalaire
print("\n--- PRODUIT SCALAIRE ---")
ps = v1.produit_scalaire(v2)
print(f"v1 · v2 = {ps} (11 car: 3*1 + 4*2 = 11)")

# Test 9: Angle entre deux vecteurs
print("\n--- ANGLE ENTRE VECTEURS ---")
angle_deg = v1.angle_avec(v2)
angle_rad = v1.angle_avec(v2, en_degres=False)
print(f"Angle(v1, v2) = {angle_deg:.2f}° ({angle_rad:.4f} rad)")

# Test 10: Vecteurs perpendiculaires
print("\n--- CAS SPÉCIAL: VECTEURS PERPENDICULAIRES ---")
v_perp1 = Vecteur2D(1, 0)
v_perp2 = Vecteur2D(0, 1)
angle_perp = v_perp1.angle_avec(v_perp2)
ps_perp = v_perp1.produit_scalaire(v_perp2)
print(f"Vecteur(1,0) · Vecteur(0,1) = {ps_perp} (perpendiculaires)")
print(f"Angle = {angle_perp:.2f}° (90°)")

# Test 11: Normalisation
print("\n--- NORMALISATION ---")
v_norm = v1.normaliser()
print(f"v1 normalisé = {v_norm}")
print(f"Norme du vecteur normalisé = {abs(v_norm):.10f} (≈ 1.0)")

# Test 12: Cas limites
print("\n--- CAS LIMITES ---")

# Cas limite 1: Division par zéro
print("\n  • Division par zéro:")
try:
    v_zero = v1 / 0
except ValueError as e:
    print(f"    ✓ Exception levée: {e}")

# Cas limite 2: Vecteur nul
print("\n  • Vecteur nul:")
v_null = Vecteur2D(0, 0)
print(f"    Vecteur nul: {v_null}")
print(f"    Norme: {abs(v_null)}")

try:
    angle_null = v1.angle_avec(v_null)
except ValueError as e:
    print(f"    ✓ Exception levée (angle avec vecteur nul): {e}")

try:
    norm_null = v_null.normaliser()
except ValueError as e:
    print(f"    ✓ Exception levée (normalisation vecteur nul): {e}")

# Cas limite 3: Vecteurs colinéaires
print("\n  • Vecteurs colinéaires:")
v_colin1 = Vecteur2D(1, 2)
v_colin2 = Vecteur2D(2, 4)
angle_colin = v_colin1.angle_avec(v_colin2)
print(f"    Vecteur(1,2) et Vecteur(2,4) (colinéaires)")
print(f"    Angle = {angle_colin:.2f}° (0°)")

# Test 13: Vecteurs opposés
print("\n  • Vecteurs opposés:")
v_opp1 = Vecteur2D(1, 1)
v_opp2 = Vecteur2D(-1, -1)
angle_opp = v_opp1.angle_avec(v_opp2)
print(f"    Vecteur(1,1) et Vecteur(-1,-1) (opposés)")
print(f"    Angle = {angle_opp:.2f}° (180°)")

print("\n" + "=" * 70)
