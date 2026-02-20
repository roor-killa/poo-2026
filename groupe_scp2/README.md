# TP Scraping — Groupe 2 | Kiprix.com

Projet de web scraping orienté objet — Licence 2 Informatique, UA.  
Site scrappé : **kiprix.com** (comparateur de prix France / DOM).

---

## 🏗️ Architecture

```
tp_scraping/
├── src/
│   ├── base_scraper.py        # Classe abstraite (Membre 1)
│   ├── manager.py             # ScraperManager / Factory (Membre 1)
│   ├── analyzer.py            # DataAnalyzer / pandas (Membre 2)
│   ├── cache.py               # CacheManager (Membre 1)
│   └── scrapers/
│       └── kiprix_scraper.py  # KiprixScraper (Membre 1 + 2)
├── tests/                     # Tests unitaires (Membre 3)
├── notebooks/                 # Analyse Jupyter (Membre 2)
├── docker/                    # Dockerfile + Compose (Membre 3)
├── docs/                      # UML + Documentation PDF (Membre 3)
└── main.py                    # CLI (Membre 1)
```

---

## 🚀 Installation

```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```

## 💻 Utilisation

```bash
# Scraper Kiprix (Guadeloupe, 5 pages)
python main.py scrape --pages 5 --territory gp

# Scraper en Martinique, sauvegarder en JSON + CSV
python main.py scrape --pages 10 --territory mq --format both

# Analyser les données
python main.py analyze data/raw/kiprix_gp.json

# Exporter en Excel
python main.py analyze data/raw/kiprix_gp.json --export excel

# Cache
python main.py cache-stats
python main.py cache-clear
```

## 🧪 Tests

```bash
pytest                         # Lancer les tests
pytest --cov=src               # Avec rapport de couverture
```

## 🐳 Docker

```bash
docker build -t tp-kiprix -f docker/Dockerfile .
docker run -v $(pwd)/data:/app/data tp-kiprix scrape --pages 5
```

---

## 👥 Équipe

| Membre | Responsabilité |
|--------|---------------|
| Membre 1 | `BaseScraper`, `KiprixScraper` (core), `ScraperManager`, `CacheManager`, CLI |
| Membre 2 | `KiprixScraper` (méthodes avancées), `DataAnalyzer`, Notebook Jupyter |
| Membre 3 | Tests unitaires (>70% coverage), Docker, Diagramme UML, Documentation PDF |

---

**Date de rendu :** 4 mars 2026
