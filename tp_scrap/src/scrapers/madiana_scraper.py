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
        """
        Version 'Text Scanner' : Récupère tout le texte de la page pour
        être sûr de ne rater aucune heure cachée.
        """
        movies_data = []
        import re
        
        # 1. On récupère tout le texte propre de la page
        texte_page = soup.get_text(separator=' | ', strip=True)
        
        # 2. On récupère la liste des titres de films via les liens (ta méthode sniper qui marche)
        liens_films = soup.find_all('a', href=True)
        titres_extraits = []
        for lien in liens_films:
            if '/movies/' in lien['href']:
                t = lien.text.strip()
                if not t:
                    img = lien.find('img')
                    if img and img.get('alt'): t = img.get('alt').strip()
                if t and len(t) > 2 and t not in ["Bande-annonce", "Places", "Infos & horaires", "A l'affiche"]:
                    if t not in titres_extraits: titres_extraits.append(t)

        # 3. Pour chaque titre, on cherche l'horaire qui se trouve JUSTE APRÈS dans le texte
        for titre in titres_extraits:
            horaires = "Non spécifié"
            
            # On cherche la position du titre dans le grand bloc de texte
            if titre in texte_page:
                # On prend les 500 caractères qui suivent le titre du film
                index_debut = texte_page.find(titre) + len(titre)
                zone_recherche = texte_page[index_debut : index_debut + 500]
                
                # On cherche des formats type 14:30 ou 14h30
                heures_trouvees = re.findall(r'\d{1,2}[:hH]\d{2}', zone_recherche)
                
                if heures_trouvees:
                    # On garde les 5 premières heures trouvées (pour éviter de prendre le film suivant)
                    horaires = " | ".join(heures_trouvees[:5]).lower().replace(':', 'h')

            movies_data.append({
                "titre": titre,
                "horaires": horaires,
                "source": "Madiana"
            })
                
        print(f"✅ {len(movies_data)} films analysés avec recherche d'horaires.")
        return movies_data