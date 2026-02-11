# TP - Scraping de Données et POO en Python

**Niveau :** Licence 2 Informatique UA
**Cours :** Programmation Orientée Objet (Python)  
**Modalité :** Binôme ou trinôme  

---

## 🎯 Contexte et Objectifs

Dans le contexte caribéen, de nombreuses données économiques et commerciales sont dispersées sur différents sites web locaux. Ce TP vous permettra de développer un système de scraping orienté objet capable d'extraire, structurer et analyser des données provenant de sites caribéens populaires.

### Objectifs pédagogiques

- **Maîtriser les concepts avancés de la POO** : classes abstraites, héritage, polymorphisme, encapsulation
- **Implémenter des design patterns** : Factory, Strategy, Observer
- **Manipuler des bibliothèques de scraping** : BeautifulSoup4, Requests, Selenium (optionnel)
- **Gérer les exceptions et erreurs** de manière robuste
- **Structurer un projet Python** professionnel avec modules et packages
- **Documenter le code** selon les standards (docstrings, type hints)

---

## 📋 Description du Projet

Vous devez concevoir et implémenter une **application orientée objet** capable de scraper des données depuis les sites suivants :

1. **bizouk.com** - Petites annonces caribéennes
2. **kiprix.com** - Comparateur de prix antillais
3. **madiana.com** - Cinéma locale
4. **rci.fm** - Site d'actualités et radio

### Fonctionnalités attendues

#### 1️⃣ Architecture POO (Séance 1)

Créer une hiérarchie de classes comprenant :

```
BaseScraper (classe abstraite)
    ├── BizoukScraper
    ├── KiprixScraper
    ├── MadianaScraper
    └── RCIScraper
```

**Classe abstraite `BaseScraper` doit contenir :**
- Attributs communs : `url`, `timeout`, `headers`, `data`
- Méthodes abstraites : `scrape()`, `parse()`
- Méthodes concrètes : `fetch_page()`, `save_to_json()`, `save_to_csv()`
- Gestion des erreurs réseau (timeout, 404, etc.)

#### 2️⃣ Implémentation des scrapers spécifiques (Séance 2)

Chaque scraper doit extraire des données pertinentes :

- **BizoukScraper** : Annonces (titre, prix, catégorie, localisation, date)
- **KiprixScraper** : Produits (nom, prix, magasin, disponibilité)
- **MadianaScraper** : Articles (description, prix, vendeur, images)
- **RCIScraper** : Articles d'actualité (titre, date, catégorie, résumé)

#### 3️⃣ Fonctionnalités avancées (Séance 3)

- **Classe `ScraperManager`** : 
  - Pattern Factory pour créer les scrapers appropriés
  - Méthode pour scraper tous les sites en parallèle (threading optionnel)
  - Agrégation des données dans un format unifié

- **Classe `DataAnalyzer`** :
  - Statistiques descriptives sur les données scrapées
  - Détection de tendances de prix (pour kiprix.com)
  - Export vers différents formats (JSON, CSV, Excel)

- **Gestion de cache** :
  - Éviter de re-scraper des pages récemment visitées
  - Stockage temporaire avec timestamps

---

## 🛠️ Contraintes Techniques

### Obligatoires

1. **Python 3.10+** avec type hints
2. **Structure de projet** :
```
tp_scraping/
├── src/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── bizouk_scraper.py
│   │   ├── kiprix_scraper.py
│   │   ├── madiana_scraper.py
│   │   └── rci_scraper.py
│   ├── manager.py
│   └── analyzer.py
├── data/
│   ├── raw/
│   └── processed/
├── tests/
│   └── test_scrapers.py
├── requirements.txt
├── README.md
└── main.py
```

3. **Bibliothèques requises** :
```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

4. **Respect du `robots.txt`** et délais entre requêtes (rate limiting)
5. **Documentation** : Docstrings Google style pour toutes les classes et méthodes
6. **Gestion d'erreurs** : Try-except appropriés avec logging
7. **Git** : Commits réguliers avec messages explicites
8. **Containerisation** avec Docker

### Optionnelles (bonus)

- Utilisation de **Selenium** pour les sites avec JavaScript dynamique
- **Tests unitaires** avec pytest
- **Interface CLI** avec argparse ou click

- **Base de données** SQLite pour stocker les résultats

---

## 📦 Livrables

### Obligatoires

1. **Code source complet** sur dépôt GitHub poo-2026
2. **README.md** détaillé avec :
   - Installation et dépendances
   - Utilisation (exemples de commandes)
   - Architecture du projet
   - Difficultés rencontrées et solutions
3. **Fichier de données** exemple (JSON ou CSV) avec au moins 50 entrées par site
4. **Documentation technique** (PDF) :
   - Diagramme de classes UML
   - Explication des design patterns utilisés
   - Guide d'utilisation
5. **Présentation orale** (10 min) : démo + explication technique

### Optionnels

- Notebook Jupyter avec analyse des données
- Dashboard de visualisation (Streamlit/Dash)
- API REST pour accéder aux données scrapées
- Tests unitaires avec coverage > 70%

---

## 📊 Critères d'Évaluation

| Critère | Points | Détails |
|---------|--------|---------|
| **Architecture POO** | /6 | Héritage, encapsulation, polymorphisme, abstraction |
| **Qualité du code** | /4 | PEP8, type hints, documentation, nommage |
| **Fonctionnalités** | /5 | Tous les scrapers fonctionnels avec données correctes |
| **Gestion d'erreurs** | /2 | Robustesse face aux erreurs réseau et parsing |
| **Documentation** | /2 | README, docstrings, UML |
| **Git & collaboration** | /1 | Commits réguliers, messages clairs, branches |
| **Bonus** | /2 | Tests, Docker, interface, features avancées |
| **TOTAL** | **/20** | |

**Note :** Évaluation continue (40%) + rendu final (60%)

---

## ⚠️ Considérations Éthiques et Légales

1. **Respectez le `robots.txt`** de chaque site
2. **Limitez la fréquence** des requêtes (1-2 secondes entre chaque)
3. **N'utilisez pas les données** à des fins commerciales sans autorisation
4. **Identifiez-vous** via le User-Agent
5. **Responsabilité** : Le scraping est à but pédagogique uniquement

```python
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Educational Project - UA Students)',
    'From': 'votre.email@univ-antilles.fr'
}
```

---

## 💡 Conseils et Ressources

### Démarrage

1. **Analysez d'abord** la structure HTML de chaque site avec les DevTools
2. **Commencez simple** : un seul scraper basique avant d'abstraire
3. **Testez régulièrement** sur de petits échantillons
4. **Gérez les changements** de structure des sites (try-except)

### Exemples de code

**Classe de base suggérée :**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time

class BaseScraper(ABC):
    """Classe abstraite pour tous les scrapers."""
    
    def __init__(self, base_url: str, delay: float = 1.5):
        self.base_url = base_url
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Educational; UA)'
        }
        self.data: List[Dict] = []
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Récupère et parse une page HTML."""
        try:
            time.sleep(self.delay)  # Rate limiting
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Erreur lors du fetch: {e}")
            return None
    
    @abstractmethod
    def scrape(self, max_pages: int = 1) -> List[Dict]:
        """Méthode principale de scraping."""
        pass
    
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse le contenu HTML."""
        pass
```

### Ressources utiles

- [Documentation BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests: HTTP for Humans](https://requests.readthedocs.io/)
- [Real Python - Web Scraping](https://realpython.com/python-web-scraping-practical-introduction/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Type Hints - Python](https://docs.python.org/3/library/typing.html)

---

## 🚀 Pour Aller Plus Loin

Si vous terminez en avance ou souhaitez approfondir :

1. **Scraping dynamique** : Utilisez Selenium pour les sites avec JS
2. **Machine Learning** : Détection automatique de patterns dans les prix
3. **API REST** : Exposez vos données via FastAPI
4. **Monitoring** : Système d'alerte pour nouveaux produits/annonces
5. **Base de données** : PostgreSQL pour stockage à long terme

---

**Bon courage et bon scraping ! 🕷️**

*N'oubliez pas : le scraping est un outil puissant, utilisez-le de manière responsable et éthique.*

---

**Date de rendu :** 4 mars 2026  
**Contact :** roor@nasdy.fr  
**Plateforme de soumission :** GitHub