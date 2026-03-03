

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


    @abstractmethod
    def to_document(self, item: dict[str, any]) -> dict[str, any]:
        """Normalise une entrée brute vers le schéma commun `documents`.

        Chaque scraper DOIT implémenter cette méthode pour que ses données
        puissent être intégrées dans la base RAG de Fèfèn.

        Args:
            item: Un élément de self.data (tel que retourné par parse()).

        Returns:
            Dictionnaire conforme au schéma de la table `documents` :

            Obligatoires :
                source   (str) : identifiant du scraper — ex: 'bizouk'
                doc_type (str) : type de document   — ex: 'annonce'
                title    (str) : titre principal
                content  (str) : texte principal utilisé pour la recherche RAG

            Optionnels :
                url          (str | None) : URL source (permet la déduplication)
                published_at (str | None) : date ISO-8601 — ex: '2026-01-15'
                metadata     (dict | None): champs spécifiques au scraper
                                            ex: {'prix': '120€', 'localisation': 'Fort-de-France'}
        """

    def save_to_db(self, conn: any) -> int:
        """Sauvegarde self.data dans la table `documents` via DocumentLoader.

        Appelle to_document() sur chaque élément de self.data puis effectue
        un UPSERT groupé (idempotent : relancer ne crée pas de doublons).

        Args:
            conn: Connexion psycopg2 active.

        Returns:
            Nombre de documents insérés ou mis à jour.

        Example:
            from src.db_loader import get_connection
            conn = get_connection()
            scraper.scrape(max_pages=3)
            n = scraper.save_to_db(conn)
            conn.close()
        """
        # from src.db_loader import DocumentLoader  # import local évite la dépendance circulaire

        # loader = DocumentLoader(conn)
        # return loader.upsert_many(self.data, self.to_document)