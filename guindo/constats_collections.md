# Constats : Polymorphisme et Collections

Ce script illustre comment le polymorphisme permet de traiter des objets de types différents (Rectangle, Cercle, Triangle) de manière uniforme au sein d'une même collection.

## Concept Clé
Le concept de **traitement polymorphique de collections** consiste à regrouper des objets ayant une classe de base commune (`Shape`) et à interagir avec eux via l'interface définie par cette base.

## Observations (Constats)

1.  **Hétérogénéité transparente** : La liste `shapes` contient des instances de classes différentes. Pourtant, pour Python et pour nos fonctions de calcul, ce sont tous des "Shapes".
2.  **Simplification du code** : Sans polymorphisme, `calculate_total_area` devrait vérifier le type de chaque objet avec des `if isinstance(...)` pour appeler la bonne méthode de calcul d'aire. Ici, un simple appel à `shape.area()` suffit.
3.  **Extensibilité (Open/Closed Principle)** : Si nous ajoutons une classe `Square(Shape)`, les fonctions `calculate_total_area` et `display_shapes_info` fonctionneront immédiatement sans aucune modification.
4.  **Contrat d'interface** : L'utilisation de `@abstractmethod` garantit que toute nouvelle forme ajoutée à la collection possédera obligatoirement les méthodes nécessaires, évitant ainsi les erreurs à l'exécution.

## Exemple de code polymorphique
```python
def calculate_total_area(shapes: List[Shape]) -> float:
    # Le comportement s'adapte dynamiquement au type réel de chaque 'shape'
    return sum(shape.area() for shape in shapes)
```
