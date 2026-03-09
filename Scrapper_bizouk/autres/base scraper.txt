

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
import json
import os


class BaseScraper(ABC):
    """
    Classe de base abstraite pour tous les scrapers.
    Implémente les fonctionnalités communes.
    """

    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Args:
            base_url: URL de base du site à scraper
            delay: Délai entre les requêtes (en secondes)
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational Purpose) Université des Antilles'
        })
        self.last_request_time: Optional[float] = None

    def _respect_delay(self):
        """Respecte le délai entre les requêtes"""
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page web

        Returns:
            BeautifulSoup object ou None si erreur
        """
        try:
            self._respect_delay()

            response = self.session.get(url, timeout=10)
            self.last_request_time = time.time()

            response.raise_for_status()

            return BeautifulSoup(response.text, 'html.parser')

        except requests.RequestException as e:
            print(f"[ERREUR] Impossible de récupérer {url} : {e}")
            return None

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Méthode abstraite à implémenter dans les classes enfants.
        Parse le contenu HTML et extrait les données.
        """
        pass

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Méthode principale de scraping.
        À implémenter dans les classes enfants.
        """
        pass

    def save_to_json(self, data: List[Dict], filename: str):
        """Sauvegarde les données en JSON"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"[OK] Données sauvegardées dans {filename}")

    def close(self):
        """Ferme la session"""
        self.session.close()