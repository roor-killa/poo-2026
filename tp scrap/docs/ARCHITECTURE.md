# Architecture du programme

## Vue d'ensemble

Le programme est decoupe en trois services Docker :

```text
Navigateur
  |
  v
Laravel :89
  |
  v
FastAPI :8009
  |
  v
PostgreSQL :5432
```

Laravel gere l'interface web et le dashboard. FastAPI expose les routes REST, lance le scraper en arriere-plan et ecrit les evenements dans PostgreSQL. PostgreSQL conserve les evenements Bizouk et leurs metadonnees.

## Source scrapee

Le scraper cible Bizouk :

- listing : `https://www.bizouk.com/?region=martinique`
- details : `https://www.bizouk.com/events/details/...`

Les cartes du listing donnent les URLs, titres, types, lieux, dates et images. Les pages detail contiennent du JSON-LD `schema.org/Event`, utilise en priorite pour obtenir la date ISO, le lieu, l'adresse, l'image, les offres, le prix minimum et l'organisateur.

## Structure

```text
.
|-- docker-compose.yml
|-- .env.example
|-- db/
|   `-- init.sql
|-- fastapi/
|   |-- Dockerfile
|   |-- requirements.txt
|   |-- main.py
|   `-- scrapers/
|       |-- __init__.py
|       |-- base_scraper.py
|       `-- event_scraper.py
|-- laravel/
|   |-- Dockerfile
|   |-- app/Http/Controllers/
|   |   |-- DashboardController.php
|   |   `-- EventController.php
|   |-- routes/
|   |   `-- web.php
|   `-- resources/views/
|       |-- layouts/app.blade.php
|       |-- events/index.blade.php
|       |-- events/show.blade.php
|       `-- dashboard/index.blade.php
`-- docs/
    `-- ARCHITECTURE.md
```

## Responsabilites

PostgreSQL cree la table `events`, indexe les champs utiles et garde `source_url` unique pour eviter les doublons.

FastAPI expose les routes REST :

- `GET /health`
- `GET /api/events`
- `GET /api/events/{id}`
- `GET /api/event-types`
- `GET /api/stats`
- `POST /api/scrape`

Le scraper Python `BizoukEventScraper` lit les cartes publiques Bizouk puis enrichit chaque evenement avec les donnees structurees des pages detail.

Laravel consomme FastAPI pour afficher la liste des evenements, les details et le dashboard.

## Flux principal

1. L'utilisateur ouvre `http://localhost:89`.
2. Laravel appelle `http://fastapi:8000/api/events`.
3. FastAPI lit PostgreSQL et renvoie les evenements.
4. Laravel affiche la liste et les filtres par type.
5. Depuis le dashboard, Laravel appelle `POST /api/scrape`.
6. FastAPI lance `BizoukEventScraper`, puis insere ou met a jour les resultats.

## Demarrage

```bash
docker compose up --build
```

Puis :

- Evenements : `http://localhost:89`
- Dashboard : `http://localhost:89/dashboard`
- API : `http://localhost:8009`
- Documentation API : `http://localhost:8009/docs`
