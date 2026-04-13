from bs4 import BeautifulSoup
from typing import List, Dict
from src.base_scraper import BaseScraper

class BizoukScraper(BaseScraper):
    """Scraper spécifique pour le site Bizouk (Événements aux Antilles)."""

    def __init__(self):
        # cible les événements en Martinique
        super().__init__(base_url="https://www.bizouk.com/events/martinique", delay=2.0)

    def scrape(self, max_pages: int = 1) -> List[Dict]:
        print("🚀 Lancement du scraper Bizouk...")
        soup = self.fetch_page(self.base_url)
        
        if soup:
            self.data = self.parse(soup)
            self.save_to_json("bizouk_data")
        else:
            print("❌ Impossible de récupérer la page Bizouk.")
            
        return self.data

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        events_data = []
        
        
        for block in soup.find_all(['div', 'article', 'li']):
            try:
                title_tag = block.find(['h2', 'h3'])
                link_tag = block.find('a', href=True)
                
                if title_tag and link_tag:
                    title = title_tag.text.strip()
                    link = link_tag['href']
                    
                    if link and not link.startswith('http'):
                        link = "https://www.bizouk.com" + link
                        
                    # on évite les doublons et les titres vides
                    if title and len(title) > 3 and not any(e['titre'] == title for e in events_data):
                        events_data.append({
                            "titre": title,
                            "lien": link,
                            "source": "Bizouk"
                        })
            except:
                continue
                
        print(f"✅ {len(events_data)} événements Bizouk trouvés et extraits !")
        return events_data
        
        
        events = soup.find_all('div', class_=lambda c: c and ('event' in c.lower() or 'card' in c.lower()))
        
        for event in events:
            try:
                # titre
                title_tag = event.find(['h2', 'h3', 'h4'])
                title = title_tag.text.strip() if title_tag else None
                
                if not title:
                    continue # passe si pas de titre trouvé

                # lien
                link_tag = event.find('a', href=True)
                link = link_tag['href'] if link_tag else ""
                if link and not link.startswith('http'):
                    link = "https://www.bizouk.com" + link

                
                date_tag = event.find('span', class_=lambda c: c and 'date' in c.lower())
                date_event = date_tag.text.strip() if date_tag else "Date non précisée"

                events_data.append({
                    "titre": title,
                    "lien": link,
                    "date": date_event,
                    "source": "Bizouk"
                })
            except Exception as e:
                pass
                
        print(f"✅ {len(events_data)} événements Bizouk trouvés et extraits !")
        return events_data