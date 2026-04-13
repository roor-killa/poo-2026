from src.scrapers.rci_scraper import RCIScraper
from src.scrapers.bizouk_scraper import BizoukScraper
from src.scrapers.kiprix_scraper import KiprixScraper
from src.scrapers.madiana_scraper import MadianaScraper

class ScraperManager:
    """
    Manager utilisant le Design Pattern FACTORY.
    Il est responsable d'instancier le bon scraper en fonction du site demandé.
    """
    
    @staticmethod
    def create_scraper(site_name: str):
        """Pattern Factory : retourne l'objet scraper correspondant."""
        site_name = site_name.lower()
        
        if site_name == "rci":
            return RCIScraper()
        elif site_name == "bizouk":
            return BizoukScraper()
        elif site_name == "kiprix":
            return KiprixScraper()
        elif site_name == "madiana":
            return MadianaScraper()
        else:
            raise ValueError(f"❌ Scraper inconnu : {site_name}")

    def run_all(self):
        """Lance tous les scrapers un par un."""
        sites = ["rci", "bizouk", "kiprix", "madiana"]
        toutes_les_donnees = []
        
        print("\n" + "="*50)
        print("🛠️ DÉMARRAGE DU SCRAPING GLOBAL")
        print("="*50 + "\n")

        for site in sites:
            try:
                scraper = self.create_scraper(site)
                donnees = scraper.scrape()
                toutes_les_donnees.extend(donnees)
            except Exception as e:
                print(f"⚠️ Échec du scraping pour {site} : {e}")
                
        print("\n" + "="*50)
        print(f"🏁 SCRAPING TERMINÉ ! Total de {len(toutes_les_donnees)} éléments récoltés.")
        print("="*50)
        
        return toutes_les_donnees