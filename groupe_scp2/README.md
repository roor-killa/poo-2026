# TP Scraping — Groupe 2 | Kiprix.com 🕷️

Projet de web scraping orienté objet avec pipeline RAG — Licence 2 Informatique, Université des Antilles.
Site scrappé : **kiprix.com** (comparateur de prix France / DOM-TOM).

---

## 👥 Membres du groupe

- **GUINDO** — Lead Développeur & Architecte : BaseScraper, ScraperManager, CacheManager, CLI, KiprixScraper, pagination, pipeline RAG, intégration FastAPI
- **AKONOU** — Analyste de Données & Features : DataAnalyzer, extraction enrichie, Notebook Jupyter
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
│   ├── cli.py                     # Interface CLI (Click) + commandes RAG
│   ├── db_manager.py              # DBManager (PostgreSQL via psycopg2)
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── kiprix_scraper.py      # KiprixScraper — scraping Kiprix.com
│   └── rag/                       # Pipeline RAG
│       ├── __init__.py
│       ├── rag_database.py        # RAGDatabase — pgvector operations
│       ├── vectorizer.py          # KiprixVectorizer — chunks + embeddings
│       ├── rag_engine.py          # RAGEngine — retrieve + generate
│       ├── hybrid_rag.py          # HybridRAGEngine — SQL + RAG
│       └── rag_cli.py             # Commandes CLI RAG
├── tests/
│   ├── test_analyzer.py
│   ├── test_base_scraper.py
│   ├── test_cache.py
│   ├── test_kiprix_scraper.py
│   └── test_manager.py
├── notebooks/
│   └── kiprix_analysis.ipynb      # Analyse exploratoire Jupyter
├── data/
│   ├── raw/                       # JSON/CSV bruts
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
└── requirements.txt
```

---

## 🚀 Installation

### Prérequis
- Python 3.11+
- Chrome / Chromium (pour Selenium)
- PostgreSQL avec extension pgvector (via Docker)

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
pip install psycopg2-binary ollama openai pgvector
pip install "numpy<2" "sentence-transformers==3.0.0" "transformers==4.44.0"
```

### 3. Variables d'environnement

```bash
export DB_HOST=localhost
export DB_USER=laravel
export DB_PASS=secret
export DB_NAME=kiprix_db
export DB_PORT=5433
export OPENAI_API_KEY=sk-...  # optionnel
```

---

## 🖥️ Utilisation CLI

### Scraping

```bash
python main.py scrape --territory mq --pages 1 --format db
python main.py scrape --territory gp --pages 5 --format json
python main.py scrape --territory re --pages 3 --format all
```

**Territoires :**

| Code | Territoire |
|------|-----------|
| `mq` | Martinique |
| `gp` | Guadeloupe |
| `re` | La Réunion |
| `gf` | Guyane |

**Formats :**

| Format | Description |
|--------|-------------|
| `db` | PostgreSQL (défaut) |
| `json` | Fichier JSON dans `data/raw/` |
| `csv` | Fichier CSV dans `data/raw/` |
| `both` | JSON + CSV |
| `all` | JSON + CSV + DB |

### Analyse

```bash
python main.py analyze data/raw/kiprix_mq.json
python main.py analyze data/raw/kiprix_gp.json --export excel
python main.py analyze data/raw/kiprix_mq.json --export csv
```

### Cache

```bash
python main.py cache-stats
python main.py cache-clear
python main.py cache-clear --all
```

---

## 🤖 Pipeline RAG

Pipeline RAG (Retrieval-Augmented Generation) pour poser des questions en langage naturel sur les données Kiprix.

### Architecture

```
Produits (PostgreSQL)
    ↓
KiprixVectorizer (sentence-transformers, 768 dims)
    ↓
pgvector (produits_embeddings)
    ↓ similarité cosinus
HybridRAGEngine
    ↓
Ollama (llama3) / OpenAI
    ↓
Réponse en français
```

### Commandes RAG

```bash
# 1. Activer pgvector (une seule fois)
docker exec -it postgres_db psql -U laravel -d kiprix_db \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 2. Vectoriser
python main.py rag vectorize
python main.py rag vectorize --territory mq --clear

# 3. Poser des questions
python main.py rag ask "Produits les moins chers en Martinique ?" --territory mq
python main.py rag ask "Compare les prix de l'huile" --sources
python main.py rag ask "Résumé des données" --provider openai --model gpt-4o-mini

# 4. Mode interactif
python main.py rag interactive --territory mq

# 5. Stats
python main.py rag stats
```

### HybridRAGEngine — Détection d'intention

| Intent | Mots-clés déclencheurs | Stratégie |
|--------|----------------------|-----------|
| **Analytique** | moins cher, plus cher, comparer, écart, trouver... | Requête SQL directe |
| **Sémantique** | autres questions | Recherche vectorielle pgvector |

---

## 🏛️ Architecture POO

### `BaseScraper` (Classe abstraite)
- Méthodes abstraites : `scrape()`, `parse()`
- Méthodes concrètes : `fetch_page()` (Selenium), `save_to_json()`, `save_to_csv()`

### `KiprixScraper(BaseScraper)`
- Scraping paginé de kiprix.com
- Extraction : nom, prix France, prix DOM, écart %, quantité, prix unitaire
- `get_products_by_category()`, `get_average_price_difference()`, `scrape_all_territories()`

### `ScraperManager` (Pattern Factory)
- `create_scraper(name)` — création dynamique
- Scraping séquentiel et parallèle (ThreadPoolExecutor)

### `CacheManager`
- Cache fichiers JSON avec expiration configurable
- Hash MD5 des URLs, nettoyage automatique

### `DataAnalyzer`
- Statistiques descriptives avec pandas
- Analyse écarts de prix France/DOM
- Export Excel et CSV, rapport textuel

### `DBManager`
- Connexion PostgreSQL via psycopg2
- Création automatique de la table `produits`
- Insertion batch avec `executemany`

---

## 🗄️ Tables PostgreSQL

```sql
-- Produits scrapés
CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT, price_france VARCHAR(50), price_dom VARCHAR(50),
    difference VARCHAR(50), quantity_value NUMERIC(10,4),
    quantity_unit VARCHAR(20), unit_reference VARCHAR(20),
    unit_price_france NUMERIC(10,2), unit_price_dom NUMERIC(10,2),
    territory VARCHAR(10), territory_name VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Embeddings RAG
CREATE TABLE produits_embeddings (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER REFERENCES produits(id),
    chunk_text TEXT NOT NULL,
    embedding vector(768),
    territory VARCHAR(10),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧪 Tests

```bash
pytest
pytest --cov=src
pytest tests/test_kiprix_scraper.py -v
```

**Couverture : 72%** — modules testés : base_scraper, kiprix_scraper, manager, cache, analyzer

---

## 🔗 Intégrations avec les autres projets

### Avec backend-2026 (karibmarket-api) — lancé en subprocess + import direct

```bash
# Via subprocess (scraping)
$SCRAPER_PYTHON main.py scrape --territory mq --pages 1 --format db

# Via import direct (chatbot RAG)
from src.rag.hybrid_rag import HybridRAGEngine
```

### Flux global

```
web3 (Next.js) → karibmarket-api (FastAPI) → groupe_scp2 (subprocess)
                         ↓                           ↓
                     kiprix_db  ←────────────────────┘
                         ↓
                   pgvector (RAG) → Ollama → chatbot
```

---

## 🐳 Docker

```bash
docker build -t kiprix-scraper .
docker run kiprix-scraper python main.py scrape --pages 1 --territory mq
docker run -v ${PWD}/data:/app/data kiprix-scraper python main.py scrape --pages 2 --territory gp

cd docker && docker-compose up -d
```

---

## 📦 Stack technique

| Technologie | Usage |
|-------------|-------|
| Python 3.11+ | Langage principal |
| Selenium + BeautifulSoup | Scraping anti-bot |
| pandas | Analyse données |
| psycopg2 | Driver PostgreSQL |
| pgvector | Stockage embeddings |
| sentence-transformers | Modèle embeddings multilingue (768 dims) |
| Ollama (llama3/mistral) | LLM local |
| OpenAI API | LLM cloud (fallback) |
| Click | Interface CLI |
| pytest | Tests unitaires |
| Docker | Containerisation |