# Interface RCI (Flask)

Ce dossier contient l'interface web et le serveur Flask relies au scraper RCI.

## Prerequis

- Utiliser le .venv central situe a la racine du repo
- Windows + PowerShell

## Installation (une seule fois)

Depuis la racine du projet:

```powershell
cd "C:\Users\gote7\MY_DISK_DOCUMENTS\Licence\L2 Informatique\Semestre 4\POO\poo-2026"
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\scraper\requirements.txt
python -m pip install -r .\scraper\rci_frontend\requirements.txt
```

## Lancer le serveur

```powershell
cd .\scraper
python .\rci_frontend\server.py
```

Ouvrir ensuite: http://localhost:5000

## Arreter le serveur

Appuyer sur Ctrl + C dans le terminal.

## Depannage rapide

- Erreur ModuleNotFoundError sur src: lancer la commande depuis le dossier scraper.
- Port 5000 deja pris: fermer le processus qui utilise le port puis relancer.
