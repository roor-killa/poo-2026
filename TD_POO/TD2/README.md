# TD2 – Héritage et Composition (Programmation Orientée Objet)


## Objectifs du TD

Ce TD a pour objectif de comprendre et pratiquer plusieurs concepts importants de la Programmation Orientée Objet :

* L’héritage simple
* L’héritage multiple
* Les classes abstraites
* L’utilisation de `super()`
* Le MRO (Method Resolution Order)
* La différence entre **héritage** et **composition**

---

# Exercice 1 – Hiérarchie d’utilisateurs

Dans cet exercice, nous avons modélisé différents types d'utilisateurs d'une bibliothèque.

Classe de base :

```
Utilisateur
```

Sous-classes :

```
Etudiant
Enseignant
Personnel
```

Chaque type d’utilisateur possède des règles différentes concernant :

* le nombre maximum d’emprunts
* la durée maximale d’emprunt

La classe `Utilisateur` est définie comme **classe abstraite** avec des méthodes abstraites :

* `nombre_max_emprunts()`
* `duree_max_emprunt()`

Ces méthodes doivent être implémentées dans chaque sous-classe.

---

## Q1 : Pourquoi utiliser `super().__init__()` dans les sous-classes ?

`super()` permet d’appeler le constructeur de la classe parent.

Exemple :

```python
super().__init__(nom, prenom, id_utilisateur)
```

Cela permet :

* d’éviter de réécrire le même code dans chaque sous-classe
* d’initialiser correctement les attributs définis dans la classe parent
* de rendre le code plus maintenable et lisible

Ainsi, les attributs communs (`nom`, `prenom`, `id_utilisateur`, `emprunts_actifs`) sont initialisés une seule fois dans la classe `Utilisateur`.

---

## Q2 : Que se passe-t-il si on oublie `super().__init__()` ?

Si `super().__init__()` n'est pas appelé :

* les attributs définis dans la classe parent ne seront pas créés
* les variables comme `self.nom` ou `self.emprunts_actifs` n’existeront pas

Cela provoquera une erreur comme :

```
AttributeError
```

Donc les objets ne fonctionneront pas correctement.

---

## Q3 : Peut-on créer une instance de `Utilisateur` directement ?

Non.

La classe `Utilisateur` est une **classe abstraite** car elle contient des méthodes décorées avec :

```
@abstractmethod
```

Python empêche donc la création d’un objet de cette classe.

Exemple interdit :

```
Utilisateur("Dupont", "Jean", "U001")
```

La classe abstraite sert uniquement de **modèle pour les sous-classes**.

---

# Exercice 2 – Héritage multiple

Dans cet exercice, nous avons ajouté des fonctionnalités supplémentaires à certains utilisateurs en utilisant des **mixins**.

Classes mixins :

```
AccesSalleRecherche
PrioriteReservation
```

Classe principale :

```
Doctorant(Etudiant, AccesSalleRecherche, PrioriteReservation)
```

Le doctorant hérite donc de plusieurs classes.

---

## Q1 : Afficher le MRO

Le **MRO (Method Resolution Order)** correspond à l’ordre dans lequel Python recherche les méthodes.

On peut l’afficher avec :

```python
Doctorant.__mro__
```

Résultat typique :

```
Doctorant
Etudiant
AccesSalleRecherche
PrioriteReservation
object
```

---

## Q2 : Dans quel ordre Python cherche les méthodes ?

Python cherche les méthodes dans l’ordre défini par le MRO.

Ordre de recherche :

1. Doctorant
2. Etudiant
3. AccesSalleRecherche
4. PrioriteReservation
5. object

Si une méthode existe dans plusieurs classes, Python utilise **la première trouvée dans cet ordre**.

---

## Q3 : Qu’est-ce que le "Diamond Problem" ?

Le **Diamond Problem** apparaît lorsqu'une classe hérite de deux classes qui héritent elles-mêmes d'une même classe.

Structure :

```
     A
    / \
   B   C
    \ /
     D
```

La question devient :

> Quelle version de la méthode doit être utilisée par D ?

Python résout ce problème grâce à l’algorithme **C3 Linearization**, utilisé pour calculer le **MRO**.

Ainsi Python détermine automatiquement un ordre cohérent de recherche des méthodes.

---

# Exercice 3 – Composition vs Héritage

Dans cet exercice, deux approches sont proposées pour modéliser une bibliothèque.

---

## Approche A – Héritage

Structure :

```
Bibliotheque
   |
BibliothequeUniversitaire
BibliothequeJeunesse
```

### Avantages

* réutilisation du code
* hiérarchie claire entre classes
* spécialisation facile d’une classe

Cependant, cette approche est adaptée uniquement si la relation est :

```
IS-A
```

Exemple :

```
Un chat est un animal
```

---

## Approche B – Composition

Structure :

```
Bibliotheque
   |
   | contient
   ↓
Sections
```

Chaque bibliothèque possède plusieurs sections.

### Avantages

* plus flexible
* structure plus modulaire
* possibilité d’ajouter ou retirer des sections facilement
* meilleure extensibilité du système

La relation ici est :

```
HAS-A
```

Exemple :

```
Une bibliothèque a des sections
```

---

## Q3 : Quelle approche choisir ?

La **composition** est la meilleure approche dans ce cas.

Pourquoi ?

Une bibliothèque **n’est pas un type de section**.
Elle **contient des sections**.

Donc la relation correcte est :

```
Bibliotheque HAS-A Section
```

et non

```
Bibliotheque IS-A Section
```

---

# Conclusion

Ce TD a permis d'étudier plusieurs concepts essentiels de la Programmation Orientée Objet en Python :

* Héritage simple
* Classes abstraites
* Utilisation de `super()`
* Héritage multiple
* MRO (Method Resolution Order)
* Diamond Problem
* Composition vs Héritage

Ces concepts sont fondamentaux pour concevoir des architectures logicielles robustes et modulaires.
