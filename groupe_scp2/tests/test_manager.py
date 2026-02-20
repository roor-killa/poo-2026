"""
Tests pour ScraperManager.

MEMBRE 3 : Implémenter tous les cas marqués TODO.
"""

import pytest
from unittest.mock import patch, MagicMock

from src.manager import ScraperManager
from src.scrapers.kiprix_scraper import KiprixScraper


class TestCreateScraper:
    def test_create_kiprix_returns_correct_type(self):
        """create_scraper('kiprix') doit retourner une instance de KiprixScraper."""
        manager = ScraperManager()
        scraper = manager.create_scraper('kiprix')
        assert isinstance(scraper, KiprixScraper)

    def test_create_kiprix_with_territory(self):
        """create_scraper doit transmettre les kwargs au constructeur."""
        manager = ScraperManager()
        scraper = manager.create_scraper('kiprix', territory='mq')
        assert scraper.territory == 'mq'

    def test_create_unknown_scraper_raises(self):
        """create_scraper doit lever ValueError pour un nom inconnu."""
        manager = ScraperManager()
        with pytest.raises(ValueError):
            manager.create_scraper('site_inconnu')


class TestScrapeAll:
    @patch.object(KiprixScraper, 'scrape')
    def test_scrape_all_sequential(self, mock_scrape):
        """scrape_all() doit retourner un dict avec les résultats de chaque scraper."""
        # TODO MEMBRE 3 :
        # - mock_scrape retourne une liste factice (ex: [{'name': 'Produit A'}])
        # - Vérifier que le résultat est un dict avec la clé 'kiprix'
        raise NotImplementedError("MEMBRE 3 : à implémenter")

    @patch.object(KiprixScraper, 'scrape')
    def test_scrape_all_parallel(self, mock_scrape):
        """scrape_all(parallel=True) doit produire le même résultat qu'en séquentiel."""
        # TODO MEMBRE 3 : similaire au test séquentiel mais avec parallel=True
        raise NotImplementedError("MEMBRE 3 : à implémenter")
