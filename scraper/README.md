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

# Ports attendus (hôte):
# - PostgreSQL : 5111
# - Frontend   : 8111
# - Nginx      : 81
#
# Astuce: copier .env.example -> .env pour fixer ces ports et la config DB.

# IMPORTANT (VPS partage entre etudiants):
# - utiliser un nom de projet unique pour isoler reseau/volumes: -p <votre_nom>
# - choisir des ports hote differents dans .env (POSTGRES_PORT, FRONTEND_PORT, NGINX_PORT)

docker compose -p <votre_nom> down --remove-orphans
docker compose -p <votre_nom> up -d --build
```

### Exposer sur un domaine HTTPS (ex: https://gombs.nasdy.be/)

Le stack ci-dessus expose l'app en HTTP sur le VPS (nginx du projet). Pour servir un **domaine en HTTPS** sur le port 443, il faut un **reverse proxy** qui termine TLS et redirige vers votre nginx applicatif.

#### Option A — Reverse proxy systeme (Nginx/Apache) + Let's Encrypt (root requis)

1) Démarrer votre stack (en gardant nginx applicatif sur le port hôte 81) :

```bash
cd scraper
docker compose -p <votre_nom> up -d --build
curl -I http://127.0.0.1:81/
```

2) Sur le VPS, configurer le Nginx **système** pour proxyfier le domaine vers `127.0.0.1:81`.
Exemple de vhost (à adapter):

```nginx
server {
	listen 80;
	server_name gombs.nasdy.be;

	location / {
		proxy_pass http://127.0.0.1:81;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

3) Générer le certificat Let's Encrypt (ex: `certbot --nginx -d gombs.nasdy.be`).

#### Option B — 100% Docker (Caddy) (pas de sudo, mais ports 80/443 doivent être libres)

Si vous n'avez pas sudo mais que vous pouvez utiliser Docker, vous pouvez faire terminer TLS par un conteneur (Caddy) et le faire proxyfier vers le nginx applicatif (port 81 dans le réseau Docker).

Prérequis:
- Le DNS `gombs.nasdy.be` pointe vers l'IP du VPS.
- Les ports 80 et 443 sont libres sur le VPS.

Principe Caddyfile minimal:

```caddy
gombs.nasdy.be {
	reverse_proxy nginx-81:81
}
```

Ensuite démarrer Caddy sur le même réseau docker-compose (ou via un second compose qui join le réseau du projet).


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