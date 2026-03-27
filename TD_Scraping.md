# TP - Web Scraping en Programmation Orientée Objet (Python)

## 🎯 Objectifs Pédagogiques

À l'issue de ce TP, vous serez capable de :
- Concevoir et implémenter des scrapers web en POO
- Utiliser BeautifulSoup4 et Requests efficacement
- Structurer du code réutilisable avec l'héritage et le polymorphisme
- Gérer les erreurs et les cas limites du scraping
- Respecter l'éthique du web scraping (robots.txt, rate limiting)
- Exporter des données structurées (JSON, CSV, base de données)

## 📋 Prérequis

```bash
pip install requests beautifulsoup4 lxml pandas python-dotenv
```

## 🏗️ Architecture du Projet

```
scraping-poo/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── news_scraper.py
│   └── business_scraper.py
├── models/
│   ├── __init__.py
│   └── data_models.py
├── utils/
│   ├── __init__.py
│   ├── file_handler.py
│   └── validators.py
├── tests/
│   └── test_scrapers.py
├── data/
│   ├── raw/
│   └── processed/
├── main.py
└── requirements.txt
```

---

## 📚 Partie 1 : Classe de Base (Scraper Générique)

### Exercice 1.1 : Créer la Classe BaseScraper

Créez une classe abstraite qui servira de fondation pour tous vos scrapers.

```python
# scrapers/base_scraper.py

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
from datetime import datetime

class BaseScraper(ABC):
    """
    Classe de base abstraite pour tous les scrapers.
    Implémente les fonctionnalités communes.
    """
    
    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Args:
            base_url: URL de base du site à scraper
            delay: Délai entre les requêtes (en secondes)
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational Purpose) Université des Antilles'
        })
        self.last_request_time = None
        
    def _respect_delay(self):
        """Respecte le délai entre les requêtes"""
        # À COMPLÉTER
        pass
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page web
        
        Returns:
            BeautifulSoup object ou None si erreur
        """
        # À COMPLÉTER
        pass
    
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Méthode abstraite à implémenter dans les classes enfants.
        Parse le contenu HTML et extrait les données.
        """
        pass
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Méthode principale de scraping.
        À implémenter dans les classes enfants.
        """
        pass
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Sauvegarde les données en JSON"""
        # À COMPLÉTER
        pass
    
    def close(self):
        """Ferme la session"""
        self.session.close()
```

**✏️ Travail à faire :**
1. Complétez la méthode `_respect_delay()` pour attendre entre les requêtes
2. Implémentez `fetch_page()` avec gestion d'erreurs (try/except)
3. Implémentez `save_to_json()` pour exporter les données

---

## 🗞️ Partie 2 : Scraper d'Articles de Presse Locale

### Exercice 2.1 : Scraper Martinique 1ère

Créez un scraper pour extraire les actualités locales.

```python
# scrapers/news_scraper.py

from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

class NewsScraper(BaseScraper):
    """
    Scraper pour les articles de presse martiniquaise
    """
    
    def __init__(self, category: str = "actualites"):
        """
        Args:
            category: Catégorie d'articles (actualites, sports, culture, etc.)
        """
        # À COMPLÉTER : initialiser avec l'URL appropriée
        super().__init__(base_url="https://example-news-site.mq")
        self.category = category
        
    def parse_article(self, article_soup: BeautifulSoup) -> Dict:
        """
        Parse un article individuel
        
        Returns:
            Dict avec titre, date, auteur, contenu, tags
        """
        # À COMPLÉTER
        pass
    
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse la page de liste d'articles
        """
        # À COMPLÉTER
        pass
    
    def scrape(self, max_pages: int = 3) -> List[Dict]:
        """
        Scrape plusieurs pages d'articles
        
        Args:
            max_pages: Nombre maximum de pages à scraper
        """
        # À COMPLÉTER
        pass
```

**✏️ Travail à faire :**
1. Choisissez un site d'actualités martiniquais accessible
2. Analysez la structure HTML (inspecteur du navigateur)
3. Implémentez les méthodes `parse_article()`, `parse()` et `scrape()`
4. Extrayez : titre, date de publication, auteur, chapeau, contenu complet, tags/catégories
5. Testez sur 10 articles minimum

**⚠️ Contraintes :**
- Respectez le fichier `robots.txt` du site
- Ajoutez un délai de 2 secondes entre chaque requête
- Gérez les articles sans auteur ou sans date

---

## 🏪 Partie 3 : Scraper d'Annuaire d'Entreprises

### Exercice 3.1 : Scraper d'Entreprises Locales

```python
# scrapers/business_scraper.py

from .base_scraper import BaseScraper
from typing import List, Dict, Optional
import re

class BusinessScraper(BaseScraper):
    """
    Scraper pour les annuaires d'entreprises martiniquaises
    """
    
    def __init__(self):
        super().__init__(base_url="https://example-directory.mq")
        
    def clean_phone(self, phone: str) -> str:
        """
        Nettoie et formate les numéros de téléphone
        Format attendu : 0596 XX XX XX
        """
        # À COMPLÉTER
        pass
    
    def extract_email(self, text: str) -> Optional[str]:
        """
        Extrait une adresse email du texte avec regex
        """
        # À COMPLÉTER
        pass
    
    def parse_business(self, business_soup: BeautifulSoup) -> Dict:
        """
        Parse une fiche entreprise
        
        Returns:
            Dict avec nom, adresse, téléphone, email, secteur, description
        """
        # À COMPLÉTER
        pass
    
    def scrape_category(self, category: str, max_results: int = 50) -> List[Dict]:
        """
        Scrape les entreprises d'une catégorie
        
        Args:
            category: Secteur d'activité (restauration, tourisme, etc.)
            max_results: Nombre maximum d'entreprises à scraper
        """
        # À COMPLÉTER
        pass
```

**✏️ Travail à faire :**
1. Utilisez un annuaire public (pages jaunes, annuaire local, etc.)
2. Implémentez la validation des numéros de téléphone
3. Utilisez des regex pour extraire les emails
4. Gérez les adresses multiformats
5. Scrapez au moins 2 catégories différentes (ex: restaurants, hôtels)

---

## 📊 Partie 4 : Modèles de Données et Validation

### Exercice 4.1 : Dataclasses pour la Structure

```python
# models/data_models.py

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import json

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
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        # À COMPLÉTER
        pass
    
    def __str__(self) -> str:
        return f"{self.title} - {self.author} ({self.published_date.date()})"

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
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return asdict(self)
    
    def is_complete(self) -> bool:
        """Vérifie si les données essentielles sont présentes"""
        # À COMPLÉTER
        pass
```

**✏️ Travail à faire :**
1. Complétez les méthodes `to_dict()` et `is_complete()`
2. Ajoutez une validation des emails dans Business
3. Créez une méthode pour exporter en CSV
4. Implémentez une méthode de recherche par commune

---

## 🔧 Partie 5 : Utilitaires et Gestion de Fichiers

### Exercice 5.1 : Gestionnaire de Fichiers

```python
# utils/file_handler.py

import json
import csv
from pathlib import Path
from typing import List, Dict
import pandas as pd

class FileHandler:
    """Gestion de l'export des données scrapées"""
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def save_json(self, data: List[Dict], filename: str):
        """Sauvegarde en JSON avec indentation"""
        # À COMPLÉTER
        pass
    
    def save_csv(self, data: List[Dict], filename: str):
        """Sauvegarde en CSV"""
        # À COMPLÉTER
        pass
    
    def load_json(self, filename: str) -> List[Dict]:
        """Charge des données JSON"""
        # À COMPLÉTER
        pass
    
    def create_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """Crée un DataFrame pandas pour analyse"""
        # À COMPLÉTER
        pass
    
    def export_excel(self, data: List[Dict], filename: str):
        """Exporte vers Excel avec plusieurs feuilles si nécessaire"""
        # À COMPLÉTER
        pass
```

---

## 🚀 Projet Final : Annuaire Collaboratif Martiniquais ou voir TP_Scraping.md

### Objectif
Créer un système complet de scraping pour constituer une base de données d'entreprises et d'actualités martiniquaises.

### Fonctionnalités Requises

1. **ScraperManager** - Classe orchestrant plusieurs scrapers
```python
class ScraperManager:
    def __init__(self):
        self.scrapers = []
        self.results = {}
        
    def add_scraper(self, name: str, scraper: BaseScraper):
        """Ajoute un scraper à la liste"""
        pass
    
    def run_all(self):
        """Execute tous les scrapers enregistrés"""
        pass
    
    def export_combined(self, format: str = 'json'):
        """Exporte toutes les données collectées"""
        pass
```

2. **Dashboard de Statistiques** - Générez un rapport HTML avec :
   - Nombre d'entreprises par catégorie
   - Nombre d'entreprises par commune
   - Distribution des articles par date
   - Top 10 des auteurs les plus actifs

3. **Système de Cache** - Évitez de re-scraper les mêmes pages
```python
class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        
    def get(self, url: str) -> Optional[str]:
        """Récupère du cache si disponible"""
        pass
    
    def set(self, url: str, content: str, ttl: int = 3600):
        """Met en cache avec expiration"""
        pass
```

4. **CLI Interface** - Interface en ligne de commande
```python
# main.py
import argparse

def main():
    parser = argparse.ArgumentParser(description='Scraper Martiniquais')
    parser.add_argument('--type', choices=['news', 'business', 'all'])
    parser.add_argument('--category', help='Catégorie à scraper')
    parser.add_argument('--output', default='data', help='Dossier de sortie')
    parser.add_argument('--format', choices=['json', 'csv', 'excel'])
    
    args = parser.parse_args()
    # À COMPLÉTER
```

### Livrables

**📦 Sur Git (un groupe = une branche) :**
```
feature/groupe-{numero}/scraping-project
```

**📝 À rendre :**
1. Code source complet avec POO
2. README.md avec :
   - Instructions d'installation
   - Exemples d'utilisation
   - Sites scrapés (avec justification éthique)
   - Difficultés rencontrées et solutions
3. Rapport de données (PDF) :
   - Statistiques sur les données collectées
   - Graphiques (matplotlib/seaborn)
   - Analyse de la qualité des données
4. Fichiers de données :
   - Au moins 100 entreprises
   - Au moins 50 articles
   - Exportés en JSON et CSV

### 🎁 Bonus Possibles (+5 points max)

- Scraper avec Selenium pour sites JavaScript
- Base de données SQLite/PostgreSQL
- API REST Flask pour exposer les données
- Tests unitaires avec pytest
- Détection automatique de nouveaux articles
- Système de notifications (nouveaux articles dans une catégorie)
- Analyse de sentiment sur les articles (NLP)
- Déploiement sur un serveur avec cron job

---

## 📖 Ressources

### Documentation
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://requests.readthedocs.io/)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)

### Éthique du Scraping
- Toujours vérifier `robots.txt`
- Respecter les délais entre requêtes
- Identifier votre bot dans le User-Agent
- Ne pas surcharger les serveurs
- Respecter les CGU des sites

### Sites Martiniquais Possibles (Exemples)
- Actualités : Martinique 1ère, RCI, France-Antilles
- Annuaires : Pages Jaunes Martinique, annuaires locaux
- Météo : Météo France Martinique
- Événements : agendas culturels locaux

---

## ⚠️ Règles Importantes

1. **Code AI-généré** : Si vous utilisez ChatGPT/Copilot, vous DEVEZ être capable d'expliquer chaque ligne
2. **Git** : Commits réguliers avec messages clairs
3. **Collaboration** : Répartition équitable du travail dans le groupe
4. **Délais** : Pas de retard accepté sans justification médicale

Bon courage ! 🚀

* roor@nasdy.fr - Université des Antilles *