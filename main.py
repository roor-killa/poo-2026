# Import du scraper Bizouk
from src.scrapers.bizouk_scraper import BizoukScraper


def main():

    # Création de l'objet scraper
    scraper = BizoukScraper()

    # Lancement du scraping
    scraper.scrape()

    # Sauvegarde des résultats
    scraper.save_to_json("data/raw/bizouk.json")

    scraper.save_to_csv("data/raw/bizouk.csv")

    print("Scraping terminé")


# Vérifie que le fichier est exécuté directement
if __name__ == "__main__":
    main()