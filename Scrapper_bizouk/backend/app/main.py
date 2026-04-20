"""
Backend FastAPI du projet Scrapper Bizouk.

Ce fichier est le point d'entree de l'API Dockerisee:
- il expose les routes HTTP appelees par le frontend Next.js;
- il lance les scrapers Python;
- il sauvegarde les resultats dans le dossier data/;
- il applique les protections vues en CM9: cle API, CORS, rate limiting et logs.
"""

from collections import defaultdict, deque
from fastapi import Depends
from fastapi import Query
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import hmac
import json
import logging
import os
import time

from scrapers.business_scraper import BusinessScraper
from scrapers.event_scraper import EventScraper
from scrapers.news_scraper import NewScraper


# Objet principal FastAPI: il contient toutes les routes HTTP exposees par le backend.
app = FastAPI(title="bizouk scraper api")

# Logger dedie aux evenements de securite utiles pour CM9:
# tentative sans cle API, depassement du rate limit, configuration manquante.
security_logger = logging.getLogger("security")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# Parametres de limitation de requetes configurables depuis le fichier .env.
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))

# Stockage en memoire des appels recents par IP.
# defaultdict(deque) permet d'avoir automatiquement une file vide pour chaque nouvelle IP/route.
rate_limit_hits = defaultdict(deque)


def get_cors_origins():
    """
    Lit la liste des frontends autorises a appeler l'API.

    Exemple dans .env:
    BACKEND_CORS_ORIGINS=http://localhost:3005,https://rosambert.nsdy.be
    """
    origins = os.getenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:3005,http://127.0.0.1:3005",
    )

    # On separe la variable par virgules pour obtenir une vraie liste Python.
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


def get_client_ip(request: Request) -> str:
    """Retrouve l'adresse IP du client, meme quand l'API passe par nginx."""

    # En production, nginx place souvent l'IP d'origine dans X-Forwarded-For.
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    # En local ou sans reverse proxy, FastAPI peut lire directement l'IP du client.
    if request.client:
        return request.client.host

    return "unknown"


def get_scraper_api_key() -> str:
    """Recupere la cle API depuis les variables d'environnement."""
    return os.getenv("SCRAPER_API_KEY", "").strip()


def require_api_key(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    """
    Bloque les routes protegees si le header X-API-Key est absent ou faux.

    Cette fonction est utilisee comme dependance FastAPI:
    si elle leve une HTTPException, la route n'est pas executee.
    """
    expected_key = get_scraper_api_key()
    client_ip = get_client_ip(request)

    # Sans cle serveur dans .env, on refuse l'action au lieu de laisser l'API ouverte.
    if not expected_key:
        security_logger.error("SCRAPER_API_KEY is not configured")
        raise HTTPException(status_code=503, detail="API key is not configured")

    # compare_digest evite une comparaison naive de secrets.
    if not x_api_key or not hmac.compare_digest(x_api_key, expected_key):
        security_logger.warning("Unauthorized API access from %s on %s", client_ip, request.url.path)
        raise HTTPException(status_code=401, detail="Invalid API key")


def rate_limit(request: Request):
    """
    Limite le nombre d'appels par IP et par route sur une fenetre de temps.

    Le but est d'eviter qu'un utilisateur relance trop vite le scraping,
    car chaque appel peut ouvrir plusieurs pages du site Bizouk.
    """
    client_ip = get_client_ip(request)

    # La limite est separee par route: /scrape/events et /files/events.json ont chacun leur compteur.
    key = f"{client_ip}:{request.url.path}"
    now = time.monotonic()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    hits = rate_limit_hits[key]

    # On supprime les anciens appels qui ne sont plus dans la fenetre de temps.
    while hits and hits[0] < window_start:
        hits.popleft()

    # Si la file contient deja trop d'appels recents, on bloque.
    if len(hits) >= RATE_LIMIT_MAX_REQUESTS:
        security_logger.warning("Rate limit exceeded from %s on %s", client_ip, request.url.path)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Sinon on enregistre l'appel courant.
    hits.append(now)


# Middleware CORS: seul le frontend declare dans .env peut appeler l'API depuis un navigateur.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)

# Dossier commun ou le backend sauvegarde les fichiers JSON produits par les scrapers.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# On limite volontairement les fichiers consultables pour eviter de lire n'importe quel fichier du serveur.
ALLOWED_DATA_FILES = {"business.json", "news.json", "events.json"}


def run_business():
    """Lance l'ancien scraper restaurants et sauvegarde le resultat en JSON."""
    scraper = BusinessScraper()
    try:
        # scrape() retourne une liste de dictionnaires Python.
        data = scraper.scrape()

        # Le JSON est sauvegarde pour pouvoir etre relu ou exporte plus tard.
        with open(DATA_DIR / "business.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        # La session HTTP doit toujours etre fermee, meme en cas d'erreur pendant le scraping.
        scraper.close()


def run_news():
    """Lance l'ancien scraper news/agenda et sauvegarde le resultat en JSON."""
    scraper = NewScraper(category="soirees/agenda/region/martinique")
    try:
        # max_pages garde ce scraper secondaire sous controle.
        data = scraper.scrape(max_pages=2)
        with open(DATA_DIR / "news.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        scraper.close()


def run_events(pages: int = 1, region: str = "martinique", limit: int = 12):
    """Lance le scraper principal Bizouk events avec pagination et limite de resultats."""
    scraper = EventScraper(region=region)
    try:
        # include_details=True ouvre chaque fiche evenement pour recuperer description, prix et frais.
        data = scraper.scrape(max_pages=pages, include_details=True, max_events=limit)
        with open(DATA_DIR / "events.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        scraper.close()


@app.get("/health")
def health():
    """Route publique tres simple pour verifier que le backend repond."""
    return {"status": "ok"}


# Dependances appliquees aux routes sensibles: authentification par cle + rate limit.
protected_endpoint = [Depends(require_api_key), Depends(rate_limit)]


@app.get("/scrape/business", dependencies=protected_endpoint)
def scrape_business():
    """Route API qui declenche le scraping des restaurants."""
    data = run_business()
    return {
        "type": "business",
        "count": len(data),
        "data": data
    }


@app.get("/scrape/news", dependencies=protected_endpoint)
def scrape_news():
    """Route API qui declenche le scraping de l'agenda/news."""
    data = run_news()
    return {
        "type": "news",
        "count": len(data),
        "data": data
    }


@app.get("/scrape/events", dependencies=protected_endpoint)
def scrape_events(
    # Query valide automatiquement les parametres de l'URL avant d'entrer dans la fonction.
    pages: int = Query(default=1, ge=1, le=10),
    region: str = Query(default="martinique", min_length=2, max_length=50, pattern="^[a-z0-9-]+$"),
    limit: int = Query(default=12, ge=1, le=100),
):
    """Route API principale utilisee par le frontend pour scraper les evenements Bizouk."""
    data = run_events(pages=pages, region=region, limit=limit)
    return {
        "type": "events",
        "region": region,
        "pages": pages,
        "limit": limit,
        "count": len(data),
        "data": data
    }


@app.get("/files/{name}", dependencies=protected_endpoint)
def get_file(name: str):
    """Renvoie un fichier JSON deja genere, en refusant les noms non autorises."""

    # Protection simple contre un nom de fichier malveillant du type ../../.env.
    if name not in ALLOWED_DATA_FILES:
        raise HTTPException(status_code=400, detail="Unsupported file")

    file_path = DATA_DIR / name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    return {
        "filename": name,
        "data": content
    }
