from typing import Dict, List

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class NewScraper(BaseScraper):
    """Scraper generique conserve pour recuperer des blocs d'actualites ou d'agenda."""

    def __init__(self, category: str = "actualites"):
        """Stocke la categorie cible et initialise la session HTTP."""
        self.category = category
        super().__init__(base_url="https://www.bizouk.com", delay=2)

    def parse_article(self, article_soup: BeautifulSoup) -> Dict:
        """Extrait un titre, une date, un contenu court et une URL depuis un bloc HTML."""
        title_tag = article_soup.find(["h1", "h2", "h3"])
        title = title_tag.get_text(strip=True) if title_tag else None

        link_tag = article_soup.find("a", href=True)
        url = None
        if link_tag:
            href = link_tag["href"].strip()

            if href.startswith("/"):
                url = f"{self.base_url}{href}"
            elif href.startswith("http"):
                url = href
            else:
                url = f"{self.base_url}/{href}"

        date_tag = article_soup.find(["time", "small", "span"])
        date = date_tag.get_text(strip=True) if date_tag else None

        content_tag = article_soup.find("p")
        content = content_tag.get_text(" ", strip=True) if content_tag else ""

        return {
            "title": title,
            "date": date,
            "content": content,
            "url": url,
        }

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Analyse une page et retourne les blocs qui ressemblent a des articles."""
        results = []
        articles = soup.find_all("article")

        if not articles:
            articles = soup.find_all("div", class_=True)

        for article in articles:
            data = self.parse_article(article)

            if data["title"] or data["url"]:
                results.append(data)

        return results

    def scrape(self, max_pages: int = 2) -> List[Dict]:
        """Parcourt plusieurs pages de la categorie configuree."""
        results = []

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/{self.category}?page={page}"
            soup = self.fetch_page(url)

            if not soup:
                break

            page_results = self.parse(soup)
            results.extend(page_results)

            if not page_results:
                break

        return results
