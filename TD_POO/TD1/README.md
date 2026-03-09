# TD1 – Programmation Orientée Objet (POO)

## Objectifs du TD

Ce TD a pour objectif de pratiquer les concepts fondamentaux de la Programmation Orientée Objet en Python :

* Création de classes
* Utilisation des attributs et méthodes
* Encapsulation
* Attributs de classe
* Méthodes de classe

---

# Exercice 1 : Gestion d'étudiants

## Q1 : Pourquoi `notes` doit être une liste et non un attribut simple ?

L'attribut `notes` doit être une liste car un étudiant possède **plusieurs notes** pendant son parcours universitaire.

Exemple :

```
[15, 12, 14, 18, 10]
```

Une liste permet de :

* stocker plusieurs valeurs
* ajouter facilement de nouvelles notes
* calculer une moyenne avec `sum()` et `len()`

Si `notes` n'était pas une liste, on ne pourrait stocker **qu'une seule note**.

---

## Q2 : Que se passe-t-il si on fait `notes = []` en attribut de classe ?

Si on écrit :

```python
class Etudiant:
    notes = []
```

Alors **tous les étudiants partageront la même liste de notes**.

Exemple :

```
etudiant1 ajoute 15
etudiant2 verra aussi 15
```

Cela pose un problème car chaque étudiant doit avoir **ses propres notes**.

C'est pourquoi `notes` doit être créé dans le constructeur :

```python
self.notes = []
```

Ainsi chaque objet étudiant possède **sa propre liste**.

---

## Q3 : Comment empêcher l'ajout d'une note invalide (<0 ou >20) ?

On utilise une **validation dans la méthode** `ajouter_note()` :

```python
if 0 <= note <= 20:
    self.notes.append(note)
else:
    print("Note invalide")
```

Cela permet de garantir que toutes les notes respectent l'échelle universitaire **0 à 20**.

---

# Exercice 2 : Encapsulation et Properties

## Q1 : Quelle est la différence entre `_attribut` et `__attribut` ?

### `_attribut`

C'est un **attribut protégé** (convention Python).

Exemple :

```python
_notes
```

Cela signifie :

* utilisable dans la classe
* utilisable dans les classes enfants
* ne devrait pas être modifié directement depuis l'extérieur

Mais Python ne l'interdit pas techniquement.

---

### `__attribut`

C'est un **attribut privé**.

Exemple :

```python
__numero_etudiant
```

Python applique un mécanisme appelé **name mangling** :

```
__numero_etudiant
↓
_Etudiant__numero_etudiant
```

Cela rend l'accès plus difficile depuis l'extérieur.

---

## Q2 : Peut-on vraiment rendre un attribut privé en Python ?

Non, Python ne rend jamais un attribut totalement privé.

Python utilise surtout des **conventions de programmation**.

Cependant `__attribut` rend l'accès plus difficile et protège mieux les données.

---

## Q3 : Pourquoi utiliser `@property` plutôt qu'une méthode `get_moyenne()` ?

Sans property :

```python
etudiant.get_moyenne()
```

Avec property :

```python
etudiant.moyenne
```

Les avantages :

* code plus lisible
* syntaxe plus naturelle
* possibilité d'ajouter une logique interne sans changer l'interface

C'est la méthode **recommandée en Python moderne**.

---

# Exercice 3 : Attributs de classe

## Q1 : Si je crée 5 étudiants puis j'en supprime 2, que vaut `compteur_total` ?

La valeur restera **5**.

Le compteur augmente lorsqu'un étudiant est créé :

```python
Etudiant.compteur_total += 1
```

Mais il ne diminue pas automatiquement lorsqu'un objet est supprimé.

---

## Q2 : Comment pourrait-on décrémenter le compteur lors de la suppression ?

On pourrait utiliser la méthode spéciale :

```python
def __del__(self):
    Etudiant.compteur_total -= 1
```

Cependant cette méthode n'est **pas toujours fiable** car Python ne garantit pas exactement quand l'objet sera détruit.

---

## Q3 : Si je change `universite` pour un étudiant, cela affecte-t-il les autres ?

Oui.

`universite` est un **attribut de classe**.

Exemple :

```python
Etudiant.universite = "UA - Campus de Schoelcher"
```

Tous les étudiants verront cette nouvelle valeur car l'attribut est **partagé par toute la classe**.

---

# Conclusion

Ce TD permet de comprendre plusieurs concepts fondamentaux de la POO en Python :

* Classes et objets
* Attributs d'instance
* Attributs de classe
* Encapsulation
* Validation des données
* Méthodes de classe
* Utilisation de `@property`

Ces concepts sont essentiels pour développer des applications Python bien structurées et maintenables.
