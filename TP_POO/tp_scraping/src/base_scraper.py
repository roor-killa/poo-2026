

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time

class BaseScraper(ABC):
    """Classe abstraite pour tous les scrapers."""
    
    def __init__(self, base_url: str, delay: float = 1.5):
        self.base_url = base_url
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Educational; UA)',
            'From': 'randi.toma@univ-antilles.fr'
        }
        self.data: List[Dict] = []
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Récupère et parse une page HTML."""
        try:
            time.sleep(self.delay)  # Rate limiting
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Erreur lors du fetch: {e}")
            return None
    
    @abstractmethod
    def scrape(self, max_pages: int = 1) -> List[Dict]:
        """Méthode principale de scraping."""
        pass
    
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse le contenu HTML."""
        pass