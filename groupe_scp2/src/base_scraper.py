"""
BaseScraper — Classe abstraite commune à tous les scrapers.

MEMBRE 1 : Ce fichier est entièrement sous ta responsabilité.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
import time
import json
import csv
import logging
from pathlib import Path
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """
    Classe abstraite définissant le contrat de base pour tous les scrapers.

    Attributes:
        base_url (str): URL de base du site à scraper.
        delay (float): Délai (en secondes) entre chaque requête (rate limiting).
        headers (dict): En-têtes HTTP envoyés avec chaque requête.
        data (List[Dict]): Données collectées lors du scraping.
        logger (Logger): Logger propre à chaque sous-classe.
    """

    def __init__(self, base_url: str, delay: float = 1.5) -> None:
        """
        Initialise le scraper avec l'URL de base et les paramètres communs.

        Args:
            base_url: URL racine du site cible.
            delay: Temps d'attente entre les requêtes (en secondes).
        """
        self.base_url = base_url
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'From': 'groupe2@univ-antilles.fr'
        }
        self.data: List[Dict] = []
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure et retourne un logger nommé d'après la sous-classe."""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère une page web et retourne un objet BeautifulSoup.

        Gère les erreurs réseau suivantes :
        - Timeout (délai dépassé)
        - Erreur HTTP (404, 503, etc.)
        - Erreur de connexion

        Args:
            url: URL complète de la page à récupérer.

        Returns:
            Objet BeautifulSoup si succès, None sinon.
        """
        time.sleep(self.delay)  # Rate limiting — respecter le serveur
        try:
            self.logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Erreur HTTP {e.response.status_code}: {url}")
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout pour: {url}")
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connexion impossible: {url}")
        return None

    def save_to_json(self, filename: str) -> None:
        """
        Sauvegarde self.data en JSON dans data/raw/.

        Args:
            filename: Nom du fichier (ex: 'kiprix_gp.json').
        """
        path = Path("data/raw") / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        self.logger.info(f"Sauvegardé: {path} ({len(self.data)} entrées)")

    def save_to_csv(self, filename: str) -> None:
        """
        Sauvegarde self.data en CSV dans data/raw/.

        Args:
            filename: Nom du fichier (ex: 'kiprix_gp.csv').
        """
        if not self.data:
            self.logger.warning("Aucune donnée à sauvegarder.")
            return
        path = Path("data/raw") / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        self.logger.info(f"Sauvegardé: {path}")

    @abstractmethod
    def scrape(self, max_pages: int = 1) -> List[Dict]:
        """
        Méthode principale de scraping — à implémenter dans chaque sous-classe.

        Args:
            max_pages: Nombre maximum de pages à scraper.

        Returns:
            Liste de dictionnaires contenant les données extraites.
        """
        pass

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extrait les données structurées depuis le HTML d'une page.

        Args:
            soup: Objet BeautifulSoup de la page à parser.

        Returns:
            Liste de dictionnaires avec les données de la page.
        """
        pass
