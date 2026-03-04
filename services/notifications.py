from abc import ABC, abstractmethod
from datetime import datetime

class Observateur(ABC):
    """Interface pour observer les événements de la bibliothèque"""
    
    @abstractmethod
    def notifier(self, message: str):
        pass

class JournalEvenements(Observateur):
    """Enregistre les événements dans un journal"""
    
    def __init__(self):
        self.journal = []
    
    def notifier(self, message: str):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ligne = f"[{date}] {message}"
        self.journal.append(ligne)
        print(ligne)  # Affiche dans la console

class StatistiquesEmprunts(Observateur):
    """Met à jour des statistiques simples sur les emprunts"""
    
    def __init__(self):
        self.emprunts_total = 0
    
    def notifier(self, message: str):
        # Chaque fois qu'un emprunt est notifié, on incrémente
        if "emprunt" in message.lower():
            self.emprunts_total += 1
        print(f"[Stats] Total emprunts: {self.emprunts_total}")