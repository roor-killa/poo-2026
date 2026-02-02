# CM6 - Architecture Logicielle (Partie 3 - Finale)
## Synthèse, Exercices et Applications Pratiques

---

## 11. Tableau Comparatif des Architectures

| Architecture | Complexité | Testabilité | Scalabilité | Use Case | Équipe |
|--------------|-----------|-------------|-------------|----------|--------|
| **Layered** | ⭐ Faible | ⭐⭐ Moyenne | ⭐⭐ Moyenne | Apps simples | Petite |
| **MVC** | ⭐⭐ Moyenne | ⭐⭐⭐ Bonne | ⭐⭐ Moyenne | Apps UI | Petite-Moyenne |
| **Clean** | ⭐⭐⭐ Élevée | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Bonne | Apps critiques | Moyenne |
| **Hexagonal** | ⭐⭐⭐ Élevée | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Bonne | Apps flexibles | Moyenne |
| **Microservices** | ⭐⭐⭐⭐⭐ Très élevée | ⭐⭐⭐ Bonne | ⭐⭐⭐⭐⭐ Excellente | Apps distribuées | Grande |

---

## 12. Guide de Choix d'Architecture

### Arbre de Décision

```
Commencer ici
    │
    ├─ Prototype / MVP rapide ?
    │   └─→ OUI → LAYERED ARCHITECTURE
    │
    ├─ Application avec UI riche ?
    │   └─→ OUI → MVC / MVVM
    │
    ├─ Besoin de tests intensifs ?
    │   └─→ OUI → CLEAN ou HEXAGONAL
    │
    ├─ Domaine métier complexe ?
    │   └─→ OUI → DDD + HEXAGONAL
    │
    ├─ Plusieurs équipes indépendantes ?
    │   └─→ OUI → MICROSERVICES
    │
    └─ Événements / Réactions en temps réel ?
        └─→ OUI → EVENT-DRIVEN
```

### Patterns Combinés

Les architectures se combinent souvent :

```python
# Exemple : Microservices + DDD + Hexagonal

Microservice "Student Service"
├── Hexagonal Architecture
│   ├── Domain (DDD)
│   │   ├── Student (Aggregate)
│   │   ├── Enrollment (Entity)
│   │   └── Email (Value Object)
│   ├── Ports
│   │   ├── StudentRepository
│   │   └── NotificationService
│   └── Adapters
│       ├── REST API (primaire)
│       ├── PostgreSQL (secondaire)
│       └── RabbitMQ (secondaire)
```

---

## 13. Exercices Pratiques

### Exercice 1 : Refactoring Architecture

**Contexte :** Vous avez hérité de ce code monolithique :

```python
class LibraryApp:
    """❌ Tout dans une seule classe"""
    
    def __init__(self):
        self.books = []
        self.users = []
    
    def add_book(self, title, author):
        # Validation
        if not title or not author:
            return False
        
        # Sauvegarde
        import sqlite3
        conn = sqlite3.connect('library.db')
        # ...
        
        # Email
        import smtplib
        # ...
        
        # UI Update
        print(f"Livre {title} ajouté")
        
        return True
    
    def borrow_book(self, user_id, book_id):
        # Logique similaire...
        pass
```

**Consignes :**
1. Identifiez les violations des principes architecturaux
2. Proposez une architecture appropriée (Layered, MVC, ou Hexagonal)
3. Refactorisez en respectant l'architecture choisie
4. Justifiez vos choix

---

### Exercice 2 : Conception DDD

**Contexte :** Système de gestion de restaurant universitaire

**Domaine métier :**
- Menus quotidiens avec plats
- Réservations de repas
- Systèmes de tickets/badges
- Gestion du stock
- Allergies et préférences alimentaires

**Consignes :**
1. Identifiez les **Bounded Contexts**
2. Définissez les **Entities** et **Value Objects**
3. Identifiez les **Aggregates**
4. Proposez des **Domain Events**
5. Définissez l'**Ubiquitous Language**

**Exemple de solution partielle :**

```python
# Bounded Context: Menu Management

# Value Objects
@dataclass(frozen=True)
class NutritionalInfo:
    calories: int
    proteins: float
    carbs: float
    fats: float

@dataclass(frozen=True)
class Allergen:
    name: str  # "gluten", "lactose", etc.

# Entities
class Dish:
    def __init__(self, dish_id: str, name: str):
        self.dish_id = dish_id
        self.name = name
        self.nutritional_info: Optional[NutritionalInfo] = None
        self.allergens: List[Allergen] = []

# Aggregate
class DailyMenu:
    """Aggregate Root"""
    def __init__(self, date: datetime, meal_type: str):
        self.menu_id = f"{date.strftime('%Y%m%d')}-{meal_type}"
        self.date = date
        self.meal_type = meal_type  # "lunch", "dinner"
        self._dishes: List[Dish] = []
    
    def add_dish(self, dish: Dish):
        """Règle métier : Max 5 plats par menu"""
        if len(self._dishes) >= 5:
            raise ValueError("Menu complet")
        self._dishes.append(dish)

# Domain Event
@dataclass
class MenuPublishedEvent:
    menu_id: str
    date: datetime
    dish_count: int
```

---

### Exercice 3 : Microservices Design

**Contexte :** Plateforme de e-learning

**Fonctionnalités :**
- Gestion des cours et contenus
- Inscriptions et paiements
- Suivi de progression
- Certificats
- Forum de discussion
- Notifications

**Consignes :**
1. Découpez en microservices (au moins 5)
2. Définissez les APIs de chaque service
3. Identifiez les communications synchrones vs asynchrones
4. Proposez une stratégie de données (base par service ? partagée ?)
5. Gérez les transactions distribuées

---

## 14. Cas Pratiques Complets

### Cas 1 : Application de Réservation de Salles

**Architecture choisie :** Hexagonal + DDD

```python
# ============================================================================
# DOMAIN LAYER
# ============================================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List


# Value Objects
@dataclass(frozen=True)
class TimeSlot:
    """Value Object : Créneau horaire"""
    start: datetime
    end: datetime
    
    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("L'heure de fin doit être après l'heure de début")
    
    def overlaps(self, other: 'TimeSlot') -> bool:
        """Vérifie si deux créneaux se chevauchent"""
        return (self.start < other.end) and (other.start < self.end)
    
    def duration_hours(self) -> float:
        """Durée en heures"""
        delta = self.end - self.start
        return delta.total_seconds() / 3600


# Entities
class Room:
    """Entity : Salle"""
    
    def __init__(self, room_id: str, name: str, capacity: int):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.equipment: List[str] = []
    
    def can_accommodate(self, attendees: int) -> bool:
        """Règle métier : Vérifier la capacité"""
        return attendees <= self.capacity


class Reservation:
    """Entity : Réservation"""
    
    def __init__(self, reservation_id: str, room_id: str, 
                 user_id: str, time_slot: TimeSlot):
        self.reservation_id = reservation_id
        self.room_id = room_id
        self.user_id = user_id
        self.time_slot = time_slot
        self.status = "CONFIRMED"
        self.attendees = 1
    
    def cancel(self):
        """Règle métier : Annuler une réservation"""
        if self.status == "CANCELLED":
            raise ValueError("Réservation déjà annulée")
        self.status = "CANCELLED"
    
    def is_active(self) -> bool:
        return self.status == "CONFIRMED"


# Aggregate
class RoomSchedule:
    """
    Aggregate Root : Planning d'une salle
    Gère toutes les réservations d'une salle
    """
    
    def __init__(self, room: Room):
        self.room = room
        self._reservations: List[Reservation] = []
    
    def make_reservation(self, reservation_id: str, user_id: str, 
                        time_slot: TimeSlot, attendees: int) -> Reservation:
        """
        Règle métier : Créer une réservation
        Invariants :
        - Pas de chevauchement
        - Capacité suffisante
        """
        # Vérifier la capacité
        if not self.room.can_accommodate(attendees):
            raise ValueError(f"Salle trop petite (capacité: {self.room.capacity})")
        
        # Vérifier les conflits
        if self._has_conflict(time_slot):
            raise ValueError("Créneau non disponible")
        
        # Créer la réservation
        reservation = Reservation(reservation_id, self.room.room_id, 
                                 user_id, time_slot)
        reservation.attendees = attendees
        self._reservations.append(reservation)
        
        return reservation
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """Annuler une réservation"""
        reservation = self._find_reservation(reservation_id)
        if not reservation:
            return False
        
        reservation.cancel()
        return True
    
    def get_available_slots(self, date: datetime, 
                           slot_duration_hours: float = 1.0) -> List[TimeSlot]:
        """
        Règle métier : Trouver les créneaux disponibles
        Horaires : 8h - 20h
        """
        available_slots = []
        
        # Créer les créneaux de la journée
        current = date.replace(hour=8, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=20, minute=0, second=0, microsecond=0)
        
        while current < end_of_day:
            slot_end = current + timedelta(hours=slot_duration_hours)
            if slot_end > end_of_day:
                break
            
            slot = TimeSlot(current, slot_end)
            
            # Vérifier si disponible
            if not self._has_conflict(slot):
                available_slots.append(slot)
            
            current = slot_end
        
        return available_slots
    
    def _has_conflict(self, time_slot: TimeSlot) -> bool:
        """Vérifie si un créneau est en conflit"""
        for reservation in self._reservations:
            if reservation.is_active():
                if reservation.time_slot.overlaps(time_slot):
                    return True
        return False
    
    def _find_reservation(self, reservation_id: str) -> Optional[Reservation]:
        for reservation in self._reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None


# ============================================================================
# PORTS (Interfaces)
# ============================================================================

class RoomRepository(ABC):
    """Port : Repository pour les salles"""
    
    @abstractmethod
    def find_by_id(self, room_id: str) -> Optional[Room]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Room]:
        pass


class ScheduleRepository(ABC):
    """Port : Repository pour les plannings"""
    
    @abstractmethod
    def save(self, schedule: RoomSchedule) -> None:
        pass
    
    @abstractmethod
    def find_by_room_id(self, room_id: str) -> Optional[RoomSchedule]:
        pass


class NotificationService(ABC):
    """Port : Service de notification"""
    
    @abstractmethod
    def notify_reservation_confirmed(self, user_id: str, 
                                    room_name: str, time_slot: TimeSlot):
        pass
    
    @abstractmethod
    def notify_reservation_cancelled(self, user_id: str, 
                                     room_name: str):
        pass


# ============================================================================
# USE CASES
# ============================================================================

class MakeReservationUseCase:
    """Use Case : Faire une réservation"""
    
    def __init__(self, room_repo: RoomRepository, 
                 schedule_repo: ScheduleRepository,
                 notifier: NotificationService):
        self.room_repo = room_repo
        self.schedule_repo = schedule_repo
        self.notifier = notifier
    
    def execute(self, room_id: str, user_id: str, 
                start: datetime, end: datetime, attendees: int) -> dict:
        """Exécute le use case"""
        
        # 1. Récupérer la salle
        room = self.room_repo.find_by_id(room_id)
        if not room:
            return {'success': False, 'error': 'Salle introuvable'}
        
        # 2. Récupérer ou créer le planning
        schedule = self.schedule_repo.find_by_room_id(room_id)
        if not schedule:
            schedule = RoomSchedule(room)
        
        # 3. Créer le créneau
        try:
            time_slot = TimeSlot(start, end)
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        
        # 4. Faire la réservation
        try:
            reservation_id = f"RES-{user_id}-{start.timestamp()}"
            reservation = schedule.make_reservation(
                reservation_id, user_id, time_slot, attendees
            )
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        
        # 5. Sauvegarder
        self.schedule_repo.save(schedule)
        
        # 6. Notifier
        self.notifier.notify_reservation_confirmed(
            user_id, room.name, time_slot
        )
        
        return {
            'success': True,
            'reservation_id': reservation.reservation_id,
            'room': room.name,
            'time_slot': time_slot
        }


class GetAvailableSlotsUseCase:
    """Use Case : Obtenir les créneaux disponibles"""
    
    def __init__(self, room_repo: RoomRepository, 
                 schedule_repo: ScheduleRepository):
        self.room_repo = room_repo
        self.schedule_repo = schedule_repo
    
    def execute(self, room_id: str, date: datetime) -> dict:
        """Exécute le use case"""
        
        # 1. Récupérer la salle
        room = self.room_repo.find_by_id(room_id)
        if not room:
            return {'success': False, 'error': 'Salle introuvable'}
        
        # 2. Récupérer le planning
        schedule = self.schedule_repo.find_by_room_id(room_id)
        if not schedule:
            schedule = RoomSchedule(room)
        
        # 3. Obtenir les créneaux disponibles
        available_slots = schedule.get_available_slots(date)
        
        return {
            'success': True,
            'room': room.name,
            'date': date,
            'available_slots': available_slots
        }


# ============================================================================
# ADAPTERS (Implémentations)
# ============================================================================

class InMemoryRoomRepository(RoomRepository):
    """Adapter : Repository en mémoire pour les salles"""
    
    def __init__(self):
        self._rooms = {
            'AMPHI-A': Room('AMPHI-A', 'Amphithéâtre A', 200),
            'SALLE-101': Room('SALLE-101', 'Salle 101', 30),
            'LAB-INFO': Room('LAB-INFO', 'Laboratoire Informatique', 25),
        }
    
    def find_by_id(self, room_id: str) -> Optional[Room]:
        return self._rooms.get(room_id)
    
    def find_all(self) -> List[Room]:
        return list(self._rooms.values())


class InMemoryScheduleRepository(ScheduleRepository):
    """Adapter : Repository en mémoire pour les plannings"""
    
    def __init__(self):
        self._schedules: dict[str, RoomSchedule] = {}
    
    def save(self, schedule: RoomSchedule) -> None:
        self._schedules[schedule.room.room_id] = schedule
    
    def find_by_room_id(self, room_id: str) -> Optional[RoomSchedule]:
        return self._schedules.get(room_id)


class ConsoleNotificationService(NotificationService):
    """Adapter : Notifications console"""
    
    def notify_reservation_confirmed(self, user_id: str, 
                                    room_name: str, time_slot: TimeSlot):
        print(f"\n📧 [Notification] Réservation confirmée")
        print(f"   Utilisateur: {user_id}")
        print(f"   Salle: {room_name}")
        print(f"   Horaire: {time_slot.start.strftime('%H:%M')} - "
              f"{time_slot.end.strftime('%H:%M')}")
    
    def notify_reservation_cancelled(self, user_id: str, room_name: str):
        print(f"\n📧 [Notification] Réservation annulée")
        print(f"   Utilisateur: {user_id}")
        print(f"   Salle: {room_name}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("CAS PRATIQUE : SYSTÈME DE RÉSERVATION DE SALLES")
    print("Architecture: Hexagonal + DDD")
    print("=" * 70)
    
    # Configuration (Dependency Injection)
    room_repo = InMemoryRoomRepository()
    schedule_repo = InMemoryScheduleRepository()
    notifier = ConsoleNotificationService()
    
    # Use Cases
    make_reservation = MakeReservationUseCase(room_repo, schedule_repo, notifier)
    get_available = GetAvailableSlotsUseCase(room_repo, schedule_repo)
    
    # Scénario 1 : Voir les créneaux disponibles
    print("\n--- Scénario 1: Créneaux disponibles ---")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    result = get_available.execute('AMPHI-A', today)
    
    if result['success']:
        print(f"\nCréneaux disponibles pour {result['room']}:")
        for i, slot in enumerate(result['available_slots'][:5], 1):
            print(f"  {i}. {slot.start.strftime('%H:%M')} - "
                  f"{slot.end.strftime('%H:%M')} "
                  f"({slot.duration_hours():.1f}h)")
    
    # Scénario 2 : Faire une réservation
    print("\n--- Scénario 2: Réservation ---")
    start_time = today.replace(hour=14, minute=0)
    end_time = today.replace(hour=16, minute=0)
    
    result = make_reservation.execute(
        'AMPHI-A',
        'prof.roor@ua.fr',
        start_time,
        end_time,
        50
    )
    
    if result['success']:
        print(f"\n✓ Réservation réussie!")
        print(f"   ID: {result['reservation_id']}")
    
    # Scénario 3 : Tentative de réservation en conflit
    print("\n--- Scénario 3: Conflit de réservation ---")
    result = make_reservation.execute(
        'AMPHI-A',
        'autre@ua.fr',
        start_time,  # Même créneau !
        end_time,
        30
    )
    
    if not result['success']:
        print(f"\n✗ Réservation échouée: {result['error']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
```

---

## 15. Anti-Patterns Architecturaux

### 15.1 Big Ball of Mud

**Symptôme :** Code sans structure claire, tout est connecté à tout.

```python
# ❌ Anti-pattern
class Application:
    def do_everything(self):
        # 10000 lignes de code mélangées
        pass
```

**Solution :** Appliquer une architecture claire dès le début.

### 15.2 God Service

**Symptôme :** Un service qui fait tout.

```python
# ❌ Anti-pattern
class ApplicationService:
    def process_order(self): pass
    def send_email(self): pass
    def calculate_taxes(self): pass
    def generate_report(self): pass
    # ... 50 autres méthodes
```

**Solution :** Séparer en services spécialisés (SRP).

### 15.3 Distributed Monolith

**Symptôme :** Microservices qui se comportent comme un monolithe.

```
Service A ←→ Service B ←→ Service C ←→ Service D
(tous fortement couplés, déploiement ensemble requis)
```

**Solution :** Vraie indépendance des services, événements asynchrones.

### 15.4 Anemic Domain Model

**Symptôme :** Entities sans logique métier (juste des getters/setters).

```python
# ❌ Anti-pattern
class Order:
    def __init__(self):
        self.items = []
    
    def get_items(self): return self.items
    def set_items(self, items): self.items = items

# Logique métier dans le service
class OrderService:
    def calculate_total(self, order):
        return sum(item.price for item in order.get_items())
```

**Solution :** Logique métier dans les Entities.

```python
# ✅ Correct
class Order:
    def __init__(self):
        self._items = []
    
    def add_item(self, item):
        self._items.append(item)
    
    def calculate_total(self):
        return sum(item.price for item in self._items)
```

---

## 16. Conclusion Générale du CM6

### Récapitulatif

**Partie 1 :**
- ✅ Architecture en Couches
- ✅ MVC (Model-View-Controller)
- ✅ Clean Architecture

**Partie 2 :**
- ✅ Hexagonal Architecture
- ✅ Domain-Driven Design (DDD)
- ✅ Microservices vs Monolithe
- ✅ Event-Driven Architecture

**Partie 3 :**
- ✅ Guide de choix
- ✅ Cas pratiques
- ✅ Anti-patterns

### Principes Universels

Quelle que soit l'architecture :

1. **Séparation des responsabilités**
2. **Dépendances contrôlées** (vers l'intérieur/abstraction)
3. **Testabilité** par isolation
4. **Évolutivité** sans casse
5. **Lisibilité** et maintenabilité

### Le Parcours Complet

```
CM4: Design Patterns
    ↓
    Résoudre des problèmes récurrents
    
CM5: Principes SOLID
    ↓
    Qualité au niveau classe
    
CM6: Architecture Logicielle
    ↓
    Organisation à grande échelle
    
→ CODE DE QUALITÉ PROFESSIONNELLE
```

---

## 17. Projet Final Intégratif

### Système de Gestion Universitaire

**Objectif :** Concevoir et implémenter un système complet utilisant tous les concepts vus.

**Fonctionnalités :**
1. Gestion des étudiants et enseignants
2. Gestion des cours et inscriptions
3. Planning et réservation de salles
4. Système de notation
5. Génération de relevés et certificats
6. Paiement des frais de scolarité
7. Notifications multi-canal

**Contraintes techniques :**
- Appliquer **SOLID** (CM5)
- Utiliser au moins **5 design patterns** (CM4)
- Choisir une **architecture appropriée** (CM6)
- **Tests unitaires** (min 80% coverage)
- **Documentation** complète

**Livrables :**
1. **Diagramme d'architecture** (C4 Model niveau 2 et 3)
2. **Code source** avec commentaires
3. **Tests** automatisés
4. **README** avec :
   - Architecture choisie et justification
   - Patterns utilisés et où
   - Principes SOLID appliqués
   - Instructions de déploiement

**Critères d'évaluation :**
- Architecture (30%)
- Respect SOLID (20%)
- Design Patterns (20%)
- Tests (15%)
- Documentation (15%)

---

## 18. Ressources et Références

### Livres Fondamentaux

**Architecture :**
- **"Clean Architecture"** - Robert C. Martin
- **"Building Microservices"** - Sam Newman
- **"Domain-Driven Design"** - Eric Evans
- **"Patterns of Enterprise Application Architecture"** - Martin Fowler

**Pratique :**
- **"Software Architecture in Practice"** - Len Bass
- **"Fundamentals of Software Architecture"** - Mark Richards

### Ressources en Ligne

- **C4 Model** (c4model.com) - Diagrammes d'architecture
- **Martin Fowler's Blog** (martinfowler.com)
- **DDD Community** (dddcommunity.org)
- **Microservices.io** - Patterns microservices

### Outils

- **PlantUML** - Diagrammes architecture
- **ArchUnit** - Tests architecture
- **SonarQube** - Qualité code
- **Docker** - Containerisation

---

## 19. Prochains Cours

**CM7 : Tests et Qualité de Code**
- Tests unitaires, intégration, E2E
- TDD (Test-Driven Development)
- Mocking et Dependency Injection
- Code Coverage et métriques

**CM8 : DevOps et CI/CD**
- Pipelines d'intégration continue
- Déploiement automatisé
- Monitoring et observabilité
- Infrastructure as Code

**CM9 : Sécurité**
- OWASP Top 10
- Authentication & Authorization
- Chiffrement
- Sécurité des APIs

---

## 20. Message Final

### L'Architecture n'est pas...

❌ Une obligation rigide  
❌ Une solution universelle  
❌ À appliquer aveuglément  
❌ Plus importante que le code qui fonctionne  

### L'Architecture est...

✅ Un guide pour organiser le code  
✅ Une aide à la communication d'équipe  
✅ Un investissement pour le futur  
✅ Une évolution progressive  

### Règles d'Or

**Start Simple** → Commencez simple  
**Refactor Continuously** → Refactorisez en continu  
**Test Everything** → Testez tout  
**Document Decisions** → Documentez les décisions  
**Adapt to Context** → Adaptez au contexte  

### Citation Finale

> **"Architecture is about the important stuff. Whatever that is."**
> 
> *— Ralph Johnson*

---

## Questions ?

Merci pour votre attention ! 

**Contact :** roland.ratenan@nasdy.fr  
**Repo GitHub :** (pour les exemples de code)

---
