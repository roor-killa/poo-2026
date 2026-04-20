from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from typing import Optional
import json
import os

from scrapers.event_scraper import BizoukEventScraper


app = FastAPI(
    title="Bizouk Events API",
    description="API pour scraper et consulter les evenements publics de Bizouk.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bizouk:bizouk_secret@db:5432/bizouk")
engine = create_engine(DATABASE_URL)


def ensure_schema() -> None:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                source_id VARCHAR(64) UNIQUE,
                source_url TEXT UNIQUE NOT NULL,
                title VARCHAR(255) NOT NULL,
                event_type VARCHAR(120),
                region VARCHAR(120),
                venue VARCHAR(255),
                address TEXT,
                city VARCHAR(120),
                country VARCHAR(80),
                start_date TIMESTAMPTZ,
                end_date TIMESTAMPTZ,
                description TEXT,
                image_url TEXT,
                organizer VARCHAR(255),
                min_price NUMERIC(10, 2),
                currency VARCHAR(10),
                offers JSONB DEFAULT '[]'::jsonb,
                contact_phone VARCHAR(80),
                contact_email VARCHAR(255),
                website TEXT,
                scraped_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS events_source_id_uidx ON events (source_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS events_start_date_idx ON events (start_date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS events_region_idx ON events (region)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS events_type_idx ON events (event_type)"))


@app.on_event("startup")
def on_startup() -> None:
    ensure_schema()


class EventOut(BaseModel):
    id: int
    source_id: Optional[str] = None
    source_url: str
    title: str
    event_type: Optional[str] = None
    region: Optional[str] = None
    venue: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    organizer: Optional[str] = None
    min_price: Optional[float] = None
    currency: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    scraped_at: Optional[str] = None


class ScrapeRequest(BaseModel):
    regions: Optional[list[str]] = None
    max_per_region: int = Field(default=30, ge=1, le=200)
    fetch_details: bool = True


class ScrapeResult(BaseModel):
    status: str
    message: str
    count: int = 0


def row_to_event(row) -> dict:
    return {
        "id": row[0],
        "source_id": row[1],
        "source_url": row[2],
        "title": row[3],
        "event_type": row[4],
        "region": row[5],
        "venue": row[6],
        "address": row[7],
        "city": row[8],
        "country": row[9],
        "start_date": row[10],
        "end_date": row[11],
        "description": row[12],
        "image_url": row[13],
        "organizer": row[14],
        "min_price": float(row[15]) if row[15] is not None else None,
        "currency": row[16],
        "contact_phone": row[17],
        "contact_email": row[18],
        "website": row[19],
        "scraped_at": row[20],
    }


def upsert_event(conn, item: dict) -> None:
    if not item.get("source_id") or not item.get("source_url") or not item.get("title"):
        return

    conn.execute(text("""
        INSERT INTO events (
            source_id, source_url, title, event_type, region, venue, address, city,
            country, start_date, end_date, description, image_url, organizer,
            min_price, currency, offers, contact_phone, contact_email, website
        )
        VALUES (
            :source_id, :source_url, :title, :event_type, :region, :venue, :address,
            :city, :country, :start_date, :end_date, :description, :image_url,
            :organizer, :min_price, :currency, CAST(:offers AS JSONB),
            :contact_phone, :contact_email, :website
        )
        ON CONFLICT (source_id) DO UPDATE SET
            source_id = COALESCE(EXCLUDED.source_id, events.source_id),
            source_url = EXCLUDED.source_url,
            title = EXCLUDED.title,
            event_type = EXCLUDED.event_type,
            region = EXCLUDED.region,
            venue = EXCLUDED.venue,
            address = EXCLUDED.address,
            city = EXCLUDED.city,
            country = EXCLUDED.country,
            start_date = EXCLUDED.start_date,
            end_date = EXCLUDED.end_date,
            description = EXCLUDED.description,
            image_url = EXCLUDED.image_url,
            organizer = EXCLUDED.organizer,
            min_price = EXCLUDED.min_price,
            currency = EXCLUDED.currency,
            offers = EXCLUDED.offers,
            contact_phone = EXCLUDED.contact_phone,
            contact_email = EXCLUDED.contact_email,
            website = EXCLUDED.website,
            updated_at = NOW()
    """), {
        "source_id": item.get("source_id"),
        "source_url": item.get("source_url"),
        "title": item.get("title"),
        "event_type": item.get("event_type"),
        "region": item.get("region"),
        "venue": item.get("venue"),
        "address": item.get("address"),
        "city": item.get("city"),
        "country": item.get("country"),
        "start_date": item.get("start_date"),
        "end_date": item.get("end_date"),
        "description": item.get("description"),
        "image_url": item.get("image_url"),
        "organizer": item.get("organizer"),
        "min_price": item.get("min_price"),
        "currency": item.get("currency"),
        "offers": json.dumps(item.get("offers") or [], ensure_ascii=False),
        "contact_phone": item.get("contact_phone"),
        "contact_email": item.get("contact_email"),
        "website": item.get("website"),
    })


def run_scraper(regions: Optional[list[str]], max_per_region: int, fetch_details: bool) -> None:
    scraper = BizoukEventScraper(delay=2.0)
    try:
        results = scraper.scrape(
            regions=regions,
            max_per_region=max_per_region,
            fetch_details=fetch_details,
        )

        ensure_schema()
        with engine.begin() as conn:
            for item in results:
                upsert_event(conn, item)

        print(f"[SCRAPER] {len(results)} evenements inseres ou mis a jour.")
    finally:
        scraper.close()


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Bizouk Events API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    try:
        ensure_schema()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB unreachable: {exc}")


@app.get("/api/events", response_model=dict, tags=["Events"])
def list_events(
    page: int = Query(1, ge=1),
    per_page: int = Query(24, ge=1, le=100),
    region: Optional[str] = None,
    event_type: Optional[str] = None,
    search: Optional[str] = None,
):
    ensure_schema()
    offset = (page - 1) * per_page
    where_clauses = []
    params: dict = {"limit": per_page, "offset": offset}

    if region:
        where_clauses.append("region = :region")
        params["region"] = region

    if event_type:
        where_clauses.append("event_type = :event_type")
        params["event_type"] = event_type

    if search:
        where_clauses.append("""
            (
                title ILIKE :search OR description ILIKE :search OR
                venue ILIKE :search OR city ILIKE :search
            )
        """)
        params["search"] = f"%{search}%"

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    query = text(f"""
        SELECT id, source_id, source_url, title, event_type, region, venue,
               address, city, country, start_date::text, end_date::text,
               description, image_url, organizer, min_price, currency,
               contact_phone, contact_email, website, scraped_at::text
        FROM events
        {where_sql}
        ORDER BY start_date NULLS LAST, scraped_at DESC
        LIMIT :limit OFFSET :offset
    """)

    count_query = text(f"SELECT COUNT(*) FROM events {where_sql}")
    count_params = {k: v for k, v in params.items() if k not in ("limit", "offset")}

    with engine.connect() as conn:
        rows = conn.execute(query, params).fetchall()
        total = conn.execute(count_query, count_params).scalar() or 0

    return {
        "data": [row_to_event(row) for row in rows],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


@app.get("/api/events/{event_id}", response_model=EventOut, tags=["Events"])
def get_event(event_id: int):
    ensure_schema()
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT id, source_id, source_url, title, event_type, region, venue,
                   address, city, country, start_date::text, end_date::text,
                   description, image_url, organizer, min_price, currency,
                   contact_phone, contact_email, website, scraped_at::text
            FROM events
            WHERE id = :id
        """), {"id": event_id}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Evenement introuvable")

    return row_to_event(row)


@app.get("/api/event-types", tags=["Events"])
def list_event_types():
    ensure_schema()
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT event_type, COUNT(*) AS count
            FROM events
            WHERE event_type IS NOT NULL
            GROUP BY event_type
            ORDER BY count DESC, event_type ASC
        """)).fetchall()
    return [{"slug": row[0], "label": row[0].replace("-", " ").title(), "count": row[1]} for row in rows]


@app.get("/api/stats", tags=["Stats"])
def get_stats():
    ensure_schema()
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM events")).scalar() or 0
        upcoming = conn.execute(text("""
            SELECT COUNT(*) FROM events
            WHERE start_date IS NULL OR start_date >= NOW()
        """)).scalar() or 0
        with_email = conn.execute(text("""
            SELECT COUNT(*) FROM events WHERE contact_email IS NOT NULL
        """)).scalar() or 0
        with_phone = conn.execute(text("""
            SELECT COUNT(*) FROM events WHERE contact_phone IS NOT NULL
        """)).scalar() or 0
        by_type = conn.execute(text("""
            SELECT COALESCE(event_type, 'sans-type'), COUNT(*)
            FROM events
            GROUP BY 1
            ORDER BY 2 DESC
        """)).fetchall()
        by_region = conn.execute(text("""
            SELECT COALESCE(region, 'sans-region'), COUNT(*)
            FROM events
            GROUP BY 1
            ORDER BY 2 DESC
        """)).fetchall()

    return {
        "total_events": total,
        "upcoming_events": upcoming,
        "with_email": with_email,
        "with_phone": with_phone,
        "by_type": [{"label": row[0], "count": row[1]} for row in by_type],
        "by_region": [{"label": row[0], "count": row[1]} for row in by_region],
    }


@app.post("/api/scrape", response_model=ScrapeResult, tags=["Scraping"])
def trigger_scrape(req: ScrapeRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        run_scraper,
        regions=req.regions,
        max_per_region=req.max_per_region,
        fetch_details=req.fetch_details,
    )
    return ScrapeResult(
        status="started",
        message="Scraping Bizouk lance en arriere-plan. Consultez /api/stats pour suivre les donnees.",
    )
