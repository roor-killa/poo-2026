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
        
        # On cherche tous les liens de films
        liens = soup.find_all('a', href=True)
        films_extraits = []

        for lien in liens:
            href = lien['href']
            if '/movies/' in href:
                # On évite les doublons
                titre = lien.text.strip()
                if not titre or len(titre) < 2 or titre in ["Bande-annonce", "Places", "A l'affiche"]:
                    continue
                
                if any(f['titre'] == titre for f in films_extraits):
                    continue

                # --- 1. IMAGE (On cherche l'image dans le lien ou juste à côté) ---
                image_url = ""
                img_tag = lien.find('img') or (lien.find_parent() and lien.find_parent().find('img'))
                if img_tag:
                    image_url = img_tag.get('data-src') or img_tag.get('src') or ""
                    if image_url.startswith('/'):
                        image_url = "https://madiana.com" + image_url

                # --- 2. HORAIRES (On cherche dans le texte global autour du titre) ---
                horaires = "Consulter le site"
                # On cherche dans le bloc parent pour trouver les heures
                bloc_parent = lien.find_parent(['div', 'article'])
                texte_recherche = bloc_parent.get_text() if bloc_parent else soup.get_text()
                
                # On cherche les formats 14h30 ou 14:30
                heures = re.findall(r'\d{1,2}[:hH]\d{2}', texte_recherche)
                if heures:
                    # On filtre pour ne garder que les heures après le titre dans le flux
                    horaires = " | ".join(heures[:5]).lower().replace(':', 'h')

                # --- 3. DESCRIPTION (On prend un texte par défaut si le site cache tout) ---
                synopsis = f"Découvrez les séances pour le film '{titre}' au cinéma Madiana. Cliquez pour plus d'infos."
                
                films_extraits.append({
                    "titre": titre,
                    "image": image_url,
                    "horaires": horaires,
                    "synopsis": synopsis
                })

        for f in films_extraits:
            movies_data.append({
                "titre": f["titre"],
                "horaires": f["horaires"],
                "image": f["image"],
                "synopsis": f["synopsis"],
                "source": "Madiana"
            })
                
        return movies_data