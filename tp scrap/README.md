# Bizouk Events Scraper

Architecture Docker pour scraper les evenements publics de [Bizouk](https://www.bizouk.com), stocker les donnees dans PostgreSQL, exposer une API FastAPI et afficher un site Laravel.

## Services

```text
PostgreSQL :5409  <- base de donnees exposee sur la machine
FastAPI    :8009  <- API REST + scraper Bizouk
Laravel    :3009  <- interface web + dashboard
Laravel    :89    <- interface web alternative
```

## Demarrage rapide

```bash
docker compose up --build
```

Une fois les conteneurs lances :

- Evenements : http://localhost:3009
- Dashboard : http://localhost:3009/dashboard
- Interface alternative : http://localhost:89
- API FastAPI : http://localhost:8009
- Documentation API : http://localhost:8009/docs

## Scraper Bizouk

Le scraper utilise :

- la page publique `https://www.bizouk.com/?region=martinique` pour recuperer les cartes evenement ;
- les pages detail `https://www.bizouk.com/events/details/...` pour lire les donnees structurees `schema.org/Event`.

Lancer le scraping depuis l'API :

```bash
curl -X POST http://localhost:8009/api/scrape \
  -H "Content-Type: application/json" \
  -d "{\"regions\":[\"martinique\"],\"max_per_region\":30,\"fetch_details\":true}"
```

## API utile

```bash
curl http://localhost:8009/health
curl "http://localhost:8009/api/events?page=1&region=martinique"
curl http://localhost:8009/api/event-types
curl http://localhost:8009/api/stats
```

## Structure

```text
.
|-- docker-compose.yml
|-- db/
|   `-- init.sql
|-- fastapi/
|   |-- Dockerfile
|   |-- requirements.txt
|   |-- main.py
|   `-- scrapers/
|       |-- base_scraper.py
|       `-- event_scraper.py
|-- laravel/
|   |-- Dockerfile
|   |-- app/Http/Controllers/
|   |-- routes/
|   `-- resources/views/
`-- docs/
    `-- ARCHITECTURE.md
```

## Note

Le fichier `robots.txt` de Bizouk autorise l'acces public general, mais bloque notamment `/api/`, `/admin/`, `/account/` et plusieurs bots d'IA. Le scraper reste sur les pages publiques autorisees et conserve un delai entre les requetes.
