from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

class NewsScraper(BaseScraper): # Scraper spécifique pour les articles de presse
    """
    Classe de base abstraite pour tous les scrapers.
    Implémente les fonctionnalités communes.
    """
    def __init__(self, category: str = "actualites"):
        """
        Args:
            category: Catégorie d'articles
        """
        super().__init__(base_url="https://www.bizouk.com/?region=martinique"+ category)
        self.category = category
        
    def parse_article(self, article_soup: BeautifulSoup) -> Dict: # Parse un article individuel
        """
        Parse un article individuel
        Returns:
        Dict avec titre, date, auteur, contenu, tags
        """
        titre_tag = article_soup.find("h1") or article_soup.find("h2")
        date_tag = article_soup.find(class_="date")
        auteur_tag = article_soup.find(class_="author")
        contenu_paragraphes = article_soup.find_all("p")
        tags_elements = article_soup.find_all(class_="tag")
        return {
            "titre": titre_tag.get_text(strip=True) if titre_tag else None,
            "date": date_tag.get_text(strip=True) if date_tag else None,
            "auteur": auteur_tag.get_text(strip=True) if auteur_tag else None,
            "contenu": "\n".join(p.get_text(strip=True) for p in contenu_paragraphes) if contenu_paragraphes else None,
            "tags": [tag.get_text(strip=True) for tag in tags_elements] if tags_elements else []
            }
    
    def parse(self, soup: BeautifulSoup) -> List[Dict]: # Parse la page de liste d'articles
        """
        Parse la page de liste d'articles
        """
        articles_data = []
        articles = soup.find_all("article")
        for article in articles:
            parsed_article = self.parse_article(article)
            articles_data.append(parsed_article)
        return articles_data
    
    def scrape(self, max_pages: int = 3) -> List[Dict]: # Scrape plusieurs pages d'articles
        """
        Scrape plusieurs pages d'articles
        
        Args:
            max_pages: Nombre maximum de pages à scraper
        """
        all_articles = []
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}&page={page}"
                html = self.fetch(url)
                soup = BeautifulSoup(html, "html.parser")
                articles = self.parse(soup)

                if not articles:
                    break 

                all_articles.extend(articles)

            except Exception as e:
                print(f"Erreur page {page}: {e}")
                continue

        return all_articles