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
        
        # On récupère tous les liens qui pointent vers un film
        liens_films = soup.find_all('a', href=True)
        films_extraits = [] 

        for lien in liens_films:
            if '/movies/' in lien['href']:
                t = lien.text.strip()
                image_url = ""
                synopsis = "Aucune description disponible." 
                
                # 1. Extraction de l'image (Gestion Lazy-Loading)
                img = lien.find('img')
                if img:
                    image_url = img.get('data-src') or img.get('src') or ''
                    if image_url.startswith('/'):
                        image_url = "https://madiana.com" + image_url
                    if not t and img.get('alt'): 
                        t = img.get('alt').strip()

                # 2. Extraction du Synopsis (Version améliorée)
                # On cherche un conteneur parent qui englobe tout le bloc du film
                parent = lien.find_parent(['div', 'article', 'li'])
                if parent:
                    # On cherche dans les classes qui contiennent souvent le résumé
                    # On essaye plusieurs cibles courantes sur Madiana
                    cible = parent.find(['p', 'div', 'span'], class_=re.compile(r'synopsis|description|resume|text|content', re.I))
                    
                    if cible:
                        synopsis = cible.text.strip()
                    else:
                        # Si on ne trouve pas de classe spécifique, on prend le premier paragraphe 
                        # de plus de 30 caractères (pour éviter de prendre les horaires par erreur)
                        for p in parent.find_all(['p', 'div']):
                            txt = p.text.strip()
                            if len(txt) > 30 and not any(h in txt.lower() for h in [":", "h", "séances"]):
                                synopsis = txt
                                break

                # Nettoyage et limitation de la longueur du synopsis
                if synopsis:
                    synopsis = synopsis.replace('\n', ' ').replace('\r', '').strip()
                    if len(synopsis) > 160:
                        synopsis = synopsis[:157] + "..."

                if t and len(t) > 2 and t not in ["Bande-annonce", "Places", "Infos & horaires", "A l'affiche"]:
                    deja_present = any(f['titre'] == t for f in films_extraits)
                    if not deja_present:
                        films_extraits.append({'titre': t, 'image': image_url, 'synopsis': synopsis})

        # Association des horaires
        texte_page = soup.get_text(separator=' | ', strip=True)
        for film in films_extraits:
            titre = film['titre']
            horaires = "Non spécifié"
            if titre in texte_page:
                index_debut = texte_page.find(titre) + len(titre)
                zone_recherche = texte_page[index_debut : index_debut + 500]
                heures_trouvees = re.findall(r'\d{1,2}[:hH]\d{2}', zone_recherche)
                if heures_trouvees:
                    horaires = " | ".join(heures_trouvees[:5]).lower().replace(':', 'h')

            movies_data.append({
                "titre": titre,
                "horaires": horaires,
                "image": film['image'],
                "synopsis": film['synopsis'],
                "source": "Madiana"
            })
                
        print(f"🎬 {len(movies_data)} films extraits avec synopsis.")
        return movies_data