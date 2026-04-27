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
        
        # On cible les conteneurs de films
        items = soup.find_all(['div', 'article'], class_=re.compile(r'movie|item|film', re.I))
        
        # Si on ne trouve rien par classe, on prend tous les liens de films
        if not items:
            items = [a.find_parent('div') for a in soup.find_all('a', href=True) if '/movies/' in a['href']]

        for item in items:
            if not item: continue
            
            # 1. Titre et Lien
            link_tag = item.find('a', href=True)
            if not link_tag or '/movies/' not in link_tag['href']: continue
            titre = link_tag.text.strip()
            
            # 2. Image
            img_tag = item.find('img')
            image_url = ""
            if img_tag:
                image_url = img_tag.get('data-src') or img_tag.get('src') or ""
                if image_url.startswith('/'): image_url = "https://madiana.com" + image_url
            
            # 3. Synopsis (On prend tout le texte du bloc qui n'est pas le titre)
            all_text = item.get_text(separator=' ', strip=True)
            synopsis = all_text.replace(titre, "").strip()
            # On nettoie un peu les horaires du synopsis
            synopsis = re.sub(r'\d{1,2}[:hH]\d{2}', '', synopsis).strip()
            
            if len(synopsis) < 10:
                synopsis = "Cliquez pour voir les détails de ce film sur le site officiel."

            # 4. Horaires
            horaires = "Consulter le site"
            heures_trouvees = re.findall(r'\d{1,2}[:hH]\d{2}', all_text)
            if heures_trouvees:
                horaires = " | ".join(heures_trouvees[:5]).lower().replace(':', 'h')

            if titre and len(titre) > 2:
                movies_data.append({
                    "titre": titre,
                    "horaires": horaires,
                    "image": image_url,
                    "synopsis": synopsis,
                    "source": "Madiana"
                })
                
        return movies_data