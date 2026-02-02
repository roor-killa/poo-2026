# Travaux Dirigés - Programmation Orientée Objet (8h)
## Licence 2 - S4 - Python

---

## 📋 Informations générales

**Volume horaire** : 8h de TD
**Organisation** : 4 séances de 2h
**Modalités** : Travail en binôme ou trinôme
**Rendu** : Code commenté + réponses aux questions
**Évaluation** : Participation + justesse des solutions

**⚠️ Règle importante : IA autorisée**
- Vous POUVEZ utiliser ChatGPT, Claude, Copilot, etc.
- MAIS vous devez expliquer chaque ligne de code que vous utilisez
- Des questions orales seront posées pour vérifier votre compréhension
- Le code sans explication = 0 point

---

## 📚 TD1 - Classes, objets et encapsulation (2h)

### 🎯 Objectifs
- Créer des classes simples
- Comprendre attributs et méthodes
- Appliquer l'encapsulation

### Exercice 1 : Gestion d'étudiants (40min)

**Contexte** : Vous devez créer un système de gestion des étudiants de l'université.

**Cahier des charges :**

1. Créez une classe `Etudiant` avec :
   - Attributs : `nom`, `prenom`, `numero_etudiant`, `notes` (liste)
   - Méthode `ajouter_note(note)` qui ajoute une note (entre 0 et 20)
   - Méthode `calculer_moyenne()` qui retourne la moyenne des notes
   - Méthode `est_admis()` qui retourne True si moyenne >= 10

2. Créez une classe `Promotion` avec :
   - Attribut : `nom_promotion`, `etudiants` (liste)
   - Méthode `ajouter_etudiant(etudiant)`
   - Méthode `calculer_moyenne_promotion()`
   - Méthode `lister_admis()` qui retourne la liste des étudiants admis

**Questions :**
- Q1 : Pourquoi `notes` doit-elle être une liste et non un attribut de classe ?
- Q2 : Que se passe-t-il si on fait `notes = []` en attribut de classe ?
- Q3 : Comment empêcher l'ajout d'une note invalide (< 0 ou > 20) ?

**Test de votre code :**
```python
# Créer des étudiants
etudiant1 = Etudiant("Dupont", "Marie", "E12345")
etudiant1.ajouter_note(15)
etudiant1.ajouter_note(12)
etudiant1.ajouter_note(14)

etudiant2 = Etudiant("Martin", "Pierre", "E12346")
etudiant2.ajouter_note(8)
etudiant2.ajouter_note(9)

# Créer une promotion
promo = Promotion("L2 Informatique 2025")
promo.ajouter_etudiant(etudiant1)
promo.ajouter_etudiant(etudiant2)

# Afficher résultats
print(f"Moyenne de {etudiant1.prenom} : {etudiant1.calculer_moyenne()}")
print(f"Est admis ? {etudiant1.est_admis()}")
print(f"Moyenne de la promotion : {promo.calculer_moyenne_promotion()}")
print(f"Étudiants admis : {len(promo.lister_admis())}")
```

**Challenge IA :**
- Générez le code avec une IA de votre choix
- Identifiez 3 problèmes ou améliorations possibles dans le code généré
- Proposez et implémentez vos corrections

---

### Exercice 2 : Encapsulation et properties (40min)

**Contexte** : Améliorer la classe `Etudiant` avec une vraie encapsulation.

**Cahier des charges :**

1. Modifiez la classe `Etudiant` pour :
   - Rendre `numero_etudiant` privé (non modifiable après création)
   - Rendre `notes` protégée
   - Valider que le numéro étudiant commence par "E" suivi de 5 chiffres
   - Créer une property `moyenne` en lecture seule
   - Empêcher l'ajout de notes si l'étudiant a déjà 10 notes

2. Ajoutez une méthode `__str__()` pour un affichage lisible

**Code de départ :**
```python
class Etudiant:
    def __init__(self, nom, prenom, numero_etudiant):
        # TODO : Implémenter avec encapsulation
        pass
```

**Questions :**
- Q1 : Quelle est la différence entre `_attribut` et `__attribut` ?
- Q2 : Peut-on vraiment rendre un attribut privé en Python ?
- Q3 : Pourquoi utiliser `@property` plutôt qu'une méthode `get_moyenne()` ?

**Test de votre code :**
```python
etudiant = Etudiant("Dubois", "Jean", "E12347")
print(etudiant.moyenne)  # Doit fonctionner
# etudiant.moyenne = 15  # Doit échouer
print(etudiant.numero_etudiant)  # Doit fonctionner
# etudiant.numero_etudiant = "E99999"  # Doit échouer

# Tester validation
try:
    etudiant_invalide = Etudiant("Test", "Test", "12345")  # Doit échouer
except ValueError as e:
    print(f"Erreur attendue : {e}")
```

---

### Exercice 3 : Attributs de classe (40min)

**Contexte** : Suivre le nombre total d'étudiants dans l'université.

**Cahier des charges :**

1. Ajoutez à la classe `Etudiant` :
   - Un attribut de classe `compteur_total` qui compte tous les étudiants créés
   - Un attribut de classe `universite` = "Université des Antilles"
   - Une méthode de classe `get_nombre_etudiants()`
   - Une méthode de classe `changer_universite(nouvelle_universite)`

2. Créez une classe `CompteurNotes` qui :
   - Garde un historique de toutes les notes attribuées (attribut de classe)
   - Méthode de classe `ajouter_note_historique(note)`
   - Méthode de classe `statistiques()` qui retourne min, max, moyenne de toutes les notes

**Questions :**
- Q1 : Si je crée 5 étudiants puis en supprime 2, que vaut `compteur_total` ?
- Q2 : Comment pourrait-on décrémenter le compteur lors de la suppression ?
- Q3 : Si je change `universite` pour un étudiant, cela affecte-t-il les autres ?

**Test de votre code :**
```python
print(Etudiant.get_nombre_etudiants())  # 0

e1 = Etudiant("A", "A", "E00001")
e2 = Etudiant("B", "B", "E00002")
e3 = Etudiant("C", "C", "E00003")

print(Etudiant.get_nombre_etudiants())  # 3
print(e1.universite)  # Université des Antilles

Etudiant.changer_universite("UA - Campus de Schoelcher")
print(e2.universite)  # UA - Campus de Schoelcher

# Test statistiques
e1.ajouter_note(15)
e2.ajouter_note(12)
e3.ajouter_note(18)
print(CompteurNotes.statistiques())
```

---