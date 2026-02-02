# Constats : Polymorphisme par Héritage Simple

C'est l'exemple le plus classique de polymorphisme : des classes filles (`Dog`, `Cat`, `Bird`) qui partagent une interface héritée de leur classe mère (`Animal`).

## Concept Clé
Le **polymorphisme par héritage** permet de traiter un objet comme une instance de sa classe de base, tout en exécutant le comportement spécifique de sa classe réelle (liaison dynamique).

## Observations (Constats)

1.  **Uniformisation via la classe mère** : Tous les animaux sont stockés dans une seule liste de type `Animal`. Cela unifie l'accès aux données.
2.  **Redéfinition (Overriding)** : Chaque classe fille redéfinit `make_sound` et `move`. Le polymorphisme garantit que la version de la classe fille est celle exécutée, même si l'objet est manipulé via une référence de type `Animal`.
3.  **Substitution de Liskov** : On peut passer une instance de `Dog` ou `Cat` à `make_animal_perform` car une classe fille doit pouvoir remplacer sa classe mère sans briser le programme.
4.  **Lisibilité du code** : La boucle `for animal in animals` est extrêmement propre et lisible. On demande à l'animal de "performer" sans se soucier de son espèce.

## Exemple de liaison dynamique
```python
for animal in animals:
    # animal peut être un Dog ou un Cat, Python décide à l'exécution 
    # quelle méthode appeler.
    make_animal_perform(animal)
```
