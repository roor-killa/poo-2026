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

# -------------------------------------------------------------------
# Tests de fetch_page
# -------------------------------------------------------------------

class TestFetchPage:

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_success(self, mock_get):
        """fetch_page doit retourner un BeautifulSoup si la requête réussit."""
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
        import requests
        mock_get.side_effect = requests.exceptions.Timeout

        scraper = ConcreteScraper("https://example.com")
        result = scraper.fetch_page("https://example.com/page")

        assert result is None

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_http_error(self, mock_get):
        """fetch_page doit retourner None sur une erreur HTTP (404, etc.)."""
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Error")
        mock_get.return_value = mock_response

        scraper = ConcreteScraper("https://example.com")
        result = scraper.fetch_page("https://example.com/page")

        assert result is None

    @patch('src.base_scraper.requests.get')
    def test_fetch_page_connection_error(self, mock_get):
        """fetch_page doit retourner None si la connexion échoue."""
        import requests

        mock_get.side_effect = requests.ConnectionError("Connection failed")

        scraper = ConcreteScraper("https://example.com")
        result = scraper.fetch_page("https://example.com/page")

        assert result is None


# -------------------------------------------------------------------
# Tests de save_to_json / save_to_csv
# -------------------------------------------------------------------

class TestSave:
    def test_save_to_json(self, tmp_path, monkeypatch):
        """save_to_json doit créer un fichier JSON valide."""
        import json
        from pathlib import Path

        scraper = ConcreteScraper("https://example.com")
        scraper.data = [
            {"name": "Produit A", "price": 10},
            {"name": "Produit B", "price": 20}
        ]

        # Rediriger data/raw vers tmp_path
        monkeypatch.setattr("src.base_scraper.Path", lambda x="": tmp_path)

        filename = "test.json"
        scraper.save_to_json(filename)

        file_path = tmp_path / filename
        assert file_path.exists()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data == scraper.data

    def test_save_to_csv(self, tmp_path, monkeypatch):
        """save_to_csv doit créer un fichier CSV valide."""
        import pandas as pd
        from pathlib import Path

        scraper = ConcreteScraper("https://example.com")
        scraper.data = [
            {"name": "Produit A", "price": 10},
            {"name": "Produit B", "price": 20}
        ]

        monkeypatch.setattr("src.base_scraper.Path", lambda x="": tmp_path)

        filename = "test.csv"
        scraper.save_to_csv(filename)

        file_path = tmp_path / filename
        assert file_path.exists()

        df = pd.read_csv(file_path)
        assert len(df) == 2
        assert "name" in df.columns

    def test_save_to_csv_empty_data(self):
        """save_to_csv ne doit pas lever d'erreur si self.data est vide."""
        scraper = ConcreteScraper("https://example.com")
        # Ne doit pas lever d'exception
        scraper.save_to_csv("test.csv")
