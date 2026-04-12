"""Tests cibles pour RCIScraper.

Objectifs:
- Verifier que scrape() lance bien le crawl et retourne les donnees.
- Verifier le fetch/crawl/parse HTML sur un mini-site simule (sans reseau).
- Ajouter un test d'integration optionnel qui scrape vraiment rci.fm.

Le test reseau reel est desactive par defaut.
Pour l'activer:
    RUN_RCI_LIVE=1 python -m pytest tests/test_rci_scraper.py -v -m integration
"""

from __future__ import annotations

import os

import pytest
from bs4 import BeautifulSoup

from src.scrapers.rci_scraper import RCIScraper


@pytest.fixture()
def fake_site_pages() -> dict[str, str]:
    """Petit graphe HTML simulant un listing + une page article."""
    return {
        "https://rci.fm/start": """
            <html><body>
                <a href="/martinique/infos/faits-divers/article-1">Article 1</a>
                <a href="/martinique/infos/categorie">Categorie</a>
                <a href="https://example.com/outside">Externe</a>
            </body></html>
        """,
        "https://rci.fm/martinique/infos/faits-divers/article-1": """
            <html><body>
                <h1 itemprop="name">Titre article RCI</h1>
                <span itemprop="author">Redaction RCI</span>
                <img itemprop="image" src="https://rci.fm/img/article.jpg" />
                <div class="info">x</div>
                <div class="info">y</div>
                <div class="info">Societe | 2026-04-12</div>
                <p property="schema:text">Premier paragraphe.</p>
                <p property="schema:text">Deuxieme paragraphe.</p>
            </body></html>
        """,
        "https://rci.fm/martinique/infos/categorie": """
            <html><body>
                <h2>Page categorie</h2>
                <a href="/martinique/infos/faits-divers/article-2">Article 2</a>
            </body></html>
        """,
        "https://rci.fm/martinique/infos/faits-divers/article-2": """
            <html><body>
                <h1 itemprop="name">Deuxieme article</h1>
                <p property="schema:text">Contenu article 2.</p>
            </body></html>
        """,
    }


def test_parse_extrait_un_article() -> None:
    scraper = RCIScraper(delay=0)
    html = """
        <html><body>
            <h1 itemprop="name">Titre test</h1>
            <span itemprop="author">Auteur test</span>
            <img itemprop="image" src="https://rci.fm/image.jpg" />
            <div class="info">i1</div>
            <div class="info">i2</div>
            <div class="info">Culture | 2026-01-01</div>
            <p property="schema:text">Contenu A</p>
            <p property="schema:text">Contenu B</p>
        </body></html>
    """
    soup = BeautifulSoup(html, "lxml")

    parsed = scraper.parse(soup)

    assert len(parsed) == 1
    item = parsed[0]
    assert item["title"] == "Titre test"
    assert item["author"] == "Auteur test"
    assert item["infos"] == "Culture | 2026-01-01"
    assert "Contenu A" in item["body"]
    assert "Contenu B" in item["body"]


def test_parse_ignore_les_pages_non_article() -> None:
    scraper = RCIScraper(delay=0)
    soup = BeautifulSoup("<html><body><h2>Listing</h2></body></html>", "lxml")

    parsed = scraper.parse(soup)

    assert parsed == []


def test_scrape_lance_le_crawl(monkeypatch: pytest.MonkeyPatch) -> None:
    scraper = RCIScraper(delay=0, start_url="https://rci.fm/start")

    called: dict[str, object] = {}

    def fake_crawl(url: str, depth: int, max_pages: int) -> None:
        called["args"] = (url, depth, max_pages)
        scraper.data.append({"title": "ok", "body": "ok"})

    monkeypatch.setattr(scraper, "_crawl", fake_crawl)

    out = scraper.scrape(max_pages=5)

    assert called["args"] == ("https://rci.fm/start", 0, 5)
    assert len(out) == 1
    assert out[0]["title"] == "ok"


def test_crawl_fetch_parse_sans_reseau(
    monkeypatch: pytest.MonkeyPatch,
    fake_site_pages: dict[str, str],
) -> None:
    scraper = RCIScraper(max_depth=1, delay=0, start_url="https://rci.fm/start")

    def fake_fetch_page(url: str):
        html = fake_site_pages.get(url)
        if html is None:
            return None
        return BeautifulSoup(html, "lxml")

    monkeypatch.setattr(scraper, "fetch_page", fake_fetch_page)

    results = scraper.scrape(max_pages=10)

    assert len(scraper.visited) >= 2
    assert len(results) >= 1

    first = results[0]
    assert first["url"].startswith("https://rci.fm/")
    assert first["depth"] in (0, 1)
    assert first["title"]
    assert len(first["body"]) >= 10


@pytest.mark.integration
def test_rci_live_scrape_reel_minimal() -> None:
    """Test reel sur rci.fm, volontairement limite et opt-in."""
    if os.getenv("RUN_RCI_LIVE") != "1":
        pytest.skip("Definir RUN_RCI_LIVE=1 pour activer ce test reseau reel")

    scraper = RCIScraper(max_depth=1, delay=0.5)
    results = scraper.scrape(max_pages=8)

    assert len(scraper.visited) >= 1
    assert len(results) >= 1

    sample = results[0]
    assert sample.get("title")
    assert len(sample.get("body", "")) >= 40
    assert str(sample.get("url", "")).startswith("https://rci.fm")
