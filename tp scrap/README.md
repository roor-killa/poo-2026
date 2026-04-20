# Bizouk Events Scraper

Architecture Docker pour scraper les evenements publics de [Bizouk](https://www.bizouk.com), stocker les donnees dans PostgreSQL, exposer une API FastAPI et afficher un site Laravel.

## Services

```text
PostgreSQL :5432  <- base de donnees
FastAPI    :8000  <- API REST + scraper Bizouk
Laravel    :80    <- interface web + dashboard
```

## Demarrage rapide

```bash
docker compose up --build
```

Une fois les conteneurs lances :

- Evenements : http://localhost
- Dashboard : http://localhost/dashboard
- API FastAPI : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## Scraper Bizouk

Le scraper utilise :

- la page publique `https://www.bizouk.com/?region=martinique` pour recuperer les cartes evenement ;
- les pages detail `https://www.bizouk.com/events/details/...` pour lire les donnees structurees `schema.org/Event`.

Lancer le scraping depuis l'API :

```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d "{\"regions\":[\"martinique\"],\"max_per_region\":30,\"fetch_details\":true}"
```

## API utile

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/api/events?page=1&region=martinique"
curl http://localhost:8000/api/event-types
curl http://localhost:8000/api/stats
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
