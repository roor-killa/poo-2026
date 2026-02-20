"""
Tests pour BaseScraper.

MEMBRE 3 : Implémenter tous les cas marqués TODO.
Objectif : coverage > 70% → lancer avec `pytest --cov=src`
"""

import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from src.base_scraper import BaseScraper


# -------------------------------------------------------------------
# Sous-classe concrète pour pouvoir instancier BaseScraper dans les tests
# -------------------------------------------------------------------
class ConcreteScraper(BaseScraper):
    """Implémentation minimale de BaseScraper pour les tests."""

    def scrape(self, max_pages: int = 1):
        return []

    def parse(self, soup: BeautifulSoup):
        return []


# -------------------------------------------------------------------
# Tests d'initialisation
# -------------------------------------------------------------------

class TestInit:
    def test_base_url(self):
        """Vérifier que base_url est correctement assignée."""
        scraper = ConcreteScraper("https://example.com")
        assert scraper.base_url == "https://example.com"

    def test_default_delay(self):
        """Vérifier que le délai par défaut est 1.5s."""
        scraper = ConcreteScraper("https://example.com")
        assert scraper.delay == 1.5

    def test_custom_delay(self):
        """Vérifier qu'un délai personnalisé est pris en compte."""
        scraper = ConcreteScraper("https://example.com", delay=3.0)
        assert scraper.delay == 3.0

    def test_data_initially_empty(self):
        """Vérifier que self.data est une liste vide à l'initialisation."""
        scraper = ConcreteScraper("https://example.com")
        assert scraper.data == []

    def test_headers_contain_user_agent(self):
        """Vérifier que les headers contiennent un User-Agent."""
        scraper = ConcreteScraper("https://example.com")
        assert 'User-Agent' in scraper.headers


# -------------------------------------------------------------------
# Tests de fetch_page
# -------------------------------------------------------------------

class TestFetchPage:
    @patch('src.base_scraper.requests.get')
    def test_fetch_page_success(self, mock_get):
        """fetch_page doit retourner un BeautifulSoup si la requête réussit."""
        # TODO MEMBRE 3 : compléter ce mock
        mock_response = MagicMock()
        mock_response.content = b"<html><body><h1>Test</h1></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        scraper = ConcreteScraper("https://example.com")
        result = scraper.fetch_page("https://example.com/page")

        assert result is not None
        assert result.find('h1').text == "Test"

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_timeout(self, mock_get):
        """fetch_page doit retourner None en cas de Timeout."""
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout

        scraper = ConcreteScraper("https://example.com")
        result = scraper.fetch_page("https://example.com/page")

        assert result is None

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_http_error(self, mock_get):
        """fetch_page doit retourner None sur une erreur HTTP (404, etc.)."""
        # TODO MEMBRE 3 : simuler une HTTPError (status_code=404)
        raise NotImplementedError("MEMBRE 3 : à implémenter")

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_connection_error(self, mock_get):
        """fetch_page doit retourner None si la connexion échoue."""
        # TODO MEMBRE 3 : simuler une ConnectionError
        raise NotImplementedError("MEMBRE 3 : à implémenter")


# -------------------------------------------------------------------
# Tests de save_to_json / save_to_csv
# -------------------------------------------------------------------

class TestSave:
    def test_save_to_json(self, tmp_path, monkeypatch):
        """save_to_json doit créer un fichier JSON valide."""
        # TODO MEMBRE 3 :
        # 1. Monkeypatche Path("data/raw") vers tmp_path
        # 2. Injecte des données dans scraper.data
        # 3. Appelle save_to_json("test.json")
        # 4. Vérifie que le fichier existe et contient les bonnes données
        raise NotImplementedError("MEMBRE 3 : à implémenter")

    def test_save_to_csv(self, tmp_path, monkeypatch):
        """save_to_csv doit créer un fichier CSV valide."""
        # TODO MEMBRE 3 : similaire à test_save_to_json
        raise NotImplementedError("MEMBRE 3 : à implémenter")

    def test_save_to_csv_empty_data(self):
        """save_to_csv ne doit pas lever d'erreur si self.data est vide."""
        scraper = ConcreteScraper("https://example.com")
        # Ne doit pas lever d'exception
        scraper.save_to_csv("test.csv")
