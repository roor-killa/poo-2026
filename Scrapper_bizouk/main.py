"""
Script console historique du projet.

Le projet utilise maintenant surtout backend/app/main.py pour l'API FastAPI,
mais ce fichier reste pratique pour tester un scraper directement dans le terminal
sans passer par Docker, nginx ou le frontend.
"""

from scrapers.business_scraper import BusinessScraper
from scrapers.event_scraper import EventScraper
from scrapers.news_scraper import NewScraper


def main():
    """Demande quel scraper lancer, execute la collecte, puis sauvegarde le JSON."""

    # L'utilisateur choisit le type de scraping depuis le terminal.
    choice = input("choisis business, news ou events ").strip().lower()

    if choice == "business":
        # BusinessScraper correspond a l'ancien scraping des restaurants.
        scraper = BusinessScraper()
        data = scraper.scrape()
        print(data)
        scraper.save_to_json(data, "data/business.json")
        scraper.close()
        return

    if choice == "news":
        # NewScraper reste un scraper generique pour des blocs agenda/news.
        scraper = NewScraper(category="soirees/agenda/region/martinique")
        data = scraper.scrape(max_pages=2)
        print(data)
        scraper.save_to_json(data, "data/news.json")
        scraper.close()
        return

    if choice == "events":
        # EventScraper est le scraper principal pour la demonstration Bizouk.
        scraper = EventScraper(region="martinique")
        data = scraper.scrape(max_pages=1, max_events=12)
        print(data)
        scraper.save_to_json(data, "data/events.json")
        scraper.close()
        return

    print("choix invalide")


# Cette condition evite que main() se lance si le fichier est importe depuis un autre module.
if __name__ == "__main__":
    main()
