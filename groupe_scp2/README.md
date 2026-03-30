# TP Scraping — Groupe 2 | Kiprix.com 🕷️

Projet de web scraping orienté objet — Licence 2 Informatique, Université des Antilles.
Site scrappé : **kiprix.com** (comparateur de prix France / DOM-TOM).

---

## 👥 Membres du groupe

- **GUINDO** — Lead Développeur & Architecte : BaseScraper, ScraperManager, CacheManager, CLI, KiprixScraper, pagination, Notebook Jupyter, exports multi-formats
- **AKONOU** — Analyste de Données & Features : DataAnalyzer, extraction enrichie
- **SADI** — Qualité, DevOps & Documentation : Tests unitaires (>70%), Docker, documentation technique, rapport PDF

---

## 🏗️ Architecture

```
groupe_scp2/
├── src/
│   ├── __init__.py
│   ├── base_scraper.py            # Classe abstraite (ABC) — BaseScraper
│   ├── manager.py                 # ScraperManager (Pattern Factory)
│   ├── analyzer.py                # DataAnalyzer (pandas)
│   ├── cache.py                   # CacheManager (fichiers JSON + expiration)
│   ├── cli.py                     # Interface CLI (Click)
│   ├── db_manager.py              # DBManager (PostgreSQL via psycopg2)
│   └── scrapers/
│       ├── __init__.py
│       └── kiprix_scraper.py      # KiprixScraper — scraping Kiprix.com
├── tests/
│   ├── test_analyzer.py
│   ├── test_base_scraper.py
│   ├── test_cache.py
│   ├── test_kiprix_scraper.py
│   └── test_manager.py
├── notebooks/
│   └── kiprix_analysis.ipynb      # Analyse exploratoire Jupyter
├── data/
│   ├── raw/                       # JSON/CSV bruts (kiprix_gp.json, etc.)
│   ├── processed/                 # Exports Excel/CSV analysés
│   └── cache/                     # Cache HTML pages
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── documentation/
│   ├── README_DOC.md
│   └── uml.puml                   # Diagramme UML PlantUML
├── main.py                        # Point d'entrée CLI
├── app.py                         # Interface Streamlit (visualisation)
├── requirements.txt
└── Dockerfile
```

---

## 🚀 Installation

### Prérequis
- Python 3.11+
- Chrome / Chromium (pour Selenium)
- PostgreSQL (via Docker recommandé)

### 1. Créer l'environnement virtuel

```bash
cd groupe_scp2
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
pip install psycopg2-binary      # Driver PostgreSQL
```

### 3. Variables d'environnement

Le `DBManager` lit les variables suivantes (avec valeurs par défaut) :

```bash
export DB_HOST=localhost
export DB_USER=laravel
export DB_PASS=secret
export DB_NAME=kiprix_db
export DB_PORT=5433
```

---

## 🖥️ Utilisation CLI

### Scraper des produits

```bash
# Scraper 1 page pour la Martinique, sauvegarder en DB
python main.py scrape --territory mq --pages 1 --format db

# Scraper 5 pages pour la Guadeloupe, sauvegarder en JSON
python main.py scrape --territory gp --pages 5 --format json

# Scraper et tout sauvegarder (JSON + CSV + DB)
python main.py scrape --territory re --pages 3 --format all
```

**Territoires disponibles :**

| Code | Territoire |
|------|-----------|
| `mq` | Martinique |
| `gp` | Guadeloupe |
| `re` | La Réunion |
| `gf` | Guyane |

**Formats de sauvegarde :**

| Format | Description |
|--------|-------------|
| `db` | PostgreSQL (défaut) |
| `json` | Fichier JSON dans `data/raw/` |
| `csv` | Fichier CSV dans `data/raw/` |
| `both` | JSON + CSV |
| `all` | JSON + CSV + DB |

### Analyser les données

```bash
# Rapport statistique en console
python main.py analyze data/raw/kiprix_mq.json

# Exporter en Excel
python main.py analyze data/raw/kiprix_gp.json --export excel

# Exporter en CSV
python main.py analyze data/raw/kiprix_mq.json --export csv
```

### Gestion du cache

```bash
# Voir les stats du cache
python main.py cache-stats

# Vider les entrées expirées
python main.py cache-clear

# Vider tout le cache
python main.py cache-clear --all
```

---

## 🏛️ Architecture POO

### `BaseScraper` (Classe abstraite)
- Méthodes abstraites : `scrape()`, `parse()`
- Méthodes concrètes : `fetch_page()` (Selenium), `save_to_json()`, `save_to_csv()`
- Gestion anti-bot : Selenium + User-Agent

### `KiprixScraper(BaseScraper)`
- Scraping paginé de kiprix.com
- Extraction : nom, prix France, prix DOM, écart %, quantité, prix unitaire
- Méthodes avancées : `get_products_by_category()`, `get_average_price_difference()`, `scrape_all_territories()`

### `ScraperManager` (Pattern Factory)
- Création dynamique des scrapers via `create_scraper(name)`
- Support scraping séquentiel et parallèle (ThreadPoolExecutor)

### `CacheManager`
- Cache fichiers JSON avec expiration configurable
- Hash MD5 des URLs comme clé de cache
- Nettoyage automatique des entrées expirées

### `DataAnalyzer`
- Chargement depuis JSON avec pandas
- Statistiques descriptives
- Analyse écarts de prix France/DOM
- Export Excel et CSV
- Rapport textuel formaté

### `DBManager`
- Connexion PostgreSQL via psycopg2
- Création automatique de la table `produits`
- Insertion batch avec `executemany`

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec couverture de code
pytest --cov=src

# Un module spécifique
pytest tests/test_kiprix_scraper.py -v
```

**Couverture actuelle : 72%**

Modules testés : `base_scraper`, `kiprix_scraper`, `manager`, `cache`, `analyzer`

---

## 🗄️ Structure de la table PostgreSQL

```sql
CREATE TABLE produits (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    url             TEXT,
    price_france    VARCHAR(50),
    price_dom       VARCHAR(50),
    difference      VARCHAR(50),
    quantity_value  NUMERIC(10, 4),
    quantity_unit   VARCHAR(20),
    unit_reference  VARCHAR(20),
    unit_price_france NUMERIC(10, 2),
    unit_price_dom  NUMERIC(10, 2),
    territory       VARCHAR(10),
    territory_name  VARCHAR(100),
    scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🐳 Docker

### Build et run

```bash
# Build
docker build -t kiprix-scraper .

# Scraper la Martinique
docker run kiprix-scraper python main.py scrape --pages 1 --territory mq

# Avec sauvegarde locale
docker run -v ${PWD}/data:/app/data kiprix-scraper python main.py scrape --pages 2 --territory gp
```

### Docker Compose (avec PostgreSQL)

```bash
cd docker
docker-compose up -d
```

---

## 🔗 Intégration avec KaribMarket API

Ce projet est utilisé comme **backend de scraping** par l'API KaribMarket FastAPI.

Le runner FastAPI (`scrape_runner.py`) lance ce projet en subprocess :

```bash
# Commande équivalente lancée par FastAPI
/chemin/venv/bin/python main.py scrape --territory mq --pages 1 --format db
```

Les données sont stockées dans `kiprix_db` et exposées via les endpoints `/api/v1/prix`.

---

## 📦 Stack technique

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11+ | Langage principal |
| Selenium | - | Scraping anti-bot |
| BeautifulSoup4 | - | Parsing HTML |
| requests | - | Requêtes HTTP |
| pandas | - | Analyse données |
| psycopg2 | - | Driver PostgreSQL |
| Click | - | Interface CLI |
| pytest | - | Tests unitaires |
| Docker | - | Containerisation |
