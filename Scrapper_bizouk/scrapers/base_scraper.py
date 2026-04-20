from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import json
import os
import time

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """
    Classe de base abstraite pour tous les scrapers.
    """

    def __init__(self, base_url: str, delay: float = 1.0, timeout: float = 20.0):
        self.base_url = base_url
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 Educational Purpose Universite des Antilles",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            }
        )
        self.last_request_time: Optional[float] = None

    def _respect_delay(self):
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            self._respect_delay()
            response = self.session.get(url, timeout=self.timeout)
            self.last_request_time = time.time()
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"[ERREUR] impossible de recuperer {url} : {e}")
            return None

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        pass

    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass

    def save_to_json(self, data: List[Dict], filename: str):
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"[OK] donnees sauvegardees dans {filename}")

    def close(self):
        self.session.close()
