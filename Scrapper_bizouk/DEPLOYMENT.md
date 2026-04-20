# Deploiement VPS

Cette application n'est pas un site statique a copier dans `public_html`.
Elle utilise trois services Docker:

- `RL_bizouk_backend`: API FastAPI et scraper Python.
- `RL_bizouk_frontend`: interface Next.js.
- `RL_bizouk_nginx`: proxy interne de l'application.

## Verification SSH

Une fois connecte au VPS:

```bash
docker --version
docker compose version
groups
pwd
ls -la
```

Si `docker` ne fonctionne pas pour l'utilisateur `rosambert`, il faut que le prof donne l'acces Docker ou lance les commandes avec un compte autorise.

## Envoi du projet

Depuis Windows, a lancer dans PowerShell depuis le dossier parent du projet:

```powershell
scp -r .\Scrapper_bizouk rosambert@37.187.236.58:~/RL_scrapper_bizouk
```

Ou depuis Git Bash:

```bash
scp -r ./Scrapper_bizouk rosambert@37.187.236.58:~/RL_scrapper_bizouk
```

## Lancement sur le VPS

```bash
cd ~/RL_scrapper_bizouk
mkdir -p data
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
```

Le conteneur nginx de l'app ecoute sur `127.0.0.1:3005`.

## Branchement de l'URL

Pour que `https://rosambert.nsdy.be` affiche l'app Docker, le serveur web du VPS doit faire un reverse proxy vers:

```text
http://127.0.0.1:3005
```

Si le serveur utilise Nginx, exemple de bloc:

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

Si le prof ne donne pas acces a la configuration Nginx/Apache du VPS, `public_html` ne suffira pas pour cette app complete. Dans ce cas, il faut soit demander au prof de configurer le reverse proxy, soit exposer temporairement le port `3005` publiquement.

## Mise a jour

Apres modification du code:

```bash
cd ~/RL_scrapper_bizouk
docker compose -f docker-compose.prod.yml up -d --build
```
