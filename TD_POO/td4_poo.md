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

## 📚 TD4 - Mini-projet intégratif (2h)

### 🎯 Objectif
Créer un système complet de bibliothèque utilisant tous les concepts vus.

### Exercice 10 : Système de bibliothèque complet (2h)

**Contexte** : Projet fil rouge - Version objet complète.

**Fonctionnalités attendues :**

1. **Gestion des documents**
   - Hiérarchie : Document (abstrait) → Livre, Magazine, DVD, EBook
   - Factory pour créer des documents
   - Chaque type a ses propres règles d'emprunt

2. **Gestion des utilisateurs**
   - Hiérarchie : Utilisateur (abstrait) → Etudiant, Enseignant, Personnel
   - Mixins pour privilèges spéciaux
   - Chaque type a ses limites d'emprunt

3. **Système d'emprunt**
   - Classe `Emprunt` avec date début, date fin, utilisateur, document
   - Calcul automatique des frais de retard
   - Pattern Observer pour notifications

4. **Bibliothèque**
   - Catalogue de documents
   - Registre d'utilisateurs
   - Historique des emprunts
   - Statistiques

**Architecture suggérée :**
```
bibliotheque/
├── modeles/
│   ├── documents.py       # Hiérarchie de documents
│   ├── utilisateurs.py    # Hiérarchie d'utilisateurs
│   ├── emprunt.py         # Classe Emprunt
│   └── bibliotheque.py    # Classe principale
├── services/
│   ├── fabrique.py        # FabriqueDocument
│   ├── notifications.py   # Système de notifications
│   └── statistiques.py    # Calculs statistiques
└── main.py                # Point d'entrée
```

**Spécifications techniques :**

```python
# documents.py
class Document(ABC):
    @abstractmethod
    def calculer_duree_max_emprunt(self):
        pass
    
    @abstractmethod
    def calculer_frais_retard(self, jours):
        pass

# utilisateurs.py
class Utilisateur(ABC):
    @abstractmethod
    def nombre_max_emprunts(self):
        pass

# emprunt.py
class Emprunt:
    def __init__(self, utilisateur, document, date_emprunt):
        # ...
    
    def est_en_retard(self):
        # ...
    
    def calculer_frais(self):
        # ...

# bibliotheque.py
class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.catalogue = []
        self.utilisateurs = []
        self.emprunts_actifs = []
        self.historique = []
    
    def ajouter_document(self, document):
        # ...
    
    def emprunter(self, utilisateur, document):
        # Vérifier disponibilité
        # Vérifier limites utilisateur
        # Créer emprunt
        # Notifier observateurs
        pass
    
    def retourner(self, emprunt):
        # Calculer frais
        # Mettre à jour statuts
        # Notifier observateurs
        pass
    
    def rechercher_document(self, critere):
        # ...
    
    def statistiques(self):
        # Documents par type
        # Emprunts par utilisateur
        # Taux d'utilisation
        pass
```

**Scénario de test complet :**

```python
# Créer la bibliothèque
biblio = Bibliotheque("Bibliothèque Universitaire")

# Ajouter des documents via Factory
documents_data = [
    {"type": "livre", "titre": "Python avancé", "auteur": "Dupont", "isbn": "123"},
    {"type": "magazine", "titre": "Tech Review", "editeur": "TechPub", "numero": 5},
    {"type": "dvd", "titre": "Formation Python", "realisateur": "Martin", "duree": 120}
]

for data in documents_data:
    type_doc = data.pop("type")
    doc = FabriqueDocument.creer(type_doc, **data)
    biblio.ajouter_document(doc)

# Créer des utilisateurs
etudiant = Etudiant("Dubois", "Marie", "E12345")
enseignant = Enseignant("Leroy", "Jean", "T001")

biblio.ajouter_utilisateur(etudiant)
biblio.ajouter_utilisateur(enseignant)

# Système de notifications
journal = JournalEvenements()
stats = StatistiquesEmprunts()
biblio.ajouter_observateur(journal)
biblio.ajouter_observateur(stats)

# Effectuer des emprunts
livre = biblio.rechercher_document("Python avancé")
biblio.emprunter(etudiant, livre)

# Afficher statistiques
biblio.afficher_statistiques()
```

**Livrables :**
1. Code source complet et commenté
2. Diagramme UML de classes
3. Tests unitaires pour les classes principales
4. Documentation des choix de conception

**Critères d'évaluation :**
- Architecture claire et modulaire (30%)
- Utilisation correcte de l'héritage et composition (25%)
- Polymorphisme et patterns (20%)
- Qualité du code et documentation (15%)
- Tests et gestion des erreurs (10%)

**Questions de réflexion :**
1. Quels design patterns avez-vous utilisés et pourquoi ?
2. Avez-vous préféré l'héritage ou la composition ? Dans quels cas ?
3. Comment votre code gère-t-il les erreurs ?
4. Comment pourrait-on améliorer le système (persistance, API, etc.) ?
5. Si vous avez utilisé l'IA, quelles parties ont été les plus difficiles à faire générer correctement ?

---

## 📊 Grille d'évaluation finale

### Compréhension des concepts (40%)
- Explique clairement classes, objets, instances
- Maîtrise héritage et composition
- Comprend polymorphisme et abstraction
- Utilise correctement l'encapsulation

### Qualité du code (30%)
- Code lisible et bien structuré
- Nommage cohérent
- Commentaires pertinents
- Respect des principes SOLID

### Résolution de problèmes (20%)
- Approche méthodique
- Gestion des cas limites
- Tests et validation

### Utilisation de l'IA (10%)
- Utilisation pertinente
- Esprit critique sur le code généré
- Capacité à expliquer et améliorer

---

## 🎓 Conseils pour réussir

**Avant chaque TD :**
- Relire le CM correspondant
- Préparer ses questions
- Installer l'environnement Python

**Pendant le TD :**
- Travailler en équipe mais comprendre individuellement
- Poser des questions sans hésiter
- Tester son code régulièrement
- Documenter ses choix

**Après le TD :**
- Refaire les exercices seul
- Consulter les ressources complémentaires
- Préparer le TD suivant

**Avec l'IA :**
- Commencer par réfléchir soi-même
- Utiliser l'IA pour vérifier ou débloquer
- Toujours comprendre le code généré
- Améliorer et adapter le code

Bon courage ! 🚀