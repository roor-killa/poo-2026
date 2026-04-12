"""Lightweight Flask server bridging the RCI frontend to the scraper."""

import logging
import os
import sys
import threading
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import psycopg2

# Add the project root to sys.path so `src` can be imported reliably
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))
load_dotenv(_PROJECT_ROOT / ".env")

from src.observers import ScraperObserver  # noqa: E402
from src.db_loader import get_connection  # noqa: E402
from src.scrapers.rci_scraper import RCIScraper  # noqa: E402

# ------------------------------------------------------------------
# Logging — show scraper activity in the console
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("rci_server")

app = Flask(__name__, static_folder=".", static_url_path="")

# In-memory state for the running scrape job
_lock = threading.Lock()
_job: dict[str, Any] = {
    "running": False,
    "data": [],
    "error": None,
    "pages_visited": 0,
    "articles_count": 0,
}


def _open_db_connection():
    """Ouvre une connexion DB avec fallback vers les valeurs docker-compose."""
    try:
        return get_connection()
    except Exception as primary_exc:
        logger.warning("Connexion DB primaire impossible: %s", primary_exc)
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5433")),
            dbname=os.getenv("POSTGRES_DB", "poo_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        )


def _load_known_rci_urls(conn) -> set[str]:
    """Charge les URLs deja presentes dans documents pour la source RCI."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT url
            FROM documents
            WHERE source = 'rci' AND doc_type = 'actualite' AND url IS NOT NULL
            """
        )
        return {row[0] for row in cur.fetchall() if row and row[0]}


# ------------------------------------------------------------------
# Observer that feeds live progress into _job
# ------------------------------------------------------------------
class LiveProgressObserver(ScraperObserver):
    """Pushes every scraper event into the shared _job dict so the
    /api/status endpoint can report real-time progress."""

    def __init__(self, scraper: RCIScraper) -> None:
        self._scraper = scraper

    def update(self, event: str, payload: dict[str, Any]) -> None:
        with _lock:
            _job["pages_visited"] = len(self._scraper.visited)
            _job["data"] = list(self._scraper.data)
            _job["articles_count"] = len(self._scraper.data)

        match event:
            case "fetch":
                logger.info("FETCH  %s → %s", payload.get("url"), payload.get("status"))
            case "parse":
                logger.info(
                    "PARSE  %d article(s) — total : %d articles, %d pages",
                    payload.get("count", 0),
                    len(self._scraper.data),
                    len(self._scraper.visited),
                )
            case "error":
                logger.warning("ERROR  %s : %s", payload.get("url"), payload.get("error"))
            case "done":
                logger.info(
                    "DONE   %d articles, %d pages en %.1fs",
                    payload.get("total", 0),
                    len(self._scraper.visited),
                    payload.get("duration", 0.0),
                )


# ------------------------------------------------------------------
# Static files
# ------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ------------------------------------------------------------------
# API — launch scraper
# ------------------------------------------------------------------
@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    """Run the RCIScraper with user-supplied arguments and return JSON."""
    with _lock:
        if _job["running"]:
            return jsonify({"error": "Un scraping est déjà en cours."}), 409

    body = request.get_json(silent=True) or {}

    max_depth = int(body.get("max_depth", 1))
    max_pages = int(body.get("max_pages", 10))
    delay = float(body.get("delay", 1.5))
    chunk_size = int(body.get("chunk_size", 200))

    # Clamp values to safe ranges
    max_depth = max(0, min(max_depth, 3))
    max_pages = max(1, min(max_pages, 100))
    delay = max(0.5, min(delay, 10.0))
    chunk_size = max(1, min(chunk_size, 1000))

    def run():
        try:
            with _lock:
                _job["running"] = True
                _job["error"] = None
                _job["data"] = []
                _job["pages_visited"] = 0
                _job["articles_count"] = 0

            scraper = RCIScraper(max_depth=max_depth, delay=delay)
            scraper.attach(LiveProgressObserver(scraper))

            # Eviter de re-scraper des articles deja stockes.
            preload_conn = _open_db_connection()
            try:
                known_urls = _load_known_rci_urls(preload_conn)
            finally:
                preload_conn.close()
            scraper.set_known_urls(known_urls)

            logger.info(
                "Scraping lancé — max_depth=%d, max_pages=%d, delay=%.1fs, chunk_size=%d, deja_connus=%d",
                max_depth, max_pages, delay, chunk_size, len(known_urls),
            )
            scraper.scrape(max_pages=max_pages)

            # Persistance systématique en base PostgreSQL après chaque scrape
            conn = _open_db_connection()
            try:
                inserted = scraper.save_to_db(conn, chunk_size=chunk_size)
            finally:
                conn.close()
            logger.info("DB sync terminé — %d document(s) RCI upserté(s)", inserted)

            # Final snapshot
            with _lock:
                _job["data"] = list(scraper.data)
                _job["pages_visited"] = len(scraper.visited)
                _job["articles_count"] = len(scraper.data)
            logger.info("Scraping terminé — %d articles récupérés.", len(scraper.data))
        except Exception as exc:
            logger.error("Erreur pendant le scraping : %s", exc)
            with _lock:
                _job["error"] = str(exc)
        finally:
            with _lock:
                _job["running"] = False

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    return jsonify(
        {
            "status": "started",
            "max_depth": max_depth,
            "max_pages": max_pages,
            "delay": delay,
            "chunk_size": chunk_size,
        }
    )


# ------------------------------------------------------------------
# API — poll status / results
# ------------------------------------------------------------------
@app.route("/api/status")
def api_status():
    with _lock:
        return jsonify({
            "running": _job["running"],
            "articles": _job["articles_count"],
            "pages_visited": _job["pages_visited"],
            "error": _job["error"],
        })


@app.route("/api/results")
def api_results():
    with _lock:
        if _job["running"]:
            return jsonify({"error": "Scraping en cours…"}), 202
        return jsonify({"articles": _job["data"], "error": _job["error"]})


@app.route("/api/raw-data")
def api_raw_data():
    """Retourne les articles RCI depuis PostgreSQL pour l'onglet Donnees."""
    limit = request.args.get("limit", default=300, type=int)
    limit = max(1, min(limit, 2000))

    conn = None
    try:
        conn = _open_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    title,
                    content,
                    url,
                    metadata,
                    published_at,
                    scraped_at,
                    updated_at
                FROM documents
                WHERE source = 'rci' AND doc_type = 'actualite'
                ORDER BY COALESCE(updated_at, scraped_at) DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()

        data: list[dict[str, Any]] = []
        for title, content, url, metadata, published_at, scraped_at, updated_at in rows:
            meta = metadata if isinstance(metadata, dict) else {}
            data.append(
                {
                    "title": title or "",
                    "author": meta.get("author", ""),
                    "photo": meta.get("photo", ""),
                    "infos": meta.get("infos", ""),
                    "body": content or "",
                    "url": url or "",
                    "depth": meta.get("depth", 0),
                    "date_publication": published_at.isoformat() if published_at else "",
                    "date_extraction": scraped_at.isoformat() if scraped_at else "",
                    "date_updated": updated_at.isoformat() if updated_at else "",
                }
            )

        return jsonify(data)
    except Exception as exc:
        logger.error("Erreur lecture DB /api/raw-data : %s", exc)
        return jsonify({"error": f"Impossible de lire la base: {exc}"}), 500
    finally:
        if conn is not None:
            conn.close()


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("RCI Frontend → http://localhost:5000")
    app.run(debug=True, port=5000)
