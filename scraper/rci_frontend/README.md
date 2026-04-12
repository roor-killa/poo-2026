# Interface RCI (Flask)

Ce dossier contient l'interface web et le serveur Flask pour le scraper RCI.

## Prerequis

- Python 3.10+
- PowerShell (Windows)

## Lancer le serveur frontend

Depuis le dossier racine du projet (celui qui contient `rci_frontend/` et `src/`) :

```powershell
cd "C:\Users\gote7\MY_DISK_DOCUMENTS\Licence\L2 Informatique\Semestre 4\POO\poo-2026\scraper"

py -m pip install -r requirements.txt
py -m pip install -r rci_frontend\requirements.txt

$env:PYTHONPATH = (Get-Location).Path

py rci_frontend\server.py
```

Quand le serveur demarre, ouvrez :

- http://localhost:5000

## Arreter le serveur

Appuyez sur `Ctrl + C` dans le terminal.

## Depannage rapide

- Si vous voyez `ModuleNotFoundError: No module named 'src'`, verifiez que :
  - Vous etes dans le dossier racine du projet.
  - Vous avez execute `$env:PYTHONPATH = (Get-Location).Path` dans le meme terminal.
- Si le port 5000 est deja utilise, arretez l'autre processus qui utilise ce port puis relancez.
