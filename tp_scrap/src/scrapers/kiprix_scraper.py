from bs4 import BeautifulSoup
from typing import List, Dict
from src.base_scraper import BaseScraper

class KiprixScraper(BaseScraper):
    """Scraper pour Kiprix (Comparateur de prix)."""
    def __init__(self):
        super().__init__(base_url="https://kiprix.com/recherche?q=martinique", delay=2.0)
        # on déguise le robot en vrai Google Chrome pour passer le pare-feu
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
    def scrape(self, max_pages: int = 1) -> List[Dict]:
        print("🚀 Lancement du scraper Kiprix...")
        soup = self.fetch_page(self.base_url)
        if soup:
            self.data = self.parse(soup)
            self.save_to_json("kiprix_data")
        return self.data

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        
        products_data = []
        products = soup.find_all('div', class_=lambda c: c and 'product' in c.lower())
        
        for p in products[:15]: # limite à 15 produits pour éviter de surcharger le site
            try:
                title = p.find(['h2', 'h3']).text.strip()
                products_data.append({"titre": title, "source": "Kiprix"})
            except:
                pass
        
        print(f"✅ {len(products_data)} produits Kiprix trouvés !")
        return products_data