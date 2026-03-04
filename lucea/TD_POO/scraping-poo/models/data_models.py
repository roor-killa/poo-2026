from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import json
import csv
import re


@dataclass
class Article:
    """Modèle pour un article de presse"""
    title: str
    url: str
    published_date: datetime
    author: Optional[str] = None
    content: str = ""
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    scraped_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict: # Convertit l'article en dictionnaire pour faciliter l'exportation
        data = asdict(self)
        data['published_date'] = self.published_date.isoformat()
        data['scraped_at'] = self.scraped_at.isoformat()
        return data

    def __str__(self) -> str: # Représentation lisible de l'article
        return f"{self.title} - {self.author} ({self.published_date.date()})"
    
    def export_csv(self, file_path: str): 
        """Exporte l'article dans un fichier CSV"""
        file = Path(file_path)
        write_header = not file.exists()  # Écrit l'entête seulement si le fichier n'existe pas

        with file.open(mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.to_dict().keys())
            if write_header:
                writer.writeheader()
            writer.writerow(self.to_dict())

@dataclass
class Business: 
    """Modèle pour une entreprise"""
    name: str
    category: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: str = ""
    commune: Optional[str] = None  # Fort-de-France, Schoelcher, etc.
    
    def __post_init__(self): # Nettoyage et validation des données après l'initialisation
        if self.email:
            self.email = self.email.strip()
            if not self._is_valid_email(self.email):
                raise ValueError(f"Email invalide : {self.email}")

    @staticmethod
    def _is_valid_email(email: str) -> bool: # Validation basique de l'email avec une expression régulière
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None
    
    def to_dict(self) -> dict: 
        """Convertit en dictionnaire"""
        return asdict(self)
    
    def is_complete(self) -> bool: 
        """Vérifie si les données essentielles sont présentes"""
        has_contact = any([self.phone, self.email, self.website])
    
        return all([
            self.name,
            self.category,
            has_contact,
            self.commune
        ])
    
    def export_csv(self, file_path: str): 
        """Exporte l'entreprise dans un fichier CSV"""
        file = Path(file_path)
        write_header = not file.exists()

        with file.open(mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.to_dict().keys())
            if write_header:
                writer.writeheader()
            writer.writerow(self.to_dict())

    @staticmethod
    def search_by_commune(business_list: list['Business'], commune: str) -> list['Business']: 
        """
        Recherche les entreprises situées dans une commune donnée (insensible à la casse).
        
        :param business_list: liste d'objets Business
        :param commune: nom de la commune à rechercher
        :return: liste d'objets Business correspondant
        """
        commune = commune.strip().lower()
        return [b for b in business_list if b.commune and b.commune.strip().lower() == commune]