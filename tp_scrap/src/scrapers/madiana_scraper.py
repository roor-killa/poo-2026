from bs4 import BeautifulSoup
from typing import List, Dict
from src.base_scraper import BaseScraper


# Ces bibliothèques permettent d'ouvrir un "vrai" navigateur pour lire le JavaScript
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

class MadianaScraper(BaseScraper):
    """
    Classe héritant de BaseScraper.
    Spécialité : Gérer un site dynamique dont le contenu apparaît via JavaScript.
    """
    def __init__(self):
        # Appel du constructeur parent avec l'URL cible
        super().__init__(base_url="https://madiana.com/horaires/", delay=2.0)

    def fetch_page_dynamique(self, url: str) -> BeautifulSoup | None:
        print(f"🌍 Connexion dynamique (Selenium) à : {url}")
        
        # --- CONFIGURATION DOCKER-FRIENDLY ---
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Obligatoire : pas d'écran
        chrome_options.add_argument("--no-sandbox") # OBLIGATOIRE pour Docker
        chrome_options.add_argument("--disable-dev-shm-usage") # OBLIGATOIRE (évite le crash mémoire)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222") # Optionnel mais aide à la stabilité
        
        try:
            # On laisse ChromeDriverManager gérer le binaire, mais on ajoute nos options
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Temps d'attente pour le réseau du VPS (parfois plus lent que chez toi)
            driver.set_page_load_timeout(30) 
            
            driver.get(url)
            
            print("⏳ Attente du chargement des affiches (8 secondes)...")
            time.sleep(8) 
            
            html_final = driver.page_source
            driver.quit() 
            
            return BeautifulSoup(html_final, 'lxml')
        except Exception as e:
            print(f"❌ Erreur Selenium : {e}")
            return None
        
    def scrape(self, max_pages: int = 1) -> List[Dict]:
        """Orchestre la récupération et la sauvegarde des données."""
        print("🚀 Lancement du scraper Madiana (Version Selenium Sniper)...")
        
        # On utilise notre méthode dynamique au lieu de la méthode classique du parent
        soup = self.fetch_page_dynamique(self.base_url)
        
        if soup:
            self.data = self.parse(soup)
            self.save_to_json("madiana_data")
            
        return self.data

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        movies_data = []
        import re
        
        liens_films = soup.find_all('a', href=True)
        films_extraits = [] 

        for lien in liens_films:
            if '/movies/' in lien['href']:
                t = lien.text.strip()
                image_url = ""
                ba_url = "#" # Lien par défaut si rien n'est trouvé
                
                # 1. Image
                img = lien.find('img')
                if img:
                    image_url = img.get('data-src') or img.get('src') or ''
                    if image_url.startswith('/'):
                        image_url = "https://madiana.com" + image_url
                        
                # 2. BANDE-ANNONCE (On cherche un lien vers la BA dans le même bloc)
                parent = lien.find_parent('div')
                if parent:
                    # On cherche un lien qui contient 'youtube' ou 'trailer' ou 'bande-annonce'
                    ba_tag = parent.find('a', href=True, string=re.compile(r'Bande-annonce|Trailer', re.I))
                    if ba_tag:
                        ba_url = ba_tag['href']
                        if ba_url.startswith('/'):
                            ba_url = "https://madiana.com" + ba_url

                if t and len(t) > 2 and t not in ["Bande-annonce", "Places", "Infos & horaires"]:
                    if not any(f['titre'] == t for f in films_extraits):
                        films_extraits.append({'titre': t, 'image': image_url, 'ba': ba_url})

        # Horaires
        texte_page = soup.get_text(separator=' | ', strip=True)
        for film in films_extraits:
            titre = film['titre']
            horaires = "Non spécifié"
            if titre in texte_page:
                idx = texte_page.find(titre) + len(titre)
                heures = re.findall(r'\d{1,2}[:hH]\d{2}', texte_page[idx : idx + 500])
                if heures:
                    horaires = " | ".join(heures[:5]).lower().replace(':', 'h')

            movies_data.append({
                "titre": titre,
                "horaires": horaires,
                "image": film['image'],
                "ba": film['ba'], # On stocke le lien ici
                "source": "Madiana"
            })
                
        return movies_data