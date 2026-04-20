# poo-2026

Programmation Orientee Objet Python 2026.

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