# Commandes Rapides Pour Les Tests

Le projet utilise le .venv central a la racine du repo.

## 1) Activer l'environnement virtuel (PowerShell)

```powershell
cd "C:\Users\gote7\MY_DISK_DOCUMENTS\Licence\L2 Informatique\Semestre 4\POO\poo-2026"
.\.venv\Scripts\Activate.ps1
cd .\scraper
```

## 2) Installer les dépendances

```powershell
python -m pip install -r requirements.txt
```

## 3) Lancer tous les tests

```powershell
python -m pytest -q
```

## 4) Lancer seulement les tests RCI (rapide)

```powershell
python -m pytest tests/test_rci_scraper.py tests/test_documents.py -k RCI -q
```

## 5) Lancer les tests d'intégration (optionnel)

Démarrez d'abord la base Docker, puis lancez :

```powershell
docker compose up -d db
python -m pytest tests/test_db_integration.py -v -m integration
```

## Notes

- "deselected" signifie que les tests ont été trouvés, mais filtrés par -k.
- "skipped" signifie qu'un test a été volontairement ignoré (par exemple, prérequis d'intégration manquants).
