from scrapers.business_scraper import BusinessScraper
from scrapers.news_scraper import NewScraper


def main():
    # choisit quel scraper lancer
    choice = input("choisis business ou news ").strip().lower()

    # lance le scraper business
    if choice == "business":
        scraper = BusinessScraper()
        data = scraper.scrape()
        print(data)
        scraper.save_to_json(data, "data/business.json")
        scraper.close()
        return

    # lance le scraper news
    if choice == "news":
        scraper = NewScraper(category="actualites")
        data = scraper.scrape(max_pages=2)
        print(data)
        scraper.save_to_json(data, "data/news.json")
        scraper.close()
        return

    # affiche un message si le choix nest pas bon
    print("choix invalide")


if __name__ == "__main__":
    main()