"""
Exemples d'utilisation du RciScraper
"""

from src.scrapers.rci_scraper import RciScraper, url_rci



if __name__ == "__main__":
    
    scraper = RciScraper(url_rci)
    scraper.delay = 120  # 2 minutes entre chaque requête
    
    # Étape 1: Scraper 2 articles (mode test)
    print("Scraping de 2 articles")
    scraper.scrape(max_articles=2)
    
    # Étape 2: Parser les articles scrapés
    print("\nParsing des articles scrapés")
    scraper.parse()