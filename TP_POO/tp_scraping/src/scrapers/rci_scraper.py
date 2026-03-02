import time
import os
import json
import re
from datetime import datetime
from typing import List, Dict

from src.base_scraper import BaseScraper

url_rci = "https://rci.fm/deuxiles/infos/toutes-les-infos"
url_rci_root = "https://rci.fm"

class RciScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url, delay=120)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.raw_data_dir = os.path.join(project_root, "data", "raw", "rci")
        self.processed_data_dir = os.path.join(project_root, "data", "processed")
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
        self.root_url = url_rci_root

    def scrape(self, max_articles: int = 10):
        """Scrape les articles depuis la page principale et sauvegarde le HTML brut"""
        print(f"Début du scraping depuis {self.base_url}")
        
        # Ajouter la listes des articles deja present
        output_path = os.path.join(self.processed_data_dir, "rci.json")
        existing_titles = set()
        if os.path.exists(output_path):
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, dict):
                        existing_titles = set(existing_data.keys())
                        print(f"Chargé {len(existing_titles)} titres existants pour éviter les doublons")
            except (json.JSONDecodeError, OSError) as e:
                print(f"Avertissement: impossible de charger rci.json: {e}")
        
        # Récupérer la page principale
        soup = self.fetch_page(self.base_url)
        if not soup:
            print("Échec de récupération de la page principale")
            return []
        
        # Trouver tous les articles
        articles = soup.find_all(attrs={"role": "article"})
        print(f"Trouvé {len(articles)} articles")
        
        scraped_count = 0
        skipped_count = 0
        article_urls = []
        
        for article in articles[:max_articles]:
            if 'about' not in article.attrs:
                continue
            
            article_url = f"{self.root_url}{article.attrs['about']}"
            article_urls.append(article_url)
            
            # Récupérer le HTML de l'article
            print(f"Scraping: {article_url}")
            article_soup = self.fetch_page(article_url)
            
            if not article_soup:
                print(f"  Échec de récupération: {article_url}")
                continue
            
            # Extraire le titre pour vérifier les doublons
            titre_elem = article_soup.find("h1", attrs={"itemprop": "name"})
            if titre_elem:
                titre = titre_elem.text.strip()
                if titre in existing_titles:
                    print(f"  Déjà scrapé (ignoré): {titre}")
                    skipped_count += 1
                    continue
            
            # Générer un nom de fichier unique basé sur l'URL
            filename = self.url_to_filename(article_url)
            filepath = os.path.join(self.raw_data_dir, filename)
            
            # Sauvegarder le HTML brut
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(article_soup))
            
            print(f"  Sauvegardé: {filepath}")
            scraped_count += 1
        
        print(f"\nScraping terminé: {scraped_count} nouveaux articles sauvegardés, {skipped_count} doublons ignorés")
        print(f"Dossier: {self.raw_data_dir}")
        return article_urls

    def parse(self):
        """Parse les fichiers HTML bruts et alimente un JSON cumulatif"""
        print(f"Début du parsing depuis {self.raw_data_dir}")
        
        # Lister tous les fichiers HTML dans le dossier raw
        html_files = [f for f in os.listdir(self.raw_data_dir) if f.endswith('.html')]
        print(f"Trouvé {len(html_files)} fichiers à parser")
        
        output_path = os.path.join(self.processed_data_dir, "rci.json")

        # Charger les données existantes pour ne pas les écraser
        if os.path.exists(output_path):
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    all_articles = json.load(f)
                if not isinstance(all_articles, dict):
                    all_articles = {}
            except (json.JSONDecodeError, OSError):
                all_articles = {}
        else:
            all_articles = {}

        parsed_count = 0
        
        for html_file in html_files:
            html_path = os.path.join(self.raw_data_dir, html_file)
            
            print(f"Parsing: {html_file}")
            
            # Lire le HTML brut
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Extraire les données structurées
            article_data = self.extract_article_data(soup)
            
            if not article_data:
                print(f"  Échec de parsing: {html_file}")
                continue
            
            # Titre comme clé principale, le reste des métadonnées comme valeur
            title = article_data.pop("titre", None)
            if not title:
                print(f"  Titre manquant, article ignoré: {html_file}")
                continue

            title = title.replace("\r\n", " ").replace("\n", " ")

            for key, value in article_data.items():
                if isinstance(value, str):
                    article_data[key] = value.replace("\r\n", " ").replace("\n", " ")
                elif isinstance(value, list):
                    article_data[key] = [
                        item.replace("\r\n", " ").replace("\n", " ") if isinstance(item, str) else item
                        for item in value
                    ]

            all_articles[title] = article_data
            print(f"  Fusionné: {title}")
            
            # Supprimer le fichier HTML après traitement
            os.remove(html_path)
            print(f"  Supprimé: {html_file}")
            parsed_count += 1

        # Sauvegarder le JSON cumulatif unique
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)

        print(f"\nParsing terminé: {parsed_count} articles fusionnés dans {output_path}")
        return parsed_count
    
    def extract_article_data(self, soup):
        """Extrait les données du HTML de l'article"""

        article_data={}

        # Extraire le titre
        titre_elem = soup.find("h1", attrs={"itemprop": "name"})
        if not titre_elem:
            return None
        
        article_data["titre"] = titre_elem.text.strip()
        
        # Extraire l'auteur avec itemprop="author"
        auteur_elem = soup.find(attrs={"itemprop": "author"})
        if auteur_elem:
            article_data["auteur"] = auteur_elem.text.strip()

        infos_elems = soup.find_all(attrs={"class": " info"})
        article_data["infos"] = [info.text.strip() for info in infos_elems]
        
        for info in article_data["infos"]:
            
            date_match = re.search(r'\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2}', info)
            if date_match:
                article_data["date"] = date_match.group(0)
        
        # Extraire le contenu
        contenu_elems = soup.find_all(attrs={"property": "schema:text"})
        article_data["contenu"] = [content.text.strip() for content in contenu_elems]
        
        # Créer l'objet 
        article_data["date_extraction"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        return article_data
    
    def url_to_filename(self, url):
        """Convertit l'URL en nom de fichier"""
        # Extraire la partie après le domaine
        filename = url.replace(self.root_url, "")
        filename = filename.strip("/")
        
        # Remplacer les caractères invalides
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'/', '_', filename)
        
        # Limiter la longueur
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename + ".html"
    
    def sanitize_filename(self, filename):
        """Retire les caracteres indesirables"""
        filename = filename.strip()
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename[:200]  # Limit filename length


    

