from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

from scrapers.business_scraper import BusinessScraper
from scrapers.event_scraper import EventScraper
from scrapers.news_scraper import NewScraper


app = FastAPI(title="bizouk scraper api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def run_business():
    scraper = BusinessScraper()
    try:
        data = scraper.scrape()
        with open(DATA_DIR / "business.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        scraper.close()


def run_news():
    scraper = NewScraper(category="soirees/agenda/region/martinique")
    try:
        data = scraper.scrape(max_pages=2)
        with open(DATA_DIR / "news.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        scraper.close()


def run_events(pages: int = 1, region: str = "martinique", limit: int = 12):
    scraper = EventScraper(region=region)
    try:
        data = scraper.scrape(max_pages=pages, include_details=True, max_events=limit)
        with open(DATA_DIR / "events.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    finally:
        scraper.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/scrape/business")
def scrape_business():
    data = run_business()
    return {
        "type": "business",
        "count": len(data),
        "data": data
    }


@app.get("/scrape/news")
def scrape_news():
    data = run_news()
    return {
        "type": "news",
        "count": len(data),
        "data": data
    }


@app.get("/scrape/events")
def scrape_events(
    pages: int = Query(default=1, ge=1, le=10),
    region: str = Query(default="martinique", min_length=2, max_length=50),
    limit: int = Query(default=12, ge=1, le=100),
):
    data = run_events(pages=pages, region=region, limit=limit)
    return {
        "type": "events",
        "region": region,
        "pages": pages,
        "limit": limit,
        "count": len(data),
        "data": data
    }


@app.get("/files/{name}")
def get_file(name: str):
    file_path = DATA_DIR / name
    if not file_path.exists():
        return {"error": "fichier introuvable"}

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    return {
        "filename": name,
        "data": content
    }
