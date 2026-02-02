# CM4 - Design Patterns (Partie 3 - Finale)
## Programmation Orientée Objet

---

## Rappel des Parties 1 et 2

**Partie 1 - Patterns de Création (base) :**
- ✅ Singleton, Factory Method

**Partie 2 - Patterns de Création (suite) + Structure :**
- ✅ Builder, Prototype, Abstract Factory
- ✅ Adapter, Decorator, Facade

**Aujourd'hui - Partie 3 - Patterns Comportementaux :**
- Observer
- Strategy
- Command
- State
- Template Method
- **Applications pratiques** pour vos projets

---

## 1. Introduction aux Patterns Comportementaux

Les patterns comportementaux concernent la **communication entre objets** et la **répartition des responsabilités**.

**Problématiques résolues :**
- Comment les objets communiquent entre eux ?
- Comment encapsuler des algorithmes ?
- Comment gérer les états d'un objet ?
- Comment découpler l'émetteur et le receveur d'une requête ?

---

## 2. Le Pattern Observer

### Problème à résoudre

Vous développez un système de gestion d'événements campus. Quand un événement est créé ou modifié, plusieurs composants doivent être notifiés : le système d'email, le tableau d'affichage, les notifications push, le système de statistiques.

**Problème** : Comment notifier automatiquement plusieurs objets quand un objet change d'état, sans créer de dépendances fortes ?

**Solution** : Observer établit une relation 1-N où les observateurs sont notifiés automatiquement.

### Structure de l'Observer

```python
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


# === Observer Interface ===

class Observer(ABC):
    """Interface pour les observateurs"""
    
    @abstractmethod
    def update(self, subject, event_type, data):
        """Appelé quand le sujet notifie un changement"""
        pass


# === Subject (Observable) ===

class Subject(ABC):
    """Classe de base pour les sujets observables"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Ajoute un observateur"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[Subject] {observer.__class__.__name__} ajouté")
    
    def detach(self, observer: Observer):
        """Retire un observateur"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[Subject] {observer.__class__.__name__} retiré")
    
    def notify(self, event_type, data=None):
        """Notifie tous les observateurs"""
        print(f"\n[Subject] Notification: {event_type}")
        for observer in self._observers:
            observer.update(self, event_type, data)


# === Concrete Subject ===

class Event(Subject):
    """Événement campus observable"""
    
    def __init__(self, title, date, location):
        super().__init__()
        self.title = title
        self.date = date
        self.location = location
        self.status = "DRAFT"
        self.participants = []
    
    def publish(self):
        """Publie l'événement"""
        self.status = "PUBLISHED"
        self.notify("EVENT_PUBLISHED", {
            'title': self.title,
            'date': self.date,
            'location': self.location
        })
    
    def cancel(self):
        """Annule l'événement"""
        old_status = self.status
        self.status = "CANCELLED"
        self.notify("EVENT_CANCELLED", {
            'title': self.title,
            'reason': 'Annulation administrative'
        })
    
    def add_participant(self, participant_email):
        """Ajoute un participant"""
        self.participants.append(participant_email)
        self.notify("PARTICIPANT_ADDED", {
            'title': self.title,
            'participant': participant_email,
            'total_participants': len(self.participants)
        })
    
    def update_location(self, new_location):
        """Change le lieu"""
        old_location = self.location
        self.location = new_location
        self.notify("LOCATION_CHANGED", {
            'title': self.title,
            'old_location': old_location,
            'new_location': new_location
        })


# === Concrete Observers ===

class EmailNotifier(Observer):
    """Envoie des emails lors des changements"""
    
    def update(self, subject, event_type, data):
        if event_type == "EVENT_PUBLISHED":
            self._send_publication_email(data)
        elif event_type == "EVENT_CANCELLED":
            self._send_cancellation_email(data)
        elif event_type == "LOCATION_CHANGED":
            self._send_location_change_email(data)
    
    def _send_publication_email(self, data):
        print(f"  📧 [Email] Nouvel événement: {data['title']}")
        print(f"     Date: {data['date']}, Lieu: {data['location']}")
    
    def _send_cancellation_email(self, data):
        print(f"  📧 [Email] Événement annulé: {data['title']}")
        print(f"     Raison: {data['reason']}")
    
    def _send_location_change_email(self, data):
        print(f"  📧 [Email] Changement de lieu pour {data['title']}")
        print(f"     Nouveau lieu: {data['new_location']}")


class DisplayBoard(Observer):
    """Met à jour le tableau d'affichage"""
    
    def update(self, subject, event_type, data):
        if event_type == "EVENT_PUBLISHED":
            print(f"  📋 [Tableau] Affichage: {data['title']} - {data['date']}")
        elif event_type == "EVENT_CANCELLED":
            print(f"  📋 [Tableau] Retrait: {data['title']}")
        elif event_type == "LOCATION_CHANGED":
            print(f"  📋 [Tableau] Mise à jour lieu: {data['new_location']}")


class PushNotificationService(Observer):
    """Envoie des notifications push"""
    
    def update(self, subject, event_type, data):
        if event_type == "EVENT_PUBLISHED":
            print(f"  📱 [Push] '{data['title']}' publié!")
        elif event_type == "PARTICIPANT_ADDED":
            if data['total_participants'] % 10 == 0:  # Tous les 10 participants
                print(f"  📱 [Push] {data['total_participants']} inscrits à '{data['title']}'")


class StatisticsCollector(Observer):
    """Collecte des statistiques"""
    
    def __init__(self):
        self.stats = {
            'events_published': 0,
            'events_cancelled': 0,
            'total_participants': 0
        }
    
    def update(self, subject, event_type, data):
        if event_type == "EVENT_PUBLISHED":
            self.stats['events_published'] += 1
            print(f"  📊 [Stats] Total événements publiés: {self.stats['events_published']}")
        elif event_type == "EVENT_CANCELLED":
            self.stats['events_cancelled'] += 1
            print(f"  📊 [Stats] Total événements annulés: {self.stats['events_cancelled']}")
        elif event_type == "PARTICIPANT_ADDED":
            self.stats['total_participants'] += 1
    
    def get_report(self):
        """Génère un rapport"""
        return f"""
Rapport Statistiques:
- Événements publiés: {self.stats['events_published']}
- Événements annulés: {self.stats['events_cancelled']}
- Total participants: {self.stats['total_participants']}
"""


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE GESTION D'ÉVÉNEMENTS - PATTERN OBSERVER")
    print("=" * 70)
    
    # Créer les observateurs
    email_notifier = EmailNotifier()
    display_board = DisplayBoard()
    push_service = PushNotificationService()
    stats_collector = StatisticsCollector()
    
    # Créer un événement
    conference = Event(
        title="Conférence IA et Éducation",
        date="2025-03-15 14:00",
        location="Amphi A"
    )
    
    # Attacher les observateurs
    print("\n--- Configuration des observateurs ---")
    conference.attach(email_notifier)
    conference.attach(display_board)
    conference.attach(push_service)
    conference.attach(stats_collector)
    
    # Déclencher des événements
    print("\n--- Événement 1: Publication ---")
    conference.publish()
    
    print("\n--- Événement 2: Ajout de participants ---")
    for i in range(1, 12):
        conference.add_participant(f"etudiant{i}@ua.fr")
    
    print("\n--- Événement 3: Changement de lieu ---")
    conference.update_location("Amphi B")
    
    print("\n--- Événement 4: Annulation ---")
    conference.cancel()
    
    # Rapport final
    print("\n" + "=" * 70)
    print(stats_collector.get_report())
    print("=" * 70)
```

**Sortie** :
```
======================================================================
SYSTÈME DE GESTION D'ÉVÉNEMENTS - PATTERN OBSERVER
======================================================================

--- Configuration des observateurs ---
[Subject] EmailNotifier ajouté
[Subject] DisplayBoard ajouté
[Subject] PushNotificationService ajouté
[Subject] StatisticsCollector ajouté

--- Événement 1: Publication ---

[Subject] Notification: EVENT_PUBLISHED
  📧 [Email] Nouvel événement: Conférence IA et Éducation
     Date: 2025-03-15 14:00, Lieu: Amphi A
  📋 [Tableau] Affichage: Conférence IA et Éducation - 2025-03-15 14:00
  📱 [Push] 'Conférence IA et Éducation' publié!
  📊 [Stats] Total événements publiés: 1

--- Événement 2: Ajout de participants ---

[Subject] Notification: PARTICIPANT_ADDED
  📱 [Push] 10 inscrits à 'Conférence IA et Éducation'

--- Événement 3: Changement de lieu ---

[Subject] Notification: LOCATION_CHANGED
  📧 [Email] Changement de lieu pour Conférence IA et Éducation
     Nouveau lieu: Amphi B
  📋 [Tableau] Mise à jour lieu: Amphi B

--- Événement 4: Annulation ---

[Subject] Notification: EVENT_CANCELLED
  📧 [Email] Événement annulé: Conférence IA et Éducation
     Raison: Annulation administrative
  📋 [Tableau] Retrait: Conférence IA et Éducation
  📊 [Stats] Total événements annulés: 1

======================================================================

Rapport Statistiques:
- Événements publiés: 1
- Événements annulés: 1
- Total participants: 11

======================================================================
```

### ⚠️ Quand utiliser Observer ?

**✅ Utilisez-le pour :**
- Systèmes d'événements et notifications
- MVC (Model-View-Controller)
- Systèmes publish/subscribe
- Logging et monitoring distribués

**❌ Évitez-le pour :**
- Relations simples 1-1
- Quand l'ordre de notification est critique (Observer ne garantit pas l'ordre)

---

## 3. Le Pattern Strategy

### Problème à résoudre

Vous développez un système d'évaluation qui doit supporter différentes méthodes de calcul de notes : moyenne simple, moyenne pondérée, médiane, meilleure note, etc.

**Problème** : Comment permettre de changer l'algorithme dynamiquement sans modifier le code client ?

**Solution** : Strategy encapsule des algorithmes interchangeables.

### Structure de la Strategy

```python
from abc import ABC, abstractmethod
from typing import List


# === Strategy Interface ===

class GradingStrategy(ABC):
    """Interface pour les stratégies de calcul de notes"""
    
    @abstractmethod
    def calculate_grade(self, grades: List[float]) -> float:
        """Calcule la note finale à partir d'une liste de notes"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Retourne la description de la stratégie"""
        pass


# === Concrete Strategies ===

class SimpleAverageStrategy(GradingStrategy):
    """Moyenne arithmétique simple"""
    
    def calculate_grade(self, grades: List[float]) -> float:
        if not grades:
            return 0.0
        return sum(grades) / len(grades)
    
    def get_description(self) -> str:
        return "Moyenne simple de toutes les notes"


class WeightedAverageStrategy(GradingStrategy):
    """Moyenne pondérée"""
    
    def __init__(self, weights: List[float]):
        """
        Args:
            weights: Liste des poids pour chaque note
        """
        self.weights = weights
    
    def calculate_grade(self, grades: List[float]) -> float:
        if not grades or len(grades) != len(self.weights):
            return 0.0
        
        weighted_sum = sum(g * w for g, w in zip(grades, self.weights))
        total_weight = sum(self.weights)
        return weighted_sum / total_weight
    
    def get_description(self) -> str:
        return f"Moyenne pondérée (poids: {self.weights})"


class MedianStrategy(GradingStrategy):
    """Calcul de la médiane"""
    
    def calculate_grade(self, grades: List[float]) -> float:
        if not grades:
            return 0.0
        
        sorted_grades = sorted(grades)
        n = len(sorted_grades)
        
        if n % 2 == 0:
            # Pair: moyenne des deux valeurs centrales
            return (sorted_grades[n//2 - 1] + sorted_grades[n//2]) / 2
        else:
            # Impair: valeur centrale
            return sorted_grades[n//2]
    
    def get_description(self) -> str:
        return "Médiane des notes"


class BestOfStrategy(GradingStrategy):
    """Garde les N meilleures notes"""
    
    def __init__(self, n_best: int):
        """
        Args:
            n_best: Nombre de meilleures notes à garder
        """
        self.n_best = n_best
    
    def calculate_grade(self, grades: List[float]) -> float:
        if not grades:
            return 0.0
        
        # Trier en ordre décroissant et prendre les n meilleures
        best_grades = sorted(grades, reverse=True)[:self.n_best]
        return sum(best_grades) / len(best_grades)
    
    def get_description(self) -> str:
        return f"Moyenne des {self.n_best} meilleures notes"


class PassFailStrategy(GradingStrategy):
    """Système binaire réussite/échec"""
    
    def __init__(self, passing_grade: float = 10.0):
        self.passing_grade = passing_grade
    
    def calculate_grade(self, grades: List[float]) -> float:
        if not grades:
            return 0.0
        
        avg = sum(grades) / len(grades)
        return 20.0 if avg >= self.passing_grade else 0.0
    
    def get_description(self) -> str:
        return f"Réussite/Échec (seuil: {self.passing_grade}/20)"


# === Context ===

class Course:
    """
    Contexte qui utilise une stratégie de notation
    """
    
    def __init__(self, name: str, strategy: GradingStrategy):
        self.name = name
        self._strategy = strategy
        self.students = {}
    
    def set_strategy(self, strategy: GradingStrategy):
        """Change la stratégie de notation"""
        print(f"[{self.name}] Changement de stratégie: {strategy.get_description()}")
        self._strategy = strategy
    
    def add_student_grades(self, student_name: str, grades: List[float]):
        """Enregistre les notes d'un étudiant"""
        self.students[student_name] = grades
    
    def calculate_final_grade(self, student_name: str) -> float:
        """Calcule la note finale d'un étudiant"""
        grades = self.students.get(student_name, [])
        return self._strategy.calculate_grade(grades)
    
    def generate_report(self):
        """Génère un rapport pour tous les étudiants"""
        print(f"\n{'=' * 70}")
        print(f"RAPPORT DE NOTES - {self.name}")
        print(f"Méthode: {self._strategy.get_description()}")
        print(f"{'=' * 70}")
        
        for student, grades in self.students.items():
            final_grade = self.calculate_final_grade(student)
            print(f"{student:20} | Notes: {grades} | Finale: {final_grade:.2f}/20")
        
        print(f"{'=' * 70}\n")


# === Utilisation ===

if __name__ == "__main__":
    # Créer un cours
    poo_course = Course("Programmation Orientée Objet", SimpleAverageStrategy())
    
    # Ajouter des étudiants et leurs notes
    poo_course.add_student_grades("Marie Lafleur", [14, 16, 12, 15])
    poo_course.add_student_grades("Jean Martin", [8, 12, 10, 9])
    poo_course.add_student_grades("Sophie Bernard", [18, 17, 19, 16])
    poo_course.add_student_grades("Paul Dubois", [10, 14, 8, 12])
    
    # Rapport avec moyenne simple
    poo_course.generate_report()
    
    # Changer de stratégie: moyenne pondérée (CC1: 20%, CC2: 20%, Projet: 30%, Examen: 30%)
    poo_course.set_strategy(WeightedAverageStrategy([0.2, 0.2, 0.3, 0.3]))
    poo_course.generate_report()
    
    # Changer de stratégie: médiane
    poo_course.set_strategy(MedianStrategy())
    poo_course.generate_report()
    
    # Changer de stratégie: 3 meilleures notes
    poo_course.set_strategy(BestOfStrategy(3))
    poo_course.generate_report()
    
    # Changer de stratégie: Pass/Fail
    poo_course.set_strategy(PassFailStrategy(passing_grade=10.0))
    poo_course.generate_report()
```

**Sortie** :
```
======================================================================
RAPPORT DE NOTES - Programmation Orientée Objet
Méthode: Moyenne simple de toutes les notes
======================================================================
Marie Lafleur        | Notes: [14, 16, 12, 15] | Finale: 14.25/20
Jean Martin          | Notes: [8, 12, 10, 9] | Finale: 9.75/20
Sophie Bernard       | Notes: [18, 17, 19, 16] | Finale: 17.50/20
Paul Dubois          | Notes: [10, 14, 8, 12] | Finale: 11.00/20
======================================================================

[Programmation Orientée Objet] Changement de stratégie: Moyenne pondérée (poids: [0.2, 0.2, 0.3, 0.3])

======================================================================
RAPPORT DE NOTES - Programmation Orientée Objet
Méthode: Moyenne pondérée (poids: [0.2, 0.2, 0.3, 0.3])
======================================================================
Marie Lafleur        | Notes: [14, 16, 12, 15] | Finale: 14.20/20
Jean Martin          | Notes: [8, 12, 10, 9] | Finale: 9.60/20
Sophie Bernard       | Notes: [18, 17, 19, 16] | Finale: 17.40/20
Paul Dubois          | Notes: [10, 14, 8, 12] | Finale: 10.80/20
======================================================================

[Programmation Orientée Objet] Changement de stratégie: Médiane des notes

======================================================================
RAPPORT DE NOTES - Programmation Orientée Objet
Méthode: Médiane des notes
======================================================================
Marie Lafleur        | Notes: [14, 16, 12, 15] | Finale: 14.50/20
Jean Martin          | Notes: [8, 12, 10, 9] | Finale: 9.50/20
Sophie Bernard       | Notes: [18, 17, 19, 16] | Finale: 17.50/20
Paul Dubois          | Notes: [10, 14, 8, 12] | Finale: 11.00/20
======================================================================
```

### ⚠️ Quand utiliser Strategy ?

**✅ Utilisez-le pour :**
- Algorithmes interchangeables
- Éviter les conditionnels multiples (if/elif/else)
- Configuration runtime d'algorithmes
- Systèmes de pricing, routing, compression

**❌ Évitez-le pour :**
- Un seul algorithme fixe
- Algorithmes qui ne changent jamais

---

## 4. Le Pattern Command

### Problème à résoudre

Vous développez une application de gestion de tâches pour les groupes de projet. Vous voulez supporter undo/redo, macro-commandes, historique, et exécution différée.

**Problème** : Comment encapsuler une requête en tant qu'objet pour supporter undo, redo, logging, etc. ?

**Solution** : Command transforme les requêtes en objets.

### Structure du Command

```python
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


# === Command Interface ===

class Command(ABC):
    """Interface pour toutes les commandes"""
    
    @abstractmethod
    def execute(self):
        """Exécute la commande"""
        pass
    
    @abstractmethod
    def undo(self):
        """Annule la commande"""
        pass
    
    def get_description(self):
        """Description de la commande"""
        return self.__class__.__name__


# === Receiver (celui qui fait le vrai travail) ===

class Task:
    """Tâche d'un projet"""
    
    def __init__(self, title: str):
        self.title = title
        self.description = ""
        self.assignee = None
        self.status = "TODO"
        self.priority = "NORMAL"
    
    def __str__(self):
        return f"[{self.status}] {self.title} (assigné à {self.assignee or 'personne'})"


class ProjectBoard:
    """Tableau de gestion de projet (Receiver)"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task):
        """Ajoute une tâche"""
        self.tasks.append(task)
        print(f"  ✓ Tâche ajoutée: {task.title}")
    
    def remove_task(self, task: Task):
        """Retire une tâche"""
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"  ✓ Tâche retirée: {task.title}")
    
    def update_task_status(self, task: Task, new_status: str):
        """Met à jour le statut d'une tâche"""
        print(f"  ✓ Statut de '{task.title}' changé: {task.status} → {new_status}")
        task.status = new_status
    
    def assign_task(self, task: Task, assignee: str):
        """Assigne une tâche"""
        print(f"  ✓ '{task.title}' assignée à {assignee}")
        task.assignee = assignee
    
    def display_board(self):
        """Affiche toutes les tâches"""
        print(f"\n📋 Projet: {self.project_name}")
        print("=" * 60)
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")
        print("=" * 60 + "\n")


# === Concrete Commands ===

class AddTaskCommand(Command):
    """Commande pour ajouter une tâche"""
    
    def __init__(self, board: ProjectBoard, task: Task):
        self.board = board
        self.task = task
    
    def execute(self):
        self.board.add_task(self.task)
    
    def undo(self):
        self.board.remove_task(self.task)
    
    def get_description(self):
        return f"Ajouter tâche: {self.task.title}"


class RemoveTaskCommand(Command):
    """Commande pour retirer une tâche"""
    
    def __init__(self, board: ProjectBoard, task: Task):
        self.board = board
        self.task = task
        self.task_index = None
    
    def execute(self):
        # Sauvegarder l'index pour l'undo
        self.task_index = self.board.tasks.index(self.task)
        self.board.remove_task(self.task)
    
    def undo(self):
        # Réinsérer à la même position
        self.board.tasks.insert(self.task_index, self.task)
        print(f"  ✓ Tâche restaurée: {self.task.title}")


class UpdateStatusCommand(Command):
    """Commande pour changer le statut"""
    
    def __init__(self, board: ProjectBoard, task: Task, new_status: str):
        self.board = board
        self.task = task
        self.new_status = new_status
        self.old_status = None
    
    def execute(self):
        self.old_status = self.task.status
        self.board.update_task_status(self.task, self.new_status)
    
    def undo(self):
        self.board.update_task_status(self.task, self.old_status)
    
    def get_description(self):
        return f"Changer statut de '{self.task.title}' en {self.new_status}"


class AssignTaskCommand(Command):
    """Commande pour assigner une tâche"""
    
    def __init__(self, board: ProjectBoard, task: Task, assignee: str):
        self.board = board
        self.task = task
        self.assignee = assignee
        self.old_assignee = None
    
    def execute(self):
        self.old_assignee = self.task.assignee
        self.board.assign_task(self.task, self.assignee)
    
    def undo(self):
        self.board.assign_task(self.task, self.old_assignee or "personne")
    
    def get_description(self):
        return f"Assigner '{self.task.title}' à {self.assignee}"


# === Macro Command ===

class MacroCommand(Command):
    """Commande composite qui exécute plusieurs commandes"""
    
    def __init__(self, commands: List[Command]):
        self.commands = commands
    
    def execute(self):
        for command in self.commands:
            command.execute()
    
    def undo(self):
        # Annuler dans l'ordre inverse
        for command in reversed(self.commands):
            command.undo()
    
    def get_description(self):
        return f"Macro: {len(self.commands)} commandes"


# === Invoker ===

class CommandHistory:
    """Gestionnaire d'historique avec undo/redo"""
    
    def __init__(self):
        self.history: List[Command] = []
        self.current_index = -1
    
    def execute_command(self, command: Command):
        """Exécute une commande et l'ajoute à l'historique"""
        # Supprimer les commandes après current_index (pour le redo)
        self.history = self.history[:self.current_index + 1]
        
        command.execute()
        self.history.append(command)
        self.current_index += 1
        
        print(f"  📝 Historique: {command.get_description()}")
    
    def undo(self):
        """Annule la dernière commande"""
        if self.current_index >= 0:
            command = self.history[self.current_index]
            command.undo()
            self.current_index -= 1
            print(f"  ↩️  Undo: {command.get_description()}")
        else:
            print("  ⚠️  Rien à annuler")
    
    def redo(self):
        """Refait la dernière commande annulée"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            command = self.history[self.current_index]
            command.execute()
            print(f"  ↪️  Redo: {command.get_description()}")
        else:
            print("  ⚠️  Rien à refaire")
    
    def show_history(self):
        """Affiche l'historique"""
        print("\n📚 Historique des commandes:")
        for i, command in enumerate(self.history):
            marker = "→" if i == self.current_index else " "
            print(f"  {marker} {i+1}. {command.get_description()}")
        print()


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE GESTION DE PROJET - PATTERN COMMAND")
    print("=" * 70)
    
    # Créer le projet
    board = ProjectBoard("Application Mobile Campus")
    history = CommandHistory()
    
    # Créer des tâches
    task1 = Task("Design de l'interface")
    task2 = Task("Développement backend API")
    task3 = Task("Intégration base de données")
    
    # Exécuter des commandes
    print("\n--- Ajout de tâches ---")
    history.execute_command(AddTaskCommand(board, task1))
    history.execute_command(AddTaskCommand(board, task2))
    history.execute_command(AddTaskCommand(board, task3))
    
    board.display_board()
    
    # Assigner des tâches
    print("--- Assignation ---")
    history.execute_command(AssignTaskCommand(board, task1, "Marie"))
    history.execute_command(AssignTaskCommand(board, task2, "Jean"))
    
    board.display_board()
    
    # Changer des statuts
    print("--- Changements de statut ---")
    history.execute_command(UpdateStatusCommand(board, task1, "IN_PROGRESS"))
    history.execute_command(UpdateStatusCommand(board, task1, "DONE"))
    
    board.display_board()
    
    # Afficher l'historique
    history.show_history()
    
    # Undo
    print("--- Undo x2 ---")
    history.undo()
    history.undo()
    
    board.display_board()
    
    # Redo
    print("--- Redo x1 ---")
    history.redo()
    
    board.display_board()
    
    # Macro commande
    print("--- Macro: Setup complet d'une nouvelle tâche ---")
    task4 = Task("Tests unitaires")
    macro = MacroCommand([
        AddTaskCommand(board, task4),
        AssignTaskCommand(board, task4, "Sophie"),
        UpdateStatusCommand(board, task4, "IN_PROGRESS")
    ])
    
    history.execute_command(macro)
    board.display_board()
    
    print("--- Undo du macro (tout s'annule) ---")
    history.undo()
    board.display_board()
```

**Sortie partielle** :
```
======================================================================
SYSTÈME DE GESTION DE PROJET - PATTERN COMMAND
======================================================================

--- Ajout de tâches ---
  ✓ Tâche ajoutée: Design de l'interface
  📝 Historique: Ajouter tâche: Design de l'interface
  ✓ Tâche ajoutée: Développement backend API
  📝 Historique: Ajouter tâche: Développement backend API
  ✓ Tâche ajoutée: Intégration base de données
  📝 Historique: Ajouter tâche: Intégration base de données

📋 Projet: Application Mobile Campus
============================================================
1. [TODO] Design de l'interface (assigné à personne)
2. [TODO] Développement backend API (assigné à personne)
3. [TODO] Intégration base de données (assigné à personne)
============================================================

--- Assignation ---
  ✓ 'Design de l'interface' assignée à Marie
  📝 Historique: Assigner 'Design de l'interface' à Marie
  ✓ 'Développement backend API' assignée à Jean
  📝 Historique: Assigner 'Développement backend API' à Jean
```

### ⚠️ Quand utiliser Command ?

**✅ Utilisez-le pour :**
- Undo/Redo
- Transaction systems
- Macro-commandes
- Queue de tâches différées
- Logging d'opérations

**❌ Évitez-le pour :**
- Opérations simples sans historique
- Quand l'overhead est trop important

---

## 5. Le Pattern State

### Problème à résoudre

Vous gérez un système de réservation de salles qui a différents états : disponible, réservée, en maintenance, confirmée. Le comportement change selon l'état.

**Problème** : Comment gérer les transitions d'état et les comportements spécifiques à chaque état sans conditionnels complexes ?

**Solution** : State encapsule les comportements spécifiques à chaque état dans des classes séparées.

### Structure du State

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# === State Interface ===

class RoomState(ABC):
    """Interface pour les états d'une salle"""
    
    @abstractmethod
    def reserve(self, room, user):
        """Tenter de réserver la salle"""
        pass
    
    @abstractmethod
    def confirm(self, room):
        """Confirmer la réservation"""
        pass
    
    @abstractmethod
    def cancel(self, room):
        """Annuler la réservation"""
        pass
    
    @abstractmethod
    def start_maintenance(self, room):
        """Mettre en maintenance"""
        pass
    
    @abstractmethod
    def get_status(self):
        """Retourner le statut"""
        pass


# === Concrete States ===

class AvailableState(RoomState):
    """État: Salle disponible"""
    
    def reserve(self, room, user):
        print(f"✓ Réservation de {room.name} par {user}")
        room.reserved_by = user
        room.reserved_at = datetime.now()
        room.state = PendingState()
    
    def confirm(self, room):
        print("⚠️  Impossible de confirmer: aucune réservation")
    
    def cancel(self, room):
        print("⚠️  Impossible d'annuler: aucune réservation")
    
    def start_maintenance(self, room):
        print(f"🔧 {room.name} mise en maintenance")
        room.state = MaintenanceState()
    
    def get_status(self):
        return "DISPONIBLE"


class PendingState(RoomState):
    """État: Réservation en attente de confirmation"""
    
    def reserve(self, room, user):
        print(f"⚠️  {room.name} déjà réservée par {room.reserved_by}")
    
    def confirm(self, room):
        print(f"✓ Réservation confirmée pour {room.reserved_by}")
        room.confirmed_at = datetime.now()
        room.state = ConfirmedState()
    
    def cancel(self, room):
        print(f"✓ Réservation annulée")
        room.reserved_by = None
        room.reserved_at = None
        room.state = AvailableState()
    
    def start_maintenance(self, room):
        print("⚠️  Annulez d'abord la réservation")
    
    def get_status(self):
        return "EN_ATTENTE"


class ConfirmedState(RoomState):
    """État: Réservation confirmée"""
    
    def reserve(self, room, user):
        print(f"⚠️  {room.name} déjà confirmée pour {room.reserved_by}")
    
    def confirm(self, room):
        print("⚠️  Déjà confirmée")
    
    def cancel(self, room):
        print(f"✓ Réservation confirmée annulée")
        room.reserved_by = None
        room.reserved_at = None
        room.confirmed_at = None
        room.state = AvailableState()
    
    def start_maintenance(self, room):
        print("⚠️  Annulez d'abord la réservation confirmée")
    
    def get_status(self):
        return "CONFIRMÉE"


class MaintenanceState(RoomState):
    """État: Salle en maintenance"""
    
    def reserve(self, room, user):
        print(f"⚠️  {room.name} en maintenance, réservation impossible")
    
    def confirm(self, room):
        print("⚠️  Salle en maintenance")
    
    def cancel(self, room):
        print("⚠️  Aucune réservation à annuler")
    
    def start_maintenance(self, room):
        print("⚠️  Déjà en maintenance")
    
    def get_status(self):
        return "MAINTENANCE"


# === Context ===

class Room:
    """
    Salle de cours (Context qui utilise des states)
    """
    
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.state = AvailableState()  # État initial
        
        # Informations de réservation
        self.reserved_by = None
        self.reserved_at = None
        self.confirmed_at = None
    
    # Délégation aux states
    def reserve(self, user: str):
        """Réserver la salle"""
        self.state.reserve(self, user)
    
    def confirm(self):
        """Confirmer la réservation"""
        self.state.confirm(self)
    
    def cancel(self):
        """Annuler la réservation"""
        self.state.cancel(self)
    
    def start_maintenance(self):
        """Mettre en maintenance"""
        self.state.start_maintenance(self)
    
    def get_info(self):
        """Obtenir les informations de la salle"""
        info = f"""
📍 Salle: {self.name}
👥 Capacité: {self.capacity} personnes
🚦 Statut: {self.state.get_status()}
"""
        if self.reserved_by:
            info += f"👤 Réservée par: {self.reserved_by}\n"
            info += f"🕒 Depuis: {self.reserved_at.strftime('%H:%M')}\n"
        
        return info


# === Utilisation ===

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE RÉSERVATION DE SALLES - PATTERN STATE")
    print("=" * 70)
    
    # Créer une salle
    amphi_a = Room("Amphithéâtre A", 200)
    
    # Scénario 1: Réservation normale
    print("\n--- Scénario 1: Réservation et confirmation ---")
    print(amphi_a.get_info())
    
    amphi_a.reserve("Groupe 1 - POO")
    print(amphi_a.get_info())
    
    amphi_a.confirm()
    print(amphi_a.get_info())
    
    # Scénario 2: Tentative de réservation sur salle confirmée
    print("\n--- Scénario 2: Tentative de double réservation ---")
    amphi_a.reserve("Groupe 2 - Web")
    
    # Scénario 3: Annulation
    print("\n--- Scénario 3: Annulation ---")
    amphi_a.cancel()
    print(amphi_a.get_info())
    
    # Scénario 4: Réservation puis maintenance
    print("\n--- Scénario 4: Réservation puis tentative de maintenance ---")
    amphi_a.reserve("Groupe 3 - Mobile")
    amphi_a.start_maintenance()  # Impossible
    
    amphi_a.cancel()  # D'abord annuler
    amphi_a.start_maintenance()  # Maintenant possible
    print(amphi_a.get_info())
    
    # Scénario 5: Tentative de réservation en maintenance
    print("\n--- Scénario 5: Réservation pendant maintenance ---")
    amphi_a.reserve("Groupe 4 - BD")
```

**Sortie** :
```
======================================================================
SYSTÈME DE RÉSERVATION DE SALLES - PATTERN STATE
======================================================================

--- Scénario 1: Réservation et confirmation ---

📍 Salle: Amphithéâtre A
👥 Capacité: 200 personnes
🚦 Statut: DISPONIBLE

✓ Réservation de Amphithéâtre A par Groupe 1 - POO

📍 Salle: Amphithéâtre A
👥 Capacité: 200 personnes
🚦 Statut: EN_ATTENTE
👤 Réservée par: Groupe 1 - POO
🕒 Depuis: 14:30

✓ Réservation confirmée pour Groupe 1 - POO

📍 Salle: Amphithéâtre A
👥 Capacité: 200 personnes
🚦 Statut: CONFIRMÉE
👤 Réservée par: Groupe 1 - POO
🕒 Depuis: 14:30

--- Scénario 2: Tentative de double réservation ---
⚠️  Amphithéâtre A déjà confirmée pour Groupe 1 - POO

--- Scénario 3: Annulation ---
✓ Réservation confirmée annulée

📍 Salle: Amphithéâtre A
👥 Capacité: 200 personnes
🚦 Statut: DISPONIBLE

--- Scénario 4: Réservation puis tentative de maintenance ---
✓ Réservation de Amphithéâtre A par Groupe 3 - Mobile
⚠️  Annulez d'abord la réservation
✓ Réservation annulée
🔧 Amphithéâtre A mise en maintenance

📍 Salle: Amphithéâtre A
👥 Capacité: 200 personnes
🚦 Statut: MAINTENANCE

--- Scénario 5: Réservation pendant maintenance ---
⚠️  Amphithéâtre A en maintenance, réservation impossible
```

### ⚠️ Quand utiliser State ?

**✅ Utilisez-le pour :**
- Objets avec comportements dépendant de leur état
- Machines à états (workflow, connexions, commandes)
- Éviter les gros switch/case sur les états
- États avec transitions complexes

**❌ Évitez-le pour :**
- 2-3 états simples (un boolean suffit)
- États sans comportements différents

---

## 6. Le Pattern Template Method

### Problème à résoudre

Vous avez plusieurs types de rapports à générer (étudiant, cours, département) qui suivent tous la même structure : en-tête, contenu, statistiques, pied de page.

**Problème** : Comment définir le squelette d'un algorithme en laissant les sous-classes redéfinir certaines étapes ?

**Solution** : Template Method définit la structure d'un algorithme dans la classe de base.

### Structure du Template Method

```python
from abc import ABC, abstractmethod
from datetime import datetime


# === Abstract Class ===

class ReportGenerator(ABC):
    """
    Template Method pour générer des rapports
    """
    
    def generate_report(self):
        """
        Template Method - définit le squelette de l'algorithme
        Cette méthode ne doit PAS être redéfinie
        """
        print("=" * 70)
        self._generate_header()
        self._generate_content()
        self._generate_statistics()
        self._generate_footer()
        print("=" * 70)
    
    # Hook methods (peuvent être surchargées)
    def _generate_header(self):
        """Génère l'en-tête (hook)"""
        print(f"RAPPORT GÉNÉRÉ LE {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("-" * 70)
    
    # Abstract methods (DOIVENT être implémentées)
    @abstractmethod
    def _generate_content(self):
        """Génère le contenu principal (abstract)"""
        pass
    
    @abstractmethod
    def _generate_statistics(self):
        """Génère les statistiques (abstract)"""
        pass
    
    # Hook methods (optionnel)
    def _generate_footer(self):
        """Génère le pied de page (hook)"""
        print("-" * 70)
        print("Université des Antilles - Système de Gestion")


# === Concrete Classes ===

class StudentReport(ReportGenerator):
    """Rapport pour un étudiant"""
    
    def __init__(self, student_name, student_id, grades):
        self.student_name = student_name
        self.student_id = student_id
        self.grades = grades
    
    def _generate_content(self):
        """Implémentation du contenu pour étudiant"""
        print(f"RAPPORT ÉTUDIANT")
        print(f"Nom: {self.student_name}")
        print(f"ID: {self.student_id}")
        print(f"\nNotes:")
        for course, grade in self.grades.items():
            print(f"  - {course}: {grade}/20")
    
    def _generate_statistics(self):
        """Statistiques pour l'étudiant"""
        if self.grades:
            avg = sum(self.grades.values()) / len(self.grades)
            max_grade = max(self.grades.values())
            min_grade = min(self.grades.values())
            
            print(f"\nSTATISTIQUES:")
            print(f"  Moyenne: {avg:.2f}/20")
            print(f"  Meilleure note: {max_grade}/20")
            print(f"  Note la plus basse: {min_grade}/20")


class CourseReport(ReportGenerator):
    """Rapport pour un cours"""
    
    def __init__(self, course_name, instructor, enrollments):
        self.course_name = course_name
        self.instructor = instructor
        self.enrollments = enrollments
    
    def _generate_header(self):
        """En-tête personnalisé pour cours"""
        super()._generate_header()
        print(f"TYPE: Rapport de Cours")
        print("-" * 70)
    
    def _generate_content(self):
        """Contenu pour cours"""
        print(f"COURS: {self.course_name}")
        print(f"Enseignant: {self.instructor}")
        print(f"\nÉtudiants inscrits: {len(self.enrollments)}")
        print("Liste:")
        for i, student in enumerate(self.enrollments, 1):
            print(f"  {i}. {student}")
    
    def _generate_statistics(self):
        """Statistiques pour cours"""
        print(f"\nSTATISTIQUES:")
        print(f"  Total inscriptions: {len(self.enrollments)}")
        print(f"  Taux de remplissage: {(len(self.enrollments)/50)*100:.1f}%")


class DepartmentReport(ReportGenerator):
    """Rapport pour un département"""
    
    def __init__(self, dept_name, courses, total_students):
        self.dept_name = dept_name
        self.courses = courses
        self.total_students = total_students
    
    def _generate_header(self):
        """En-tête personnalisé pour département"""
        super()._generate_header()
        print(f"TYPE: Rapport de Département")
        print(f"DÉPARTEMENT: {self.dept_name}")
        print("-" * 70)
    
    def _generate_content(self):
        """Contenu pour département"""
        print(f"Cours offerts: {len(self.courses)}")
        for course in self.courses:
            print(f"  • {course}")
    
    def _generate_statistics(self):
        """Statistiques pour département"""
        print(f"\nSTATISTIQUES:")
        print(f"  Total étudiants: {self.total_students}")
        print(f"  Nombre de cours: {len(self.courses)}")
        print(f"  Moyenne étudiants/cours: {self.total_students/len(self.courses):.1f}")
    
    def _generate_footer(self):
        """Pied de page personnalisé"""
        super()._generate_footer()
        print(f"Contact: {self.dept_name.lower()}@univ-antilles.fr")


# === Utilisation ===

if __name__ == "__main__":
    # Rapport étudiant
    print("\n### RAPPORT ÉTUDIANT ###\n")
    student_report = StudentReport(
        student_name="Marie Lafleur",
        student_id="20231234",
        grades={
            "POO": 15,
            "Web Dev": 16,
            "Mobile": 14,
            "Base de Données": 17
        }
    )
    student_report.generate_report()
    
    # Rapport cours
    print("\n\n### RAPPORT COURS ###\n")
    course_report = CourseReport(
        course_name="Programmation Orientée Objet",
        instructor="Prof. Roor",
        enrollments=[
            "Marie Lafleur", "Jean Martin", "Sophie Bernard",
            "Paul Dubois", "Alice Moreau", "Lucas Petit"
        ]
    )
    course_report.generate_report()
    
    # Rapport département
    print("\n\n### RAPPORT DÉPARTEMENT ###\n")
    dept_report = DepartmentReport(
        dept_name="Informatique",
        courses=["POO", "Web Dev", "Mobile", "IA", "Réseaux", "Sécurité"],
        total_students=145
    )
    dept_report.generate_report()
```

### ⚠️ Quand utiliser Template Method ?

**✅ Utilisez-le pour :**
- Algorithmes avec structure commune mais étapes variables
- Éviter la duplication de code
- Framework hooks (Django views, unittest)
- Workflows standardisés

**❌ Évitez-le pour :**
- Algorithmes complètement différents
- Quand la flexibilité est plus importante que la structure

---

## 7. Applications Pratiques pour vos Projets

### 7.1 Projet E-commerce Campus

**Patterns recommandés :**

```python
# Observer: Notifications sur commande
class Order(Subject):
    def place_order(self):
        self.notify("ORDER_PLACED", order_data)
        # → EmailNotifier, InventoryManager, AnalyticsCollector

# Strategy: Méthodes de paiement
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

# Command: Historique de commandes avec undo
class PlaceOrderCommand(Command):
    def execute(self): ...
    def undo(self): ...

# State: États de commande (pending, paid, shipped, delivered)
class OrderStateMachine:
    def transition_to_shipped(self): ...
```

### 7.2 Projet Plateforme de Cours

**Patterns recommandés :**

```python
# Observer: Notifications d'activité
class Course(Subject):
    def publish_new_lesson(self):
        self.notify("NEW_LESSON", lesson_data)
        # → Student notifications, Progress tracker

# Strategy: Méthodes d'évaluation
class Assessment:
    def __init__(self, grading_strategy):
        self.strategy = grading_strategy
    
    # Quiz, assignments, projects = différentes stratégies

# Template Method: Génération de certificats
class CertificateGenerator(ABC):
    def generate(self):
        self._add_header()
        self._add_content()  # Varie selon le type
        self._add_signature()

# State: Progression étudiant (enrolled, in_progress, completed)
```

### 7.3 Projet Gestion de Bibliothèque

**Patterns recommandés :**

```python
# Command: Emprunts/Retours avec historique
class BorrowBookCommand(Command):
    def execute(self): ...
    def undo(self): ...  # Annuler un emprunt

# State: États du livre (available, borrowed, reserved, lost)
class BookState(ABC):
    def borrow(self, book, user): ...

# Observer: Notifications de disponibilité
class Book(Subject):
    def return_book(self):
        self.notify("BOOK_AVAILABLE")
        # → Notify users in waiting list
```

### 7.4 Projet Réseau Social Campus

**Patterns recommandés :**

```python
# Observer: Système de follow/notifications
class User(Subject):
    def post_content(self, content):
        self.notify("NEW_POST", content)
        # → Followers get notified

# Strategy: Algorithmes de feed
class FeedGenerator:
    def __init__(self, strategy: FeedStrategy):
        self.strategy = strategy
    # Chronological, Popular, Recommended = différentes stratégies

# Command: Posts avec edit history
class CreatePostCommand(Command):
    def execute(self): ...
    def undo(self): ...
```

---

## 8. Patterns Combinés - Architecture Complète

Voici comment combiner plusieurs patterns dans une application réelle :

```python
# === Application de Gestion de Projet Étudiant ===

# Singleton: Configuration globale
@singleton
class AppConfig:
    pass

# Factory: Création de différents types de projets
class ProjectFactory:
    @staticmethod
    def create_project(project_type):
        # Returns WebProject, MobileProject, ResearchProject
        pass

# Builder: Construction de projets complexes
class ProjectBuilder:
    def set_team(self, members): ...
    def add_milestone(self, milestone): ...
    def build(self): ...

# Observer: Notifications sur événements projet
class Project(Subject):
    def complete_milestone(self):
        self.notify("MILESTONE_COMPLETED")

# Strategy: Différentes méthodes d'évaluation
class Evaluator:
    def __init__(self, strategy: EvaluationStrategy):
        self.strategy = strategy

# Command: Actions avec undo/redo
class UpdateProjectCommand(Command):
    pass

# State: États du projet
class ProjectState:
    # PLANNING, ACTIVE, REVIEW, COMPLETED
    pass

# Decorator: Ajout de fonctionnalités
class LoggedProject(ProjectDecorator):
    pass

# Facade: Interface simplifiée
class ProjectManagementFacade:
    def create_and_setup_project(self, params):
        # Utilise Factory, Builder, configure Observers, etc.
        pass

# Template Method: Rapports standardisés
class ProjectReport(ABC):
    def generate(self):
        self._header()
        self._content()  # Varie
        self._footer()
```

---

## 9. Récapitulatif Final - Tous les Patterns

### Patterns de Création

| Pattern | Objectif | Exemple Campus |
|---------|----------|----------------|
| **Singleton** | Une instance unique | Configuration, DB connection |
| **Factory Method** | Déléguer création | Types d'événements |
| **Abstract Factory** | Familles d'objets | Thèmes UI |
| **Builder** | Construction complexe | Profil étudiant |
| **Prototype** | Clonage | Templates documents |

### Patterns de Structure

| Pattern | Objectif | Exemple Campus |
|---------|----------|----------------|
| **Adapter** | Compatibilité | Intégration paiement |
| **Decorator** | Ajout dynamique | Notifications enrichies |
| **Facade** | Simplification | Processus inscription |
| **Composite** | Arbre d'objets | Structure cours/modules |
| **Proxy** | Contrôle d'accès | Lazy loading |
| **Bridge** | Découpler abstraction | Multi-plateforme |

### Patterns Comportementaux

| Pattern | Objectif | Exemple Campus |
|---------|----------|----------------|
| **Observer** | Notifications 1-N | Événements campus |
| **Strategy** | Algorithmes interchangeables | Méthodes notation |
| **Command** | Encapsuler requêtes | Undo/Redo tâches |
| **State** | Comportement selon état | Réservation salles |
| **Template Method** | Squelette algorithme | Génération rapports |
| **Iterator** | Parcours collections | Liste étudiants |
| **Mediator** | Communication centralisée | Chat groupe |
| **Chain of Responsibility** | Chaîne de traitements | Validation formulaire |

---

## 10. Principes SOLID et Design Patterns

Les design patterns appliquent les principes SOLID :

### S - Single Responsibility Principle
```python
# Chaque pattern a une responsabilité claire
class EmailNotifier(Observer):  # Seulement les emails
class PushNotifier(Observer):   # Seulement les push
```

### O - Open/Closed Principle
```python
# Ouvert à l'extension, fermé à la modification
# Ajouter un nouveau strategy sans modifier le code existant
class NewGradingStrategy(GradingStrategy):
    def calculate_grade(self, grades):
        # Nouvelle implémentation
        pass
```

### L - Liskov Substitution Principle
```python
# Les sous-classes sont interchangeables
def process_payment(processor: PaymentProcessor):
    processor.process()  # Fonctionne avec toute stratégie
```

### I - Interface Segregation Principle
```python
# Interfaces spécifiques plutôt qu'une grosse interface
class Printable(ABC):
    def print(self): pass

class Saveable(ABC):
    def save(self): pass
```

### D - Dependency Inversion Principle
```python
# Dépendre des abstractions, pas des implémentations
class ReportGenerator:
    def __init__(self, formatter: ReportFormatter):  # Abstraction
        self.formatter = formatter
```

---

## 11. Anti-Patterns à Éviter

### 11.1 Pattern Overload
```python
# ❌ Trop de patterns pour rien
factory = SingletonFactoryBuilderAdapter()  # WTF?
```

### 11.2 God Class avec Patterns
```python
# ❌ Utiliser des patterns ne résout pas une mauvaise architecture
class ApplicationManager(Subject, Observer, Command, Strategy):
    # 5000 lignes de code...
    pass
```

### 11.3 Premature Pattern Application
```python
# ❌ Ajouter des patterns "au cas où"
# Commencez simple, refactorez vers des patterns quand nécessaire
```

### 11.4 Copy-Paste Pattern
```python
# ❌ Copier un pattern sans comprendre
# Adaptez le pattern à votre contexte
```

---

## 12. Exercices de Synthèse

### Exercice 1 : Système de Messagerie Multi-Canal

Créez un système de messagerie qui :
- Support plusieurs canaux (Email, SMS, Push, Slack)
- Permet d'envoyer des messages avec retry et logging
- Garde un historique avec undo/redo
- Notifie des observateurs quand un message est envoyé

**Patterns à utiliser :** Observer, Decorator, Command, Strategy

### Exercice 2 : Workflow de Validation de Projet

Créez un workflow pour valider des projets étudiants :
- États : Draft, Submitted, UnderReview, Approved, Rejected
- Différentes méthodes d'évaluation selon le type de projet
- Notifications aux parties prenantes
- Génération de rapports standardisés

**Patterns à utiliser :** State, Strategy, Observer, Template Method

### Exercice 3 : Système de Réservation Complexe

Créez un système de réservation de ressources :
- Différents types de ressources (salles, équipement, véhicules)
- Construction de réservations complexes
- États de réservation
- Historique avec undo/redo

**Patterns à utiliser :** Factory, Builder, State, Command

---

## 13. Checklist pour Choisir un Pattern

**Questions à se poser :**

1. **Création d'objets ?**
   - Besoin d'une seule instance ? → **Singleton**
   - Plusieurs types à créer ? → **Factory Method**
   - Familles d'objets liés ? → **Abstract Factory**
   - Construction complexe ? → **Builder**
   - Copie d'objets ? → **Prototype**

2. **Structure et composition ?**
   - Interfaces incompatibles ? → **Adapter**
   - Ajouter des responsabilités ? → **Decorator**
   - Simplifier une interface ? → **Facade**

3. **Comportement et communication ?**
   - Notifier plusieurs objets ? → **Observer**
   - Algorithmes interchangeables ? → **Strategy**
   - Undo/Redo nécessaire ? → **Command**
   - Comportement selon état ? → **State**
   - Squelette commun ? → **Template Method**

---

## 14. Ressources pour Aller Plus Loin

### Livres
- **"Design Patterns"** (Gang of Four) - La référence
- **"Head First Design Patterns"** - Approche visuelle
- **"Refactoring to Patterns"** - Quand et comment refactorer

### Sites Web
- **Refactoring.Guru** - Excellentes illustrations et exemples
- **SourceMaking.com** - Patterns + Anti-patterns
- **Python Patterns** - Spécifique Python

### Projets Open Source
- **Django** - Template Method, Observer, Strategy
- **Flask** - Decorator, Factory
- **Requests** - Adapter, Builder

### Pratique
- **Code Katas** sur design patterns
- **Refactoring.guru exercises**
- **Leetcode Design Questions**

---

## 15. Conclusion du CM4

### Ce que nous avons appris

**Partie 1 :** Fondamentaux, Singleton, Factory Method

**Partie 2 :** Builder, Prototype, Abstract Factory, Adapter, Decorator, Facade

**Partie 3 :** Observer, Strategy, Command, State, Template Method

### Compétences acquises

✓ Reconnaître les problèmes que chaque pattern résout  
✓ Implémenter les patterns en Python  
✓ Choisir le bon pattern pour une situation  
✓ Combiner plusieurs patterns  
✓ Éviter les anti-patterns  
✓ Appliquer les principes SOLID  

### Message final

**Les design patterns ne sont pas :**
- Une obligation
- Une solution miracle
- À utiliser systématiquement

**Les design patterns sont :**
- Un vocabulaire commun entre développeurs
- Des solutions éprouvées à des problèmes récurrents
- Un outil pour améliorer la qualité du code
- Un moyen de faciliter la maintenance

**Règle d'or :** Commencez simple, refactorez vers des patterns quand le besoin se fait sentir.

---

## 16. Prochaines Étapes

**Dans vos projets :**
- Identifiez où appliquer les patterns
- Commencez par Observer et Strategy (les plus utiles)
- Documentez vos choix de patterns
- Revue de code en groupe sur l'utilisation des patterns

---

## 17. Quiz Final

**Questions de réflexion :**

1. Quel pattern utiliseriez-vous pour un système de notifications multi-canal ?
2. Comment implémenteriez-vous un système d'undo/redo ?
3. Quelle est la différence entre Strategy et State ?
4. Quand utiliser Factory Method vs Abstract Factory ?
5. Comment éviter le "pattern overuse" ?

**Mini-projet :**
Concevez l'architecture d'une application de votre choix en identifiant au moins 5 patterns différents et justifiez chaque choix.

---

## Questions ?

Merci pour votre attention !

**Contact :** roland.ratenan@nasdy.fr  
**Office Hours :** 9h-17h

**N'oubliez pas :** Le meilleur pattern est celui qui rend votre code plus maintenable et compréhensible !

---

*Fin du CM4 - Design Patterns*