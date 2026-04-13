from bs4 import BeautifulSoup
from typing import List, Dict


from src.base_scraper import BaseScraper

class RCIScraper(BaseScraper):
    """Scraper spécifique pour le site d'actualités rci.fm (Martinique)."""

    def __init__(self):
       
        super().__init__(base_url="https://www.rci.fm/martinique/infos/toutes-les-infos", delay=2.0)

    def scrape(self, max_pages: int = 1) -> List[Dict]:
        """Méthode principale pour orchestrer le scraping de RCI."""
        print(f"🚀 Lancement du scraper RCI...")
        
        # 1. télécharge la page HTML
        soup = self.fetch_page(self.base_url)
        
        if soup:
            # 2. analyse le HTML pour extraire les articles
            self.data = self.parse(soup)
            
            # 3. sauvegarde des données (dans data/raw/rci_data.json)
            self.save_to_json("rci_data")
        else:
            print("❌ Impossible de récupérer la page principale.")
            
        return self.data

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait les articles de l'objet BeautifulSoup."""
        articles_data = []
        
        #  cherche toutes les balises <article> sur la page
        articles = soup.find_all('article')
        
        for article in articles:
            try:
                # on cherche le titre (souvent dans un h2 ou h3)
                title_tag = article.find('h2') or article.find('h3')
                title = title_tag.text.strip() if title_tag else "Titre inconnu"
                
                # le lien de l'article
                link_tag = article.find('a', href=True)
                link = link_tag['href'] if link_tag else ""
                
                
                if link and not link.startswith('http'):
                    link = "https://www.rci.fm" + link
                
                
                if title != "Titre inconnu":
                    articles_data.append({
                        "titre": title,
                        "lien": link,
                        "source": "RCI"
                    })
            except Exception as e:
                print(f"⚠️ Erreur mineure sur un article : {e}")
                
        print(f"✅ {len(articles_data)} articles trouvés et extraits !")
        return articles_data