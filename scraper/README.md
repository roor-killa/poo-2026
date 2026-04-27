# poo-2026

Programmation Orientee Objet Python 2026.

## Deploiement Docker (Linux / VPS)

Si vous voyez une erreur `KeyError: 'ContainerConfig'` avec `docker-compose==1.29.2`, c'est un probleme connu de **Docker Compose v1**. La solution est d'utiliser **Docker Compose v2** (plugin) et la commande `docker compose`.

Sur Debian/Ubuntu (VPS):

```bash
# 1) Verifier les versions
docker version
docker-compose version || true
docker compose version || true

# 2) Installer Compose v2 (plugin)
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# (optionnel) enlever l'ancien docker-compose v1 s'il est installe via apt
sudo apt-get remove -y docker-compose || true

# (optionnel) pour enlever l'avertissement "legacy builder", installer buildx
sudo apt-get install -y docker-buildx-plugin

# 3) Nettoyer les conteneurs/volumes de ce projet puis relancer
cd scraper

# IMPORTANT (VPS partage entre etudiants):
# - utiliser un nom de projet unique pour isoler reseau/volumes: -p <votre_nom>
# - choisir des ports hote differents dans .env (POSTGRES_PORT, FRONTEND_PORT, NGINX_PORT)

docker compose -p <votre_nom> down --remove-orphans
docker compose -p <votre_nom> up -d --build
```

## Environnement Python centralise

Le projet utilise un seul environnement virtuel a la racine du repo: .venv.

### 1) Activer le .venv (PowerShell)

```powershell
cd "C:\Users\gote7\MY_DISK_DOCUMENTS\Licence\L2 Informatique\Semestre 4\POO\poo-2026"
.\.venv\Scripts\Activate.ps1
```

### 2) Installer les dependances du scraper + frontend

```powershell
python -m pip install -r .\scraper\requirements.txt
python -m pip install -r .\scraper\rci_frontend\requirements.txt
```

## Lancer le frontend RCI

```powershell
cd .\scraper
python .\rci_frontend\server.py
```

Puis ouvrir http://localhost:5000.

## Lancer les tests

Depuis .\scraper:

```powershell
python -m pytest -q
```

Tests cibles RCI:

```powershell
python -m pytest tests/test_rci_scraper.py tests/test_documents.py -k RCI -q
```

## RAG DB (chunk_rci_to_rag)

Le script .\scraper\db\chunk_rci_to_rag.py:

- lit les articles depuis rc_schema.rci_articles
- cree ou met a jour rag_documents (upsert)
- decoupe le texte en chunks
- remplace les chunks d'un document dans rag_chunks

Usage typique:

```powershell
cd .\scraper\db
python .\chunk_rci_to_rag.py --help
```