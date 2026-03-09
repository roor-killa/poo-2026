# TD3 – Polymorphisme et Design Patterns

Licence 2 – Programmation Orientée Objet (Python)

## Objectifs du TD

Ce TD permet de mettre en pratique plusieurs concepts importants de la programmation orientée objet :

* le **polymorphisme**
* les **classes abstraites**
* les **design patterns**
* l’architecture logicielle modulaire

Les patterns étudiés sont :

* Système de notification (polymorphisme)
* Factory Pattern
* Observer Pattern

---

# Exercice 7 – Système de notification

Dans cet exercice, nous avons implémenté un système permettant d’envoyer une notification via différents canaux :

* Email
* SMS
* Notification Push

Toutes ces classes héritent d'une classe abstraite :

```
Notification
```

Chaque classe implémente sa propre version de la méthode :

```
envoyer(message, destinataire)
```

---

## Q1 : Qu’est-ce que le polymorphisme dans cet exercice ?

Le polymorphisme signifie que **plusieurs objets peuvent utiliser la même méthode avec des comportements différents**.

Dans ce cas :

```
notif.envoyer(message, destinataire)
```

peut appeler différentes implémentations :

```
NotificationEmail.envoyer()
NotificationSMS.envoyer()
NotificationPush.envoyer()
```

Le programme utilise donc **la même interface mais avec des comportements différents selon l’objet**.

---

## Q2 : Pourquoi la classe Notification doit-elle être abstraite ?

La classe `Notification` est abstraite car elle sert uniquement de **modèle commun**.

Elle définit :

* une méthode commune : `formater_message()`
* une méthode obligatoire : `envoyer()`

Chaque sous-classe doit implémenter sa propre version de `envoyer()`.

Cela garantit que **tous les types de notifications auront cette méthode**.

---

## Q3 : Comment ajouter un nouveau canal sans modifier le code existant ?

Il suffit de créer une nouvelle classe :

```python
class NotificationWhatsApp(Notification):

    def envoyer(self, message, destinataire):
        print(f"WhatsApp envoyé à {destinataire}")
```

Puis l’ajouter au gestionnaire :

```python
gestionnaire.ajouter_canal(NotificationWhatsApp())
```

On ne modifie pas le code existant.
Cela respecte le principe :

**Open / Closed Principle**

---

# Exercice 8 – Factory Pattern

Le **Factory Pattern** permet de centraliser la création d’objets.

Dans ce TD, nous devons créer différents types de documents :

* Livre
* Magazine
* DVD
* EBook

La classe **FabriqueDocument** décide quel objet créer selon le type demandé.

---

## Q1 : Quel est l’avantage du Factory Pattern ?

Les avantages principaux sont :

* centraliser la création des objets
* simplifier le code principal
* cacher la logique de création
* rendre le système plus extensible

Le programme principal ne connaît pas les classes concrètes.

Il utilise simplement :

```
FabriqueDocument.creer(type_doc)
```

---

## Q2 : Comment ajouter un nouveau type de document ?

Il suffit de :

1. créer une nouvelle classe (exemple : CD)
2. ajouter ce type dans la factory

Cela permet d’étendre le système facilement.

---

## Q3 : Peut-on utiliser un dictionnaire au lieu de if/elif ?

Oui, et c’est **une solution plus élégante et plus maintenable**.

Elle permet d’éviter une longue série de conditions.

---

# Version améliorée du Factory Pattern (avec dictionnaire)

```python
class FabriqueDocument:

    # dictionnaire qui associe un type à une classe
    _types = {
        "livre": Livre,
        "magazine": Magazine,
        "dvd": DVD,
        "ebook": EBook
    }

    @classmethod
    def creer(cls, type_doc, **kwargs):

        # vérifier que le type existe
        if type_doc not in cls._types:
            raise ValueError(f"Type de document inconnu : {type_doc}")

        # récupérer la classe correspondante
        classe_document = cls._types[type_doc]

        # créer l'objet
        return classe_document(**kwargs)
```

### Avantages de cette version

* code plus court
* plus facile à maintenir
* ajout d’un nouveau type très simple

Exemple :

```
FabriqueDocument._types["cd"] = CD
```

---

# Exercice 9 – Observer Pattern

Le **Observer Pattern** permet de notifier automatiquement plusieurs objets lorsqu’un événement se produit.

Dans cet exercice :

* le **document** est l’objet observable
* les **observateurs** réagissent aux événements

Observateurs :

* JournalEvenements
* StatistiquesEmprunts
* NotificateurUtilisateurs

Structure :

```
DocumentObservable
        |
        | notifie
        ↓
Observateurs
```

Lorsqu’un document est emprunté ou retourné, tous les observateurs sont informés.

---

## Q1 : Quelle est la différence avec le pattern Strategy ?

### Observer Pattern

Un objet notifie **plusieurs observateurs** lorsqu’un événement se produit.

Exemple :

```
document.emprunter()
```

Plusieurs systèmes sont informés.

---

### Strategy Pattern

Permet de **changer l’algorithme utilisé**.

Exemple :

```
strategie_paiement = CarteBancaire
```

La stratégie peut être remplacée dynamiquement.

---

## Q2 : Pourquoi utiliser une liste d’observateurs ?

Parce qu’il peut y avoir **plusieurs systèmes à notifier** :

* journal des événements
* statistiques
* notifications
* système de recommandation

Une liste permet d’ajouter ou retirer facilement des observateurs.

---

## Q3 : Comment éviter les références circulaires ?

Une référence circulaire apparaît lorsque deux objets se référencent mutuellement.

Solutions possibles :

* supprimer les observateurs inutiles
* utiliser `weakref` en Python
* éviter que les observateurs stockent une référence forte vers le sujet

Cela permet d’éviter les problèmes de mémoire.

---

# Conclusion

Ce TD a permis de comprendre plusieurs concepts avancés de la POO :

* polymorphisme
* classes abstraites
* Factory Pattern
* Observer Pattern
* architecture modulaire

Ces concepts sont très utilisés dans le développement logiciel professionnel.
