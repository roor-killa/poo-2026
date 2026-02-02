# Constats : Pattern Strategy (Polymorphisme d'Objet)

Ce script utilise le **Pattern Strategy**, qui est une application puissante du polymorphisme pour rendre les algorithmes interchangeables à l'exécution.

## Concept Clé
Le **Pattern Strategy** délègue un comportement spécifique (ici, le tri) à un objet spécialisé. Cela permet de changer "l'intelligence" d'un système sans modifier le système lui-même.

## Observations (Constats)

1.  **Délégation** : La classe `Sorter` ne sait pas comment trier. Elle "possède" une stratégie et lui délègue le travail. C'est le principe de composition préféré à l'héritage.
2.  **Interchangeabilité à l'exécution** : Grâce à `set_strategy`, on peut passer d'un tri à bulle à un tri rapide pendant que le programme tourne. Le polymorphisme garantit que le `Sorter` peut appeler `.sort()` sur n'importe quelle stratégie.
3.  **Découplage** : L'utilisateur du `Sorter` n'a pas besoin de connaître les détails internes de `BubbleSort` ou `QuickSort`. Il interagit uniquement avec l'interface `SortStrategy`.
4.  **Solidité** : Ce pattern respecte le "S" de SOLID (Single Responsibility) car chaque classe de stratégie a une seule responsabilité : implémenter son algorithme.

## Exemple de délégation polymorphique
```python
def sort(self, data: List) -> List:
    # Le Sorter ne sait pas quel algorithme est utilisé ici
    return self.strategy.sort(data)
```
