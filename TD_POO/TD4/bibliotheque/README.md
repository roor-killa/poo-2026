# TD4 – Mini-Projet : Système de Bibliothèque (POO en Python)

---
s
# 1. Description du projet

Ce mini-projet consiste à développer un **système complet de gestion de bibliothèque** en utilisant les concepts de la Programmation Orientée Objet (POO) étudiés durant les TD.

Le système permet de :

* gérer différents types de **documents**
* gérer différents types **d’utilisateurs**
* effectuer des **emprunts et retours**
* calculer les **frais de retard**
* produire des **statistiques**
* envoyer des **notifications automatiques**

Le projet utilise plusieurs concepts importants :

* héritage
* polymorphisme
* classes abstraites
* composition
* design patterns (Factory, Observer)

---

# 2. Structure du projet

```text
bibliotheque/
│
├── modeles/
│   ├── documents.py
│   ├── utilisateurs.py
│   ├── emprunt.py
│   └── bibliotheque.py
│
├── services/
│   ├── fabrique.py
│   ├── notifications.py
│   └── statistiques.py
│
└── main.py
```

---

# 3. Description des modules

## 3.1 documents.py

Contient la **hiérarchie des documents**.

Classe abstraite :

```
Document
```

Sous-classes :

* Livre
* Magazine
* DVD
* EBook

Chaque document définit :

* une **durée maximale d’emprunt**
* un **calcul des frais de retard**

Exemple :

```python
class Livre(Document):

    def calculer_duree_max_emprunt(self):
        return 21

    def calculer_frais_retard(self, jours):
        return jours * 0.5
```

Cela illustre le **polymorphisme** : chaque type de document possède ses propres règles.

---

## 3.2 utilisateurs.py

Contient la **hiérarchie des utilisateurs**.

Classe abstraite :

```
Utilisateur
```

Sous-classes :

* Etudiant
* Enseignant
* Personnel

Chaque type d'utilisateur possède une **limite d’emprunt différente**.

Exemple :

```python
class Etudiant(Utilisateur):

    def nombre_max_emprunts(self):
        return 5
```

---

## 3.3 emprunt.py

Cette classe représente un **emprunt de document**.

Elle contient :

* utilisateur
* document
* date d'emprunt
* date de retour prévue
* date de retour réelle

Fonctionnalités :

* vérifier si un emprunt est en retard
* calculer les frais de retard

---

## 3.4 bibliotheque.py

Classe principale du système.

Elle gère :

* catalogue de documents
* utilisateurs
* emprunts actifs
* historique des emprunts
* observateurs (notifications)

Fonctions principales :

```
ajouter_document()
ajouter_utilisateur()
emprunter()
retourner()
rechercher_document()
afficher_statistiques()
```

---

## 3.5 fabrique.py

Implémente le **Factory Pattern**.

La factory crée automatiquement les documents selon leur type.

Version améliorée utilisant un dictionnaire :

```python
class FabriqueDocument:

    _types = {
        "livre": Livre,
        "magazine": Magazine,
        "dvd": DVD,
        "ebook": EBook
    }

    @classmethod
    def creer(cls, type_doc, **kwargs):

        if type_doc not in cls._types:
            raise ValueError(f"Type de document inconnu : {type_doc}")

        return cls._types[type_doc](**kwargs)
```

Avantages :

* évite les longues structures `if/elif`
* code plus maintenable
* ajout facile de nouveaux types

---

## 3.6 notifications.py

Implémente le **Observer Pattern**.

Observateurs :

* JournalEvenements
* StatistiquesEmprunts

Lorsqu’un événement se produit (emprunt ou retour), tous les observateurs sont notifiés.

Exemple :

```
Marie a emprunté Python avancé
```

Les observateurs peuvent :

* enregistrer l’événement
* mettre à jour les statistiques

---

## 3.7 statistiques.py

Contient des méthodes permettant de calculer :

* nombre de documents par type
* emprunts par utilisateur
* taux d’utilisation des documents

Exemple :

```
Documents par type :
Livre : 5
DVD : 3
Magazine : 2
```

---

## 3.8 main.py

Point d’entrée du programme.

Il permet de :

1. créer la bibliothèque
2. créer les documents via la factory
3. créer les utilisateurs
4. connecter les observateurs
5. effectuer des emprunts
6. afficher les statistiques

---

# 4. Concepts de POO utilisés

## Héritage

Utilisé pour créer des hiérarchies :

```
Document
 ├ Livre
 ├ Magazine
 ├ DVD
 └ EBook
```

```
Utilisateur
 ├ Etudiant
 ├ Enseignant
 └ Personnel
```

---

## Polymorphisme

Les méthodes suivantes sont redéfinies selon le type d’objet :

```
calculer_duree_max_emprunt()
calculer_frais_retard()
nombre_max_emprunts()
```

Chaque classe implémente sa propre version.

---

## Composition

La classe **Bibliotheque** contient :

* des documents
* des utilisateurs
* des emprunts

Relation :

```
Bibliotheque HAS-A Document
Bibliotheque HAS-A Utilisateur
Bibliotheque HAS-A Emprunt
```

---

# 5. Design Patterns utilisés

## Factory Pattern

Utilisé pour créer les documents automatiquement.

Avantage :

* centralise la création des objets
* facilite l’ajout de nouveaux types

---

## Observer Pattern

Permet de notifier automatiquement plusieurs systèmes lorsqu’un événement se produit.

Exemple :

```
emprunt d'un document
↓
journal mis à jour
↓
statistiques mises à jour
```

---

# 6. Gestion des erreurs

Le système vérifie plusieurs cas :

* document déjà emprunté
* limite d’emprunts atteinte
* type de document inconnu
* document introuvable

Ces vérifications permettent d’éviter les erreurs d’utilisation.

---

# 7. Améliorations possibles

Le système pourrait être amélioré avec :

* une **base de données**
* une **interface graphique**
* une **API web**
* une gestion des **réservations**
* un système de **connexion utilisateurs**

---

# 8. Conclusion

Ce mini-projet permet d’appliquer concrètement plusieurs concepts importants de la programmation orientée objet :

* héritage
* polymorphisme
* abstraction
* composition
* design patterns

Ces concepts sont essentiels pour développer des applications structurées et maintenables.

---
