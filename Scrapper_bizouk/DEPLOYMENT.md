# Deploiement VPS

Cette application n'est pas un site statique a copier dans `public_html`.
Elle utilise trois services Docker:

- `RL_bizouk_backend`: API FastAPI et scraper Python.
- `RL_bizouk_frontend`: interface Next.js.
- `RL_bizouk_nginx`: proxy interne de l'application.

Le conteneur nginx de l'app ecoute sur `127.0.0.1:3005`.

## 1. Verifier le VPS

Une fois connecte au VPS:

```bash
docker --version
docker compose version
groups
pwd
ls -la
```

Si `docker` ne fonctionne pas pour l'utilisateur `rosambert`, il faut que le prof donne l'acces Docker ou lance les commandes avec un compte autorise.

Pour eviter les coupures SSH:

```bash
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=5 rosambert@37.187.236.58
```

## 2. Mettre le code sur le VPS

Il y a deux manieres de mettre a jour le VPS.
Pour un vrai flux proche CI/CD, la methode Git est la plus propre.

### Option A - Methode Git recommandee

Sur ton PC:

```powershell
git add .
git commit -m "securise et documente scrapper bizouk"
git push origin rosambert
```

Sur le VPS, une premiere fois:

```bash
cd ~
git clone -b rosambert https://github.com/roor-killa/poo-2026.git RL_poo_2026
cd ~/RL_poo_2026/Scrapper_bizouk
mkdir -p data
cp -n .env.example .env
```

Pour les mises a jour suivantes sur le VPS:

```bash
cd ~/RL_poo_2026/Scrapper_bizouk
git pull origin rosambert
docker compose -f docker-compose.prod.yml up -d --build
curl http://127.0.0.1:3005/api/health
```

Cette methode est meilleure que copier-coller le projet, parce que le VPS recupere exactement les commits de ta branche.

### Option B - Methode archive temporaire

Depuis le terminal VS Code PowerShell, sur le PC:

```powershell
cd C:\Users\yukii\Documents\CODE_L1\CODE_L2\OBJET\depot\poo-2026
tar -czf RL_scrapper_bizouk_update.tar.gz -C .\Scrapper_bizouk .
scp .\RL_scrapper_bizouk_update.tar.gz rosambert@37.187.236.58:~/
```

Puis dans Git Bash/SSH sur le VPS:

```bash
mkdir -p ~/RL_scrapper_bizouk
tar -xzf ~/RL_scrapper_bizouk_update.tar.gz -C ~/RL_scrapper_bizouk
cd ~/RL_scrapper_bizouk
mkdir -p data
cp -n .env.example .env
```

Cette methode marche pour depanner, mais elle n'est pas ideale pour montrer du CI/CD.

## 3. Configurer les secrets

Le fichier `.env` du VPS doit contenir les vraies valeurs de production.
Il ne doit jamais etre commit.

Pour generer une cle API forte sur le VPS:

```bash
sed -i "s/^SCRAPER_API_KEY=.*/SCRAPER_API_KEY=$(openssl rand -hex 32)/" .env
```

Pour lire la cle a saisir dans l'interface:

```bash
grep '^SCRAPER_API_KEY=' .env
```

## 4. Lancer l'application

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
curl http://127.0.0.1:3005/api/health
```

Test d'une route protegee:

```bash
API_KEY=$(grep '^SCRAPER_API_KEY=' .env | cut -d= -f2-)
curl -H "X-API-Key: $API_KEY" "http://127.0.0.1:3005/api/scrape/events?pages=1&region=martinique&limit=1"
```

## 5. Brancher l'URL

Pour que `https://rosambert.nsdy.be` affiche l'app Docker, le serveur web du VPS doit faire un reverse proxy vers:

```text
http://127.0.0.1:3005
```

Exemple Nginx:

```nginx
server {
    listen 80;
    server_name rosambert.nsdy.be;

    location / {
        proxy_pass http://127.0.0.1:3005;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Si le prof ne donne pas acces a la configuration Nginx/Apache du VPS, `public_html` ne suffit pas pour cette app complete.
Il faut soit demander au prof de configurer le reverse proxy, soit exposer temporairement le port `3005` publiquement.

## 6. Vers un vrai CI/CD

Le CI/CD veut dire que le deploiement part automatiquement de GitHub.
Le schema propre serait:

1. tu modifies le code sur ta branche `rosambert`;
2. tu fais `git push origin rosambert`;
3. GitHub Actions se connecte au VPS en SSH;
4. le VPS fait `git pull origin rosambert`;
5. Docker reconstruit et relance les conteneurs.

Il ne faut pas mettre le mot de passe SSH dans Git.
Pour automatiser proprement, il faut utiliser des secrets GitHub Actions:

- `VPS_HOST`: `37.187.236.58`
- `VPS_USER`: `rosambert`
- `VPS_SSH_KEY`: cle privee SSH autorisee sur le VPS
- `VPS_PROJECT_PATH`: chemin du projet sur le VPS

Le fichier `.env` doit rester uniquement sur le VPS.
GitHub ne doit jamais contenir les vraies cles API ou mots de passe.
