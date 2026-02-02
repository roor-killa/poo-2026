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

## 📚 TD2 - Héritage et composition (2h)

### 🎯 Objectifs
- Maîtriser l'héritage simple et multiple
- Comprendre composition vs héritage
- Utiliser `super()` correctement

### Exercice 4 : Hiérarchie d'utilisateurs (50min)

**Contexte** : Une bibliothèque a différents types d'utilisateurs.

**Cahier des charges :**

1. Créez une classe de base `Utilisateur` avec :
   - Attributs : `nom`, `prenom`, `id_utilisateur`, `emprunts_actifs` (liste)
   - Méthode `emprunter(document)` qui ajoute à `emprunts_actifs`
   - Méthode `retourner(document)` qui retire de `emprunts_actifs`
   - Méthode abstraite `nombre_max_emprunts()` à implémenter dans les sous-classes

2. Créez les sous-classes :
   - `Etudiant(Utilisateur)` : max 5 emprunts, 21 jours
   - `Enseignant(Utilisateur)` : max 10 emprunts, 60 jours
   - `Personnel(Utilisateur)` : max 7 emprunts, 30 jours

3. Chaque sous-classe doit surcharger :
   - `nombre_max_emprunts()`
   - `duree_max_emprunt()` (en jours)
   - `__str__()` pour afficher le type et le nom

**Diagramme UML à compléter :**
```
        Utilisateur
           |
    ________________
    |       |      |
    ?       ?      ?
```

**Questions :**
- Q1 : Pourquoi utiliser `super().__init__()` dans les sous-classes ?
- Q2 : Que se passe-t-il si on oublie `super().__init__()` ?
- Q3 : Peut-on créer une instance de `Utilisateur` directement ? Pourquoi ?

**Test de votre code :**
```python
etudiant = Etudiant("Dupont", "Marie", "E12345")
enseignant = Enseignant("Martin", "Paul", "T001")

print(etudiant.nombre_max_emprunts())  # 5
print(enseignant.duree_max_emprunt())  # 60

etudiant.emprunter("Livre Python")
print(len(etudiant.emprunts_actifs))  # 1
```

**Challenge IA :**
- Demandez à l'IA de créer cette hiérarchie
- L'IA a-t-elle utilisé une classe abstraite ? Si non, pourquoi est-ce mieux ?
- Modifiez le code pour utiliser `ABC` et `@abstractmethod`

---

### Exercice 5 : Héritage multiple (40min)

**Contexte** : Certains utilisateurs ont des privilèges spéciaux.

**Cahier des charges :**

1. Créez les mixins :
   - `AccesSalleRecherche` : méthode `acceder_salle_recherche()`
   - `PrioriteReservation` : méthode `reserver_avec_priorite(document)`

2. Créez la classe :
   - `Doctorant(Etudiant, AccesSalleRecherche, PrioriteReservation)`

3. Testez le MRO (Method Resolution Order)

**Questions :**
- Q1 : Affichez le MRO de `Doctorant` avec `Doctorant.__mro__`
- Q2 : Dans quel ordre Python cherche-t-il les méthodes ?
- Q3 : Qu'est-ce que le "Diamond Problem" ? Python le résout-il ?

**Code squelette :**
```python
class AccesSalleRecherche:
    def acceder_salle_recherche(self):
        return f"{self.nom} accède à la salle de recherche"

class PrioriteReservation:
    def reserver_avec_priorite(self, document):
        return f"{self.nom} réserve {document} en priorité"

class Doctorant(Etudiant, AccesSalleRecherche, PrioriteReservation):
    def __init__(self, nom, prenom, id_utilisateur, directeur_these):
        super().__init__(nom, prenom, id_utilisateur)
        self.directeur_these = directeur_these

# Test
print(Doctorant.__mro__)
```

---

### Exercice 6 : Composition vs Héritage (30min)

**Contexte** : Modéliser une bibliothèque avec ses sections.

**Débat** : Deux approches possibles

**Approche A - Héritage :**
```python
class Bibliotheque:
    pass

class BibliothequeUniversitaire(Bibliotheque):
    pass

class BibliothequeJeunesse(Bibliotheque):
    pass
```

**Approche B - Composition :**
```python
class Section:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite

class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.sections = []
    
    def ajouter_section(self, section):
        self.sections.append(section)
```

**Questions :**
- Q1 : Quels sont les avantages de l'approche A ?
- Q2 : Quels sont les avantages de l'approche B ?
- Q3 : Laquelle choisiriez-vous et pourquoi ?

**À implémenter :**
Implémentez l'approche B complète avec :
- Classe `Section` : attributs `nom`, `capacite`, `documents` (liste)
- Classe `Bibliotheque` : gère plusieurs sections
- Méthode `rechercher_document(titre)` qui cherche dans toutes les sections
- Méthode `afficher_statistiques()` qui affiche nb documents par section

**Test :**
```python
biblio = Bibliotheque("Bibliothèque Schoelcher")
biblio.ajouter_section(Section("Sciences", 1000))
biblio.ajouter_section(Section("Littérature", 800))
biblio.afficher_statistiques()
```

---