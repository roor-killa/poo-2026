# scrapers/base_scraper.py

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
from datetime import datetime
import json


class BaseScraper(ABC):
    """
    Classe abstraite de base pour tous les scrapers.
    Contient les méthodes communes :
    - gestion de session
    - gestion du délai entre requêtes
    - récupération de page
    - sauvegarde JSON
    """

    def __init__(self, base_url: str, delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()

        # Identification claire du bot (important éthiquement)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational Purpose) Université des Antilles'
        })

        self.last_request_time = None

    def _respect_delay(self):
        """
        Attend si nécessaire pour respecter le délai minimum entre requêtes.
        """
        if self.last_request_time is not None:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < self.delay:
                time.sleep(self.delay - elapsed_time)
        self.last_request_time = time.time()

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Télécharge une page et retourne un objet BeautifulSoup.
        """
        try:
            self._respect_delay()
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            return soup

        except requests.exceptions.RequestException as e:
            print(f"[ERREUR] Impossible de récupérer {url}")
            print(f"Détail : {e}")
            return None

    def save_to_json(self, data: List[Dict], filename: str):
        """
        Sauvegarde les données dans un fichier JSON.
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[OK] {len(data)} entrées sauvegardées dans {filename}")
        except Exception as e:
            print(f"[ERREUR] Sauvegarde impossible : {e}")

    def close(self):
        """Ferme la session HTTP"""
        self.session.close()

    # ------------------------------------------------------------------ #
    # Méthodes abstraites — à implémenter dans chaque scraper enfant      #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse une page HTML et retourne une liste de dictionnaires."""
        pass

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Méthode principale de scraping."""
        pass
