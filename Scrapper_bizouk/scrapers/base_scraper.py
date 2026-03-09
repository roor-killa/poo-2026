from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
import json
import os


class BaseScraper(ABC):
    """
    classe de base abstraite pour tous les scrapers
    """

    def __init__(self, base_url: str, delay: float = 1.0):
        # stocke lurl de base du site
        self.base_url = base_url

        # stocke le délai entre deux requêtes
        self.delay = delay

        # crée une session réutilisable pour les requêtes http
        self.session = requests.Session()

        # ajoute un user agent pour identifier le scraper
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 Educational Purpose Université des Antilles"
        })

        # garde la trace du moment de la dernière requête
        self.last_request_time: Optional[float] = None

    def _respect_delay(self):
        # attend si la dernière requête est trop récente
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        # récupère une page puis la transforme en objet beautifulsoup
        try:
            # respecte le délai avant la requête
            self._respect_delay()

            # envoie la requête au site
            response = self.session.get(url, timeout=10)

            # met à jour le moment de la dernière requête
            self.last_request_time = time.time()

            # vérifie que la réponse est valide
            response.raise_for_status()

            # retourne le html parsé
            return BeautifulSoup(response.text, "html.parser")

        except requests.RequestException as e:
            print(f"[ERREUR] impossible de récupérer {url} : {e}")
            return None

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        # devra être définie dans la classe enfant
        pass

    @abstractmethod
    def scrape(self) -> List[Dict]:
        # devra être définie dans la classe enfant
        pass

    def save_to_json(self, data: List[Dict], filename: str):
        # récupère le dossier du fichier si il existe
        folder = os.path.dirname(filename)

        # crée le dossier seulement si nécessaire
        if folder:
            os.makedirs(folder, exist_ok=True)

        # sauvegarde les données dans un fichier json
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"[OK] données sauvegardées dans {filename}")

    def close(self):
        # ferme la session http
        self.session.close()