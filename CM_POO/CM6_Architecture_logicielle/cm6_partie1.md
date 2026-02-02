# CM6 - Architecture Logicielle (Partie 1)
## Programmation Orientée Objet - Organisation à Grande Échelle

---

## Introduction

## 1. Qu'est-ce que l'Architecture Logicielle ?

### Définition

> **L'architecture logicielle est l'organisation fondamentale d'un système, incarnée dans ses composants, leurs relations entre eux et avec l'environnement, et les principes guidant sa conception et son évolution.**
> 
> *— IEEE 1471*

**En termes simples :** C'est la **structure de haut niveau** qui définit comment organiser le code d'une application.

### Analogie : Architecture de bâtiment

```
🏗️ Architecture d'un Bâtiment          💻 Architecture Logicielle
=====================================  ====================================
Fondations                             Infrastructure (Base de données, etc.)
Structure portante                     Modules principaux (Domain, Services)
Étages séparés                         Couches (Presentation, Business, Data)
Plomberie/Électricité                  Services transversaux (Logging, Auth)
Pièces                                 Composants/Classes
```

### Pourquoi l'architecture est importante ?

**Sans architecture claire :**
```
❌ Code spaghetti
❌ Dépendances circulaires
❌ Difficile à tester
❌ Impossible à faire évoluer
❌ Bugs en cascade
```

**Avec une bonne architecture :**
```
✅ Code organisé et compréhensible
✅ Séparation des responsabilités
✅ Facile à tester
✅ Évolutivité
✅ Maintenance simplifiée
```

---

## 2. Architecture en Couches (Layered Architecture)

### Concept de base

L'architecture en couches organise le code en **strates horizontales**, chaque couche ayant une responsabilité spécifique.

**Règle d'or :** Une couche ne peut dépendre que des couches **inférieures**.

### Structure classique à 3 couches

```
┌─────────────────────────────────────┐
│   PRESENTATION LAYER (Interface)    │  ← Utilisateur
│   - CLI, Web UI, API REST           │
├─────────────────────────────────────┤
│   BUSINESS LAYER (Logique Métier)   │
│   - Règles métier, Calculs          │
├─────────────────────────────────────┤
│   DATA ACCESS LAYER (Données)       │  ← Base de données
│   - Repositories, ORM, Queries      │
└─────────────────────────────────────┘
```

### Implémentation d'une architecture à 3 couches

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta


# ============================================================================
# COUCHE 3 : DATA ACCESS LAYER (Accès aux données)
# ============================================================================

class Student:
    """Entité Student (représente une ligne en base)"""
    
    def __init__(self, student_id: str, name: str, email: str, enrollment_date: datetime):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.enrollment_date = enrollment_date
        self.grades: List[float] = []
    
    def __repr__(self):
        return f"Student({self.student_id}, {self.name})"


class StudentRepository:
    """
    Repository : Responsable de la persistance des étudiants
    Couche DATA ACCESS
    """
    
    def __init__(self):
        # Simulation avec un dictionnaire (en réalité : base de données)
        self._students: dict[str, Student] = {}
    
    def save(self, student: Student) -> None:
        """Sauvegarde un étudiant"""
        self._students[student.student_id] = student
        print(f"[DATA] Étudiant {student.student_id} sauvegardé")
    
    def find_by_id(self, student_id: str) -> Optional[Student]:
        """Récupère un étudiant par ID"""
        student = self._students.get(student_id)
        if student:
            print(f"[DATA] Étudiant {student_id} récupéré")
        return student
    
    def find_all(self) -> List[Student]:
        """Récupère tous les étudiants"""
        print(f"[DATA] Récupération de {len(self._students)} étudiants")
        return list(self._students.values())
    
    def delete(self, student_id: str) -> bool:
        """Supprime un étudiant"""
        if student_id in self._students:
            del self._students[student_id]
            print(f"[DATA] Étudiant {student_id} supprimé")
            return True
        return False


# ============================================================================
# COUCHE 2 : BUSINESS LAYER (Logique métier)
# ============================================================================

class StudentService:
    """
    Service : Contient la logique métier
    Couche BUSINESS
    """
    
    def __init__(self, repository: StudentRepository):
        self.repository = repository
    
    def enroll_student(self, student_id: str, name: str, email: str) -> Student:
        """
        Inscrit un nouvel étudiant
        RÈGLE MÉTIER : ID doit être unique
        """
        print(f"\n[BUSINESS] Traitement inscription de {name}")
        
        # Vérifier si l'étudiant existe déjà
        existing = self.repository.find_by_id(student_id)
        if existing:
            raise ValueError(f"Étudiant {student_id} déjà inscrit")
        
        # Créer l'étudiant
        student = Student(
            student_id=student_id,
            name=name,
            email=email,
            enrollment_date=datetime.now()
        )
        
        # Sauvegarder
        self.repository.save(student)
        
        print(f"[BUSINESS] ✓ Inscription réussie")
        return student
    
    def add_grade(self, student_id: str, grade: float) -> None:
        """
        Ajoute une note à un étudiant
        RÈGLE MÉTIER : Note entre 0 et 20
        """
        print(f"\n[BUSINESS] Ajout note {grade} pour {student_id}")
        
        # Validation métier
        if not 0 <= grade <= 20:
            raise ValueError("La note doit être entre 0 et 20")
        
        # Récupérer l'étudiant
        student = self.repository.find_by_id(student_id)
        if not student:
            raise ValueError(f"Étudiant {student_id} non trouvé")
        
        # Ajouter la note
        student.grades.append(grade)
        
        # Sauvegarder
        self.repository.save(student)
        
        print(f"[BUSINESS] ✓ Note ajoutée")
    
    def calculate_average(self, student_id: str) -> float:
        """
        Calcule la moyenne d'un étudiant
        LOGIQUE MÉTIER
        """
        print(f"\n[BUSINESS] Calcul moyenne pour {student_id}")
        
        student = self.repository.find_by_id(student_id)
        if not student:
            raise ValueError(f"Étudiant {student_id} non trouvé")
        
        if not student.grades:
            return 0.0
        
        average = sum(student.grades) / len(student.grades)
        print(f"[BUSINESS] Moyenne calculée: {average:.2f}")
        return average
    
    def is_passing(self, student_id: str) -> bool:
        """
        Vérifie si l'étudiant a la moyenne
        RÈGLE MÉTIER : Moyenne >= 10
        """
        average = self.calculate_average(student_id)
        return average >= 10.0
    
    def get_student_status(self, student_id: str) -> str:
        """
        Retourne le statut de l'étudiant
        LOGIQUE MÉTIER : Nouveau, En cours, Réussite, Échec
        """
        student = self.repository.find_by_id(student_id)
        if not student:
            return "INCONNU"
        
        if not student.grades:
            return "NOUVEAU"
        
        if len(student.grades) < 4:
            return "EN_COURS"
        
        return "RÉUSSITE" if self.is_passing(student_id) else "ÉCHEC"


# ============================================================================
# COUCHE 1 : PRESENTATION LAYER (Interface utilisateur)
# ============================================================================

class StudentController:
    """
    Controller : Gère les interactions utilisateur
    Couche PRESENTATION
    """
    
    def __init__(self, service: StudentService):
        self.service = service
    
    def display_menu(self):
        """Affiche le menu principal"""
        print("\n" + "=" * 60)
        print("SYSTÈME DE GESTION DES ÉTUDIANTS")
        print("=" * 60)
        print("1. Inscrire un étudiant")
        print("2. Ajouter une note")
        print("3. Voir la moyenne")
        print("4. Voir le statut")
        print("5. Quitter")
        print("=" * 60)
    
    def enroll_student_command(self):
        """Commande : Inscrire un étudiant"""
        print("\n--- Inscription d'un étudiant ---")
        student_id = input("ID étudiant : ")
        name = input("Nom : ")
        email = input("Email : ")
        
        try:
            student = self.service.enroll_student(student_id, name, email)
            print(f"\n✓ Étudiant {student.name} inscrit avec succès!")
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
    
    def add_grade_command(self):
        """Commande : Ajouter une note"""
        print("\n--- Ajout d'une note ---")
        student_id = input("ID étudiant : ")
        grade_str = input("Note (0-20) : ")
        
        try:
            grade = float(grade_str)
            self.service.add_grade(student_id, grade)
            print(f"\n✓ Note {grade} ajoutée avec succès!")
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
    
    def view_average_command(self):
        """Commande : Voir la moyenne"""
        print("\n--- Moyenne d'un étudiant ---")
        student_id = input("ID étudiant : ")
        
        try:
            average = self.service.calculate_average(student_id)
            is_passing = self.service.is_passing(student_id)
            
            print(f"\n📊 Moyenne : {average:.2f}/20")
            print(f"📋 Statut : {'✓ RÉUSSITE' if is_passing else '✗ ÉCHEC'}")
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
    
    def view_status_command(self):
        """Commande : Voir le statut"""
        print("\n--- Statut d'un étudiant ---")
        student_id = input("ID étudiant : ")
        
        try:
            status = self.service.get_student_status(student_id)
            print(f"\n📋 Statut : {status}")
        except ValueError as e:
            print(f"\n✗ Erreur : {e}")
    
    def run(self):
        """Lance l'application"""
        while True:
            self.display_menu()
            choice = input("\nVotre choix : ")
            
            if choice == "1":
                self.enroll_student_command()
            elif choice == "2":
                self.add_grade_command()
            elif choice == "3":
                self.view_average_command()
            elif choice == "4":
                self.view_status_command()
            elif choice == "5":
                print("\nAu revoir!")
                break
            else:
                print("\n✗ Choix invalide")


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ARCHITECTURE EN COUCHES - DÉMONSTRATION")
    print("=" * 70)
    
    # Construction de l'application (injection de dépendances)
    repository = StudentRepository()      # Couche 3 : Data
    service = StudentService(repository)  # Couche 2 : Business
    controller = StudentController(service)  # Couche 1 : Presentation
    
    # Version automatisée pour la démo (au lieu de run())
    print("\n--- DÉMONSTRATION AUTOMATIQUE ---\n")
    
    # Inscrire des étudiants
    student1 = service.enroll_student("20231001", "Marie Lafleur", "marie@ua.fr")
    student2 = service.enroll_student("20231002", "Jean Martin", "jean@ua.fr")
    
    # Ajouter des notes
    service.add_grade("20231001", 15)
    service.add_grade("20231001", 16)
    service.add_grade("20231001", 14)
    service.add_grade("20231001", 17)
    
    service.add_grade("20231002", 8)
    service.add_grade("20231002", 9)
    service.add_grade("20231002", 7)
    service.add_grade("20231002", 10)
    
    # Afficher les moyennes
    print("\n" + "=" * 70)
    print("RÉSULTATS")
    print("=" * 70)
    
    for student_id in ["20231001", "20231002"]:
        average = service.calculate_average(student_id)
        status = service.get_student_status(student_id)
        is_passing = service.is_passing(student_id)
        
        print(f"\nÉtudiant {student_id}:")
        print(f"  Moyenne: {average:.2f}/20")
        print(f"  Statut: {status}")
        print(f"  Résultat: {'✓ RÉUSSITE' if is_passing else '✗ ÉCHEC'}")
    
    print("\n" + "=" * 70)
    print("AVANTAGES DE L'ARCHITECTURE EN COUCHES:")
    print("- Séparation claire des responsabilités")
    print("- Couche Presentation peut changer (CLI → Web) sans toucher Business")
    print("- Couche Data peut changer (Dict → SQLite) sans toucher Business")
    print("- Logique métier isolée et testable")
    print("=" * 70)
```

### Avantages et Inconvénients

**✅ Avantages :**
- Simple à comprendre et implémenter
- Séparation claire des responsabilités
- Chaque couche peut évoluer indépendamment
- Testabilité par couche

**❌ Inconvénients :**
- Peut devenir rigide sur de gros projets
- Risque de "couches anémiques" (logique métier dispersée)
- Dépendances en cascade (Presentation → Business → Data)

---

## 3. Architecture MVC (Model-View-Controller)

### Concept

MVC sépare l'application en 3 composants :

```
┌──────────┐
│   VIEW   │ ← Affichage
└─────┬────┘
      │
      ↓
┌──────────┐      ┌───────────┐
│CONTROLLER│ ←──→ │   MODEL   │
└──────────┘      └───────────┘
   Logique         Données + Règles
```

**Flux typique :**
1. **Utilisateur** → Interaction avec la **View**
2. **View** → Appelle le **Controller**
3. **Controller** → Modifie le **Model**
4. **Model** → Notifie la **View** (Observer pattern!)
5. **View** → Se met à jour

### Implémentation MVC

```python
from abc import ABC, abstractmethod
from typing import List, Callable


# ============================================================================
# MODEL (Données + Logique Métier)
# ============================================================================

class TodoItem:
    """Un élément de la liste de tâches"""
    
    def __init__(self, task_id: int, description: str):
        self.task_id = task_id
        self.description = description
        self.completed = False
    
    def toggle_complete(self):
        """Bascule l'état de complétion"""
        self.completed = not self.completed
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.task_id}. {self.description}"


class TodoModel:
    """
    Model : Gère les données et la logique métier
    Implémente le pattern Observer pour notifier la View
    """
    
    def __init__(self):
        self._todos: List[TodoItem] = []
        self._next_id = 1
        self._observers: List[Callable] = []
    
    # Pattern Observer
    def attach(self, observer: Callable):
        """Attache un observateur (la View)"""
        self._observers.append(observer)
    
    def notify(self):
        """Notifie tous les observateurs"""
        for observer in self._observers:
            observer()
    
    # Opérations métier
    def add_todo(self, description: str) -> TodoItem:
        """Ajoute une tâche"""
        todo = TodoItem(self._next_id, description)
        self._todos.append(todo)
        self._next_id += 1
        self.notify()  # Notifier la View
        return todo
    
    def toggle_todo(self, task_id: int) -> bool:
        """Bascule l'état d'une tâche"""
        for todo in self._todos:
            if todo.task_id == task_id:
                todo.toggle_complete()
                self.notify()  # Notifier la View
                return True
        return False
    
    def remove_todo(self, task_id: int) -> bool:
        """Supprime une tâche"""
        for i, todo in enumerate(self._todos):
            if todo.task_id == task_id:
                del self._todos[i]
                self.notify()  # Notifier la View
                return True
        return False
    
    def get_all_todos(self) -> List[TodoItem]:
        """Récupère toutes les tâches"""
        return self._todos.copy()
    
    def get_stats(self) -> dict:
        """Retourne des statistiques"""
        total = len(self._todos)
        completed = sum(1 for t in self._todos if t.completed)
        pending = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }


# ============================================================================
# VIEW (Interface Utilisateur)
# ============================================================================

class TodoView:
    """
    View : Responsable de l'affichage
    S'enregistre comme observateur du Model
    """
    
    def __init__(self, model: TodoModel):
        self.model = model
        # S'enregistrer comme observateur
        self.model.attach(self.render)
    
    def render(self):
        """Affiche l'état actuel (appelé automatiquement par le Model)"""
        print("\n" + "=" * 60)
        print("📝 LISTE DE TÂCHES")
        print("=" * 60)
        
        todos = self.model.get_all_todos()
        
        if not todos:
            print("Aucune tâche")
        else:
            for todo in todos:
                print(f"  {todo}")
        
        # Statistiques
        stats = self.model.get_stats()
        print("\n" + "-" * 60)
        print(f"Total: {stats['total']} | "
              f"Complétées: {stats['completed']} | "
              f"En cours: {stats['pending']} | "
              f"Taux: {stats['completion_rate']:.0f}%")
        print("=" * 60)
    
    def display_menu(self):
        """Affiche le menu"""
        print("\nActions :")
        print("  1. Ajouter une tâche")
        print("  2. Compléter/Décompléter une tâche")
        print("  3. Supprimer une tâche")
        print("  4. Quitter")
    
    def show_message(self, message: str):
        """Affiche un message"""
        print(f"\n💬 {message}")


# ============================================================================
# CONTROLLER (Logique de contrôle)
# ============================================================================

class TodoController:
    """
    Controller : Gère les interactions utilisateur
    Modifie le Model en fonction des actions
    """
    
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view
    
    def add_todo(self, description: str):
        """Action : Ajouter une tâche"""
        if not description.strip():
            self.view.show_message("⚠️  Description vide")
            return
        
        todo = self.model.add_todo(description)
        self.view.show_message(f"✓ Tâche '{description}' ajoutée (ID: {todo.task_id})")
    
    def toggle_todo(self, task_id: int):
        """Action : Basculer l'état d'une tâche"""
        if self.model.toggle_todo(task_id):
            self.view.show_message(f"✓ Tâche {task_id} mise à jour")
        else:
            self.view.show_message(f"⚠️  Tâche {task_id} introuvable")
    
    def remove_todo(self, task_id: int):
        """Action : Supprimer une tâche"""
        if self.model.remove_todo(task_id):
            self.view.show_message(f"✓ Tâche {task_id} supprimée")
        else:
            self.view.show_message(f"⚠️  Tâche {task_id} introuvable")
    
    def run(self):
        """Lance l'application"""
        # Affichage initial
        self.view.render()
        
        while True:
            self.view.display_menu()
            choice = input("\nChoix : ").strip()
            
            if choice == "1":
                description = input("Description de la tâche : ")
                self.add_todo(description)
            
            elif choice == "2":
                task_id_str = input("ID de la tâche : ")
                try:
                    task_id = int(task_id_str)
                    self.toggle_todo(task_id)
                except ValueError:
                    self.view.show_message("⚠️  ID invalide")
            
            elif choice == "3":
                task_id_str = input("ID de la tâche : ")
                try:
                    task_id = int(task_id_str)
                    self.remove_todo(task_id)
                except ValueError:
                    self.view.show_message("⚠️  ID invalide")
            
            elif choice == "4":
                self.view.show_message("Au revoir!")
                break
            
            else:
                self.view.show_message("⚠️  Choix invalide")


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ARCHITECTURE MVC - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer les composants MVC
    model = TodoModel()
    view = TodoView(model)
    controller = TodoController(model, view)
    
    # Version automatisée pour la démo
    print("\n--- DÉMONSTRATION AUTOMATIQUE ---")
    
    # Ajouter des tâches
    controller.add_todo("Réviser le cours de POO")
    controller.add_todo("Faire les exercices SOLID")
    controller.add_todo("Préparer le projet final")
    
    # Compléter une tâche
    controller.toggle_todo(1)
    
    # Ajouter une autre tâche
    controller.add_todo("Lire la documentation Clean Architecture")
    
    # Compléter une autre tâche
    controller.toggle_todo(2)
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU MVC:")
    print("- Séparation claire Model/View/Controller")
    print("- Model notifie automatiquement la View (Observer)")
    print("- Plusieurs Views possibles pour le même Model")
    print("- Testabilité : chaque composant est indépendant")
    print("=" * 70)
    
    # Pour lancer en mode interactif, décommenter :
    # controller.run()
```

### Variations de MVC

**MVP (Model-View-Presenter)**
- Presenter remplace Controller
- Plus de logique dans le Presenter
- View complètement passive

**MVVM (Model-View-ViewModel)**
- ViewModel expose les données pour la View
- Data Binding automatique
- Populaire dans les frameworks modernes (Angular, Vue, WPF)

---

## 4. Clean Architecture (Uncle Bob)

### Principe fondamental

> **Les règles métier ne doivent dépendre de RIEN d'autre.**
>
> *— Robert C. Martin*

### Les cercles concentriques

```
┌─────────────────────────────────────────────────┐
│  Frameworks & Drivers                           │ ← Extérieur
│  (Web, DB, UI, Devices, External Interfaces)    │
├─────────────────────────────────────────────────┤
│  Interface Adapters                             │
│  (Controllers, Gateways, Presenters)            │
├─────────────────────────────────────────────────┤
│  Application Business Rules                     │
│  (Use Cases / Interactors)                      │
├─────────────────────────────────────────────────┤
│  Enterprise Business Rules                      │ ← Intérieur
│  (Entities / Domain Models)                     │
└─────────────────────────────────────────────────┘

Règle : Les dépendances pointent TOUJOURS vers l'intérieur
```

### Principe de la Dependency Rule

**❌ Interdit :**
```python
# Entity (centre) dépend de quelque chose d'externe
class Student:
    def save(self):
        import sqlite3  # ❌ Entity dépend de la DB
```

**✅ Correct :**
```python
# Entity pure (aucune dépendance)
class Student:
    def __init__(self, name: str):
        self.name = name

# Repository (couche externe) dépend de l'Entity
class StudentRepository:
    def save(self, student: Student):  # ✅ Dépendance vers l'intérieur
        import sqlite3
        # ...
```

### Implémentation de Clean Architecture

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# COUCHE 1 : ENTITIES (Enterprise Business Rules)
# ============================================================================

@dataclass
class Course:
    """
    Entity : Règles métier pures
    Aucune dépendance externe !
    """
    course_id: str
    name: str
    instructor: str
    max_students: int
    enrolled_students: List[str]
    
    def can_enroll(self) -> bool:
        """Règle métier : Vérifier si on peut encore inscrire"""
        return len(self.enrolled_students) < self.max_students
    
    def enroll_student(self, student_id: str) -> bool:
        """Règle métier : Inscrire un étudiant"""
        if not self.can_enroll():
            return False
        
        if student_id in self.enrolled_students:
            return False  # Déjà inscrit
        
        self.enrolled_students.append(student_id)
        return True
    
    def withdraw_student(self, student_id: str) -> bool:
        """Règle métier : Retirer un étudiant"""
        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id)
            return True
        return False
    
    def get_enrollment_rate(self) -> float:
        """Calcul métier : Taux de remplissage"""
        return (len(self.enrolled_students) / self.max_students) * 100


# ============================================================================
# COUCHE 2 : USE CASES (Application Business Rules)
# ============================================================================

# --- Interfaces (Ports) ---

class CourseRepository(ABC):
    """Port : Interface pour la persistance"""
    
    @abstractmethod
    def save(self, course: Course) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, course_id: str) -> Optional[Course]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Course]:
        pass


class NotificationService(ABC):
    """Port : Interface pour les notifications"""
    
    @abstractmethod
    def notify_enrollment(self, student_id: str, course_name: str) -> None:
        pass


# --- Use Cases ---

class EnrollStudentUseCase:
    """
    Use Case : Inscrire un étudiant à un cours
    Orchestration de la logique applicative
    """
    
    def __init__(self, course_repo: CourseRepository, notifier: NotificationService):
        self.course_repo = course_repo
        self.notifier = notifier
    
    def execute(self, student_id: str, course_id: str) -> dict:
        """
        Exécute le use case
        Returns: dict avec success, message, course
        """
        # 1. Récupérer le cours
        course = self.course_repo.find_by_id(course_id)
        if not course:
            return {
                'success': False,
                'message': f"Cours {course_id} introuvable",
                'course': None
            }
        
        # 2. Vérifier si inscription possible
        if not course.can_enroll():
            return {
                'success': False,
                'message': f"Cours {course.name} complet",
                'course': course
            }
        
        # 3. Inscrire (logique métier dans l'Entity)
        if not course.enroll_student(student_id):
            return {
                'success': False,
                'message': f"Étudiant {student_id} déjà inscrit",
                'course': course
            }
        
        # 4. Sauvegarder
        self.course_repo.save(course)
        
        # 5. Notifier
        self.notifier.notify_enrollment(student_id, course.name)
        
        return {
            'success': True,
            'message': f"Inscription réussie au cours {course.name}",
            'course': course
        }


class GetCourseStatsUseCase:
    """Use Case : Obtenir les statistiques d'un cours"""
    
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo
    
    def execute(self, course_id: str) -> dict:
        """Retourne les statistiques d'un cours"""
        course = self.course_repo.find_by_id(course_id)
        if not course:
            return {'success': False, 'message': 'Cours introuvable'}
        
        return {
            'success': True,
            'course_name': course.name,
            'instructor': course.instructor,
            'enrolled': len(course.enrolled_students),
            'capacity': course.max_students,
            'enrollment_rate': course.get_enrollment_rate(),
            'available_seats': course.max_students - len(course.enrolled_students)
        }


# ============================================================================
# COUCHE 3 : INTERFACE ADAPTERS (Gateways, Controllers, Presenters)
# ============================================================================

# --- Adapters (implémentations des Ports) ---

class InMemoryCourseRepository(CourseRepository):
    """Adapter : Repository en mémoire"""
    
    def __init__(self):
        self._courses: dict[str, Course] = {}
    
    def save(self, course: Course) -> None:
        self._courses[course.course_id] = course
        print(f"[Repository] Cours {course.course_id} sauvegardé")
    
    def find_by_id(self, course_id: str) -> Optional[Course]:
        return self._courses.get(course_id)
    
    def find_all(self) -> List[Course]:
        return list(self._courses.values())


class ConsoleNotificationService(NotificationService):
    """Adapter : Notifications console"""
    
    def notify_enrollment(self, student_id: str, course_name: str) -> None:
        print(f"[Notification] 📧 Étudiant {student_id} inscrit au cours {course_name}")


# --- Controller ---

class CourseController:
    """Controller : Point d'entrée de l'application"""
    
    def __init__(self, enroll_use_case: EnrollStudentUseCase, 
                 stats_use_case: GetCourseStatsUseCase):
        self.enroll_use_case = enroll_use_case
        self.stats_use_case = stats_use_case
    
    def enroll_student(self, student_id: str, course_id: str) -> None:
        """Endpoint : Inscrire un étudiant"""
        result = self.enroll_use_case.execute(student_id, course_id)
        
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['message']}")
    
    def show_course_stats(self, course_id: str) -> None:
        """Endpoint : Afficher les statistiques"""
        result = self.stats_use_case.execute(course_id)
        
        if not result['success']:
            print(f"✗ {result['message']}")
            return
        
        print(f"\n📊 Statistiques du cours {result['course_name']}")
        print(f"   Enseignant: {result['instructor']}")
        print(f"   Inscrits: {result['enrolled']}/{result['capacity']}")
        print(f"   Taux de remplissage: {result['enrollment_rate']:.1f}%")
        print(f"   Places disponibles: {result['available_seats']}")


# ============================================================================
# COUCHE 4 : FRAMEWORKS & DRIVERS (Main, Config)
# ============================================================================

def main():
    """Point d'entrée - Configuration de l'application"""
    
    print("=" * 70)
    print("CLEAN ARCHITECTURE - DÉMONSTRATION")
    print("=" * 70)
    
    # 1. Créer les adapters (couche externe)
    course_repo = InMemoryCourseRepository()
    notifier = ConsoleNotificationService()
    
    # 2. Créer les use cases (couche application)
    enroll_use_case = EnrollStudentUseCase(course_repo, notifier)
    stats_use_case = GetCourseStatsUseCase(course_repo)
    
    # 3. Créer le controller (couche interface)
    controller = CourseController(enroll_use_case, stats_use_case)
    
    # 4. Préparer des données de test
    poo_course = Course(
        course_id="POO-L2",
        name="Programmation Orientée Objet",
        instructor="Prof. Roor",
        max_students=30,
        enrolled_students=[]
    )
    course_repo.save(poo_course)
    
    # 5. Scénarios de test
    print("\n--- Scénario 1: Inscriptions ---")
    controller.enroll_student("STU001", "POO-L2")
    controller.enroll_student("STU002", "POO-L2")
    controller.enroll_student("STU003", "POO-L2")
    
    print("\n--- Scénario 2: Statistiques ---")
    controller.show_course_stats("POO-L2")
    
    print("\n--- Scénario 3: Double inscription ---")
    controller.enroll_student("STU001", "POO-L2")  # Déjà inscrit
    
    print("\n--- Scénario 4: Cours inexistant ---")
    controller.enroll_student("STU004", "WEB-L2")
    
    print("\n" + "=" * 70)
    print("AVANTAGES DE LA CLEAN ARCHITECTURE:")
    print("- Entities pures sans dépendances")
    print("- Use Cases testables indépendamment")
    print("- Changement de DB sans toucher la logique métier")
    print("- Changement de framework sans toucher les Use Cases")
    print("- Dependency Inversion Principle appliqué partout")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## 5. Comparaison des Architectures

| Architecture | Complexité | Use Case | Avantages | Inconvénients |
|--------------|-----------|----------|-----------|---------------|
| **Couches (Layered)** | ⭐ Simple | Petites apps | Facile à comprendre | Peut devenir rigide |
| **MVC** | ⭐⭐ Moyenne | Applications UI | Séparation claire | Coupling Model-View |
| **Clean Architecture** | ⭐⭐⭐ Complexe | Applications critiques | Testabilité maximale | Overhead important |

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **Architecture en Couches** : 3 couches (Presentation, Business, Data)  
✅ **MVC** : Séparation Model-View-Controller  
✅ **Clean Architecture** : Cercles concentriques avec Dependency Rule  

### Principes clés

1. **Séparation des responsabilités** à tous les niveaux
2. **Dépendances contrôlées** (toujours vers l'intérieur en Clean Arch)
3. **Testabilité** par isolation des composants
4. **Évolutivité** en changeant une couche sans affecter les autres

### Dans la Partie 2, nous verrons :

- Hexagonal Architecture (Ports & Adapters)
- Domain-Driven Design (DDD)
- Microservices vs Monolithe
- Event-Driven Architecture
- Applications pratiques pour vos projets

---

*Suite dans la Partie 2...*