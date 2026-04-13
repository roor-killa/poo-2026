# Constats : Surcharge d'Opérateurs (Polymorphisme Ad-hoc)

Ce script illustre comment personnaliser le comportement des opérateurs intégrés de Python (`+`, `-`, `*`, `==`) pour nos propres classes.

## Concept Clé
La **surcharge d'opérateurs** (via les "dunder methods" comme `__add__`) permet d'utiliser une syntaxe mathématique naturelle sur des objets complexes, rendant le code plus expressif.

## Observations (Constats)

1.  **Syntaxe naturelle** : Faire `v1 + v2` est beaucoup plus intuitif que d'appeler `v1.add_vector(v2)`. Cela rapproche le code de la notation mathématique.
2.  **Consistance avec le langage** : En implémentant `__str__` et `__abs__`, notre classe `Vector2D` se comporte exactement comme un type numérique natif de Python (comme `int` ou `float`).
3.  **Encapsulation de la logique** : La complexité de l'addition (additionner x avec x et y avec y) est cachée à l'intérieur de la classe. L'utilisateur voit seulement un signe `+`.
4.  **Interopérabilité** : `__rmul__` permet de gérer la multiplication dans les deux sens (`vecteur * scalar` et `scalar * vecteur`), assurant une flexibilité totale.

## Exemple de surcharge
```python
def __add__(self, other):
    # Cette méthode est appelée par l'opérateur '+'
    return Vector2D(self.x + other.x, self.y + other.y)
```
