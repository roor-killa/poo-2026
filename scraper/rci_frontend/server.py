"""Lightweight Flask server bridging the RCI frontend to the scraper."""

import logging
import sys
import threading
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

# Add the project root to sys.path so `src` can be imported reliably
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

from src.observers import ScraperObserver  # noqa: E402
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

    # Clamp values to safe ranges
    max_depth = max(0, min(max_depth, 3))
    max_pages = max(1, min(max_pages, 100))
    delay = max(0.5, min(delay, 10.0))

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

            logger.info(
                "Scraping lancé — max_depth=%d, max_pages=%d, delay=%.1fs",
                max_depth, max_pages, delay,
            )
            scraper.scrape(max_pages=max_pages)

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

    return jsonify({"status": "started", "max_depth": max_depth, "max_pages": max_pages, "delay": delay})


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
    """Serve the raw scraped JSON data from scraper/data/raw/rci_raw.json"""
    import json
    raw_data_path = _PROJECT_ROOT / "data" / "raw" / "rci_raw.json"
    try:
        with open(raw_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Fichier rci_raw.json non trouvé"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Fichier JSON invalide"}), 400


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("RCI Frontend → http://localhost:5000")
    app.run(debug=True, port=5000)
