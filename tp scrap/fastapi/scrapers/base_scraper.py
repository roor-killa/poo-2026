# scrapers/base_scraper.py

from abc import ABC, abstractmethod
import json
import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """
    Base class for scrapers.
    Handles the HTTP session, request delay, page fetching, and JSON export.
    """

    def __init__(self, base_url: str, delay: float = 1.0, timeout: int = 30, retries: int = 2):
        self.base_url = base_url
        self.delay = delay
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/147.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        })

        self.last_request_time = None

    def _respect_delay(self):
        if self.last_request_time is not None:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < self.delay:
                time.sleep(self.delay - elapsed_time)
        self.last_request_time = time.time()

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        last_error = None

        for attempt in range(1, self.retries + 1):
            try:
                self._respect_delay()
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return BeautifulSoup(response.text, "lxml")

            except requests.exceptions.RequestException as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(2)

        print(f"[ERREUR] Impossible de recuperer {url}")
        print(f"Detail : {last_error}")
        return None

    def save_to_json(self, data: List[Dict], filename: str):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"[OK] {len(data)} entrees sauvegardees dans {filename}")
        except Exception as exc:
            print(f"[ERREUR] Sauvegarde impossible : {exc}")

    def close(self):
        self.session.close()

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        pass

    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass
