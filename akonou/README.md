# Exercices de Programmation Orientée Objet (POO) - Akonou

Ce dossier contient une série d'exercices couvrant les concepts fondamentaux de la Programmation Orientée Objet en Python.

## 📚 Description des fichiers

### 1. **exo1.py** - Gestion d'un Compte Bancaire
- **Concept** : Passage du procédural à l'objet
- **Contenu** :
  - Classe `CompteBancaire` pour gérer un compte bancaire
  - Méthodes : `deposer()`, `retirer()`, `afficher_solde()`, etc.
  - Historique des transactions
  - Gestion des erreurs avec validations
- **Apprentissage** : Principes de base de l'encapsulation et des attributs privés (`__`)

### 2. **exo2.py** - Gestion des Étudiants
- **Concept** : Attributs de classe et attributs d'instance
- **Contenu** :
  - Classe `Etudiant` pour représenter un étudiant
  - Gestion des notes par matière
  - Calcul des moyennes (générale et par matière)
  - Compteur d'étudiants (attribut de classe)
  - Affichage du bulletin de notes
- **Apprentissage** : Distinction entre variables de classe et d'instance

### 3. **exo3.py** - Classe Vecteur 2D
- **Concept** : Méthodes spéciales Python et surcharge d'opérateurs
- **Contenu** :
  - Classe `Vecteur2D` pour manipuler des vecteurs mathématiques
  - Surcharge d'opérateurs : `+` (addition), `-` (soustraction), `*` (produit scalaire), `/` (division)
  - Surcharge d'opérateurs de comparaison : `==`, `!=`, `<`
  - Calcul de la norme et de l'angle
  - Méthodes magiques : `__str__()`, `__repr__()`, `__len__()`
- **Apprentissage** : Implémentation des méthodes spéciales pour une meilleure intégration avec Python

### 4. **exo2heritagecomposé.py** - Héritage Composé (Problème du Diamond)
- **Concept** : Héritage multiple et ordre de résolution des méthodes (MRO)
- **Contenu** :
  - Classe `Document` (classe de base)
  - Classes `Empruntable` et `Reservable` (deux branches)
  - Classe `LivreNumerique` (hérite des deux)
  - Démonstration de la résolution des appels avec `super()`
- **Apprentissage** : Gestion complexe de l'héritage multiple en Python

### 5. **exo2heritagesimplecm2part2.py** - Héritage Simple et Polymorphisme
- **Concept** : Héritage simple et redéfinition de méthodes
- **Contenu** :
  - Classe `Document` (classe parente)
  - Classes dérivées : `Livre`, `Magazine`, `DVD`
  - Gestion de la disponibilité et de l'emprunt
  - Redéfinition polymorphe de `afficher_info()`
  - Polymorphisme en action
- **Apprentissage** : Principes de l'héritage simple et du polymorphisme

### 6. **exocm3partie1polymorphismeduck.py** - Duck Typing et Polymorphisme
- **Concept** : Polymorphisme par duck typing (typage canard)
- **Contenu** :
  - Classes : `Livre`, `Magazine`, `DVD`
  - Chacune implémente une méthode `afficher()`
  - Fonction `presenter_document()` qui fonctionne avec n'importe quel type
  - Démonstration du duck typing en action
- **Apprentissage** : "Si ça marche comme un canard et ça crie comme un canard, c'est un canard" - fonctionnement sans héritage commun

### 7. **exoencapsulationpart2.py** - Encapsulation Avancée
- **Concept** : Encapsulation avec propriétés (property) et validations
- **Contenu** :
  - Classe `Livre` avec attributs privés et protégés
  - Utilisation de `@property` pour l'accès contrôlé aux données
  - Validations des données via setters
  - Distinction entre attributs privés (`__`) et protégés (`_`)
  - Calcul automatique du prix (avec TVA et remises)
- **Apprentissage** : Encapsulation avancée pour protéger l'intégrité des données

## 🎓 Progression d'apprentissage

1. **Bases** → `exo1.py` : Créer une classe simple avec des méthodes
2. **Attributs** → `exo2.py` : Différencier classe et instance
3. **Opérateurs** → `exo3.py` : Surcharger les opérateurs
4. **Héritage Simple** → `exo2heritagesimplecm2part2.py` : Créer une hiérarchie
5. **Polymorphisme** → `exocm3partie1polymorphismeduck.py` : Flexibilité sans héritage
6. **Héritage Complexe** → `exo2heritagecomposé.py` : Gestion du diamond
7. **Encapsulation** → `exoencapsulationpart2.py` : Protéger les données

## 💻 Implémentations clés

### exo1.py - Classe CompteBancaire

**Attributs privés** :
- `__numero` : numéro IBAN
- `__titulaire` : nom du propriétaire
- `__solde` : solde actuel
- `__historique` : liste des transactions

**Méthodes principales** :
- `deposer(montant)` : ajoute l'argent et enregistre la transaction
- `retirer(montant)` : retire l'argent avec vérification du solde
- `virement(montant, autre_compte)` : transfère vers un autre compte
- `afficher_historique()` : affiche toutes les transactions

**Concepts** :
- Encapsulation avec `__` (double underscore)
- Validation des données (montants positifs)
- Gestion des erreurs avec `ValueError`
- Historique des opérations

### exo2.py - Classes Etudiant et Promotion

**Classe Etudiant** :
- Attributs de classe : `universite`, `nombre_etudiants` (partagés par tous)
- Attributs d'instance : notes par matière dans un dictionnaire
- `ajouter_note(matiere, note)` : enregistre une note
- `calculer_moyenne()` : moyenne générale
- `calculer_moyenne_matiere(matiere)` : moyenne par matière
- `est_admis(seuil)` : vérifie si la moyenne >= seuil
- `obtenir_mention()` : retourne la mention (Passable, Assez bien, Bien, Très bien)
- `comparer_avec(autre_etudiant)` : compare les deux étudiants

**Classe Promotion** :
- Gère une liste d'étudiants
- `calculer_moyenne_promotion()` : moyenne globale
- `calculer_taux_reussite(seuil)` : pourcentage d'admis
- `obtenir_meilleur_etudiant()` : l'étudiant avec la meilleure moyenne
- `afficher_statistiques()` : affichage complet

**Concepts** :
- Variables de classe vs variables d'instance
- Dictionnaires pour stocker les notes
- Itération sur des collections
- Méthodes statiques et de classe

### exo3.py - Classe Vecteur2D

**Surcharge d'opérateurs** :
- `__add__(autre)` : addition vectorielle `v1 + v2`
- `__sub__(autre)` : soustraction `v1 - v2`
- `__mul__(scalaire)` : multiplication par scalaire `v * 3`
- `__rmul__(scalaire)` : multiplication à droite `3 * v`
- `__truediv__(scalaire)` : division par scalaire `v / 2`
- `__eq__(autre)` : comparaison `v1 == v2`
- `__ne__(autre)` : inégalité `v1 != v2`
- `__abs__()` : norme du vecteur `abs(v)` = $\sqrt{x^2 + y^2}$
- `__neg__()` : opposé du vecteur `-v`
- `__pos__()` : copie positive `+v`

**Méthodes mathématiques** :
- `produit_scalaire(autre)` : $v_1 \cdot v_2 = x_1 x_2 + y_1 y_2$
- `angle_avec(autre)` : angle entre deux vecteurs en degrés ou radians
- `normaliser()` : retourne un vecteur unitaire

**Concepts** :
- Méthodes spéciales/magiques (dunder methods)
- Opérations mathématiques surchargées
- Gestion des erreurs (division par zéro)
- Tolérance pour les comparaisons en virgule flottante

### exo2heritagesimplecm2part2.py - Hiérarchie Document

**Classe parent - Document** :
- `__init__(titre, auteur)` : initialise les attributs
- `emprunter()` : marque comme emprunté
- `retourner()` : remet disponible
- `afficher_info()` : affiche les informations
- `obtenir_statut()` : retourne "Disponible" ou "Emprunté"

**Classes dérivées** :
- `Livre(Document)` : ajoute isbn et nb_pages
  - Surcharge `afficher_info()` pour ajouter les détails
- `Magazine(Document)` : ajoute numero et mois
  - Surcharge `afficher_info()` avec numéro et date

**Concepts** :
- Héritage simple avec `class Livre(Document):`
- `super().__init__()` pour appeler le constructeur parent
- Polymorphisme : chaque classe redéfinit `afficher_info()`
- Réutilisation de code via l'héritage

### exocm3partie1polymorphismeduck.py - Duck Typing

**Classes sans héritage commun** :
- `Livre.afficher()` : "Je suis un livre"
- `Magazine.afficher()` : "Je suis un magazine"
- `DVD.afficher()` : "Je suis un DVD"

**Fonction polymorphe** :
```python
def presenter_document(doc):
    print(doc.afficher())  # Pas de vérification de type!
```

**Concepts** :
- Duck typing : "If it walks like a duck and quacks like a duck, it's a duck"
- Pas besoin d'héritage commun
- Tant que l'objet a la méthode `afficher()`, ça marche
- Flexibilité maximale

### exoencapsulationpart2.py - Classe Livre avancée

**Attributs** :
- `_titre` : protégé (lecture seule)
- `_auteur` : protégé (lecture seule)
- `__isbn` : privé (très protégé)
- `_disponible` : protégé avec getter/setter

**Propriétés (Property decorators)** :
- `@property titre` : lecture seule
- `@property auteur` : lecture seule
- `@property isbn` : lecture seule
- `@property titre_modifiable` : avec setter pour validation
- `@property prix_ht` / `@price_ht.setter` : prix avant TVA
- `@property prix_ttc` : prix avec TVA (calculé)

**Validations** :
- Contrôle du format ISBN
- Validations des prix positifs
- Remises entre 0% et 100%

**Concepts** :
- Différence entre `_` (protégé) et `__` (privé)
- Décorateurs `@property` et `.setter`
- Encapsulation avec validations
- Calculs de propriétés dérivées

### exo2heritagecomposé.py - Héritage Multiple (Diamond)

**Structure du problème du Diamond** :
```
     Document
      /  \
  Empruntable  Reservable
      \  /
  LivreNumerique
```

**Résolution avec MRO (Method Resolution Order)** :
- `super().__init__()` pour appeler les constructeurs parents
- Python utilise C3 Linearization pour éviter les appels multiples
- Chaque classe ajoute ses propres fonctionnalités :
  - `Document` : titre de base
  - `Empruntable` : gestion de l'emprunt
  - `Reservable` : gestion des réservations
  - `LivreNumerique` : combine les deux

**Concepts** :
- Héritage multiple complexe
- MRO (Method Resolution Order)
- Appels cascadés avec `super()`
- Avantages et pièges de l'héritage multiple

## 🚀 Exécution

Pour tester un exercice :
```bash
python exo1.py
python exo2.py
python exo3.py
# etc.
```

Chaque fichier contient généralement des exemples d'utilisation dans un bloc `if __name__ == "__main__":` ou directement en fin de fichier.

---
**Auteur** : Akonou  
**Cours** : Programmation Orientée Objet
