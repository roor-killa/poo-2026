# Import du scraper Bizouk
from bizouk_scraper import BizoukScraper


def main():

    # Création de l'objet scraper
    scraper = BizoukScraper()

    # Lancement du scraping
    data = scraper.scrape()

    # Sauvegarde des résultats
    scraper.save_to_json(data, "data/raw/bizouk.json")
    
    print("Scraping terminé")


# Vérifie que le fichier est exécuté directement
if __name__ == "__main__":
    main()