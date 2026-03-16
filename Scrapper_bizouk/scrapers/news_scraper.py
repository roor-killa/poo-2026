from .base_scraper import BaseScraper
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class NewScraper(BaseScraper):

    def __init__(self, category: str = "actualites"):
        # stocke la catégorie à scraper
        self.category = category

        # initialise lurl de base du site
        super().__init__(base_url="https://www.bizouk.com", delay=2)

    def parse_article(self, article_soup: BeautifulSoup) -> Dict:
        # récupère le titre
        title_tag = article_soup.find(["h1", "h2", "h3"])
        title = title_tag.get_text(strip=True) if title_tag else None

        # récupère le lien
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

        # récupère la date si elle existe
        date_tag = article_soup.find(["time", "small", "span"])
        date = date_tag.get_text(strip=True) if date_tag else None

        # récupère le texte principal
        content_tag = article_soup.find("p")
        content = content_tag.get_text(" ", strip=True) if content_tag else ""

        return {
            "title": title,
            "date": date,
            "content": content,
            "url": url
        }

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        # liste finale des articles
        results = []

        # cherche les blocs article
        articles = soup.find_all("article")

        # si aucun article nest trouvé
        # essaie avec des blocs div plus génériques
        if not articles:
            articles = soup.find_all("div", class_=True)

        # parcourt les blocs trouvés
        for article in articles:
            data = self.parse_article(article)

            # garde seulement les blocs qui ont au moins un titre ou un lien
            if data["title"] or data["url"]:
                results.append(data)

        return results

    def scrape(self, max_pages: int = 2) -> List[Dict]:
        # liste finale des résultats
        results = []

        # parcourt plusieurs pages
        for page in range(1, max_pages + 1):
            # construit lurl avec pagination
            url = f"{self.base_url}/{self.category}?page={page}"

            # récupère la page
            soup = self.fetch_page(url)

            # arrête si la page nest pas récupérée
            if not soup:
                break

            # parse la page et ajoute les résultats
            page_results = self.parse(soup)
            results.extend(page_results)

            # arrête si aucune donnée nest trouvée
            if not page_results:
                break

        return results