from scrapers.business_scraper import BusinessScraper
from scrapers.event_scraper import EventScraper
from scrapers.news_scraper import NewScraper


def main():
    choice = input("choisis business, news ou events ").strip().lower()

    if choice == "business":
        scraper = BusinessScraper()
        data = scraper.scrape()
        print(data)
        scraper.save_to_json(data, "data/business.json")
        scraper.close()
        return

    if choice == "news":
        scraper = NewScraper(category="soirees/agenda/region/martinique")
        data = scraper.scrape(max_pages=2)
        print(data)
        scraper.save_to_json(data, "data/news.json")
        scraper.close()
        return

    if choice == "events":
        scraper = EventScraper(region="martinique")
        data = scraper.scrape(max_pages=1, max_events=12)
        print(data)
        scraper.save_to_json(data, "data/events.json")
        scraper.close()
        return

    print("choix invalide")


if __name__ == "__main__":
    main()
