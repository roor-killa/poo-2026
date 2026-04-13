import time
import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    """
    Classe abstraite définissant la structure obligatoire d'un scraper.
    Utilise le pattern Template Method.
    """

    def __init__(self, base_url: str, delay: float = 1.5):
        self.base_url = base_url
        self.delay = delay
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Project; L2 Info UA)',
            'Accept-Language': 'fr-FR,fr;q=0.9'
        }
        self.data: List[Dict] = []

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Méthode concrète : Récupère le HTML d'une page."""
        try:
            print(f"🌍 Connexion à : {url}")
            time.sleep(self.delay)  # Pause pour ne pas surcharger le site
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Lève une erreur si 404 ou 500
            
            # Retourne l'objet BeautifulSoup prêt à être analysé
            return BeautifulSoup(response.content, 'lxml')
            
        except requests.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            return None

    def save_to_json(self, filename: str):
        """Méthode concrète : Sauvegarde les données dans data/raw."""
        # On s'assure que le dossier existe
        output_dir = os.path.join("data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f"{filename}.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"💾 Données sauvegardées dans {filepath}")

    @abstractmethod
    def scrape(self):
        """Méthode abstraite : Chaque enfant DEVRA définir comment il navigue."""
        pass

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Méthode abstraite : Chaque enfant DEVRA définir comment il extrait les infos."""
        pass