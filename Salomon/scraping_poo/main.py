from scraper.business_scraper import BusinessScraper

# crée le scraper
scraper = BusinessScraper()

# lance le scraping
data = scraper.scrape()

# sauvegarde les données
scraper.save_to_json(data, "data/business.json")

# ferme la session
scraper.close()