
from base_scraper import BaseScraper
import time

url_rci = "https://rci.fm/deuxiles/infos/toutes-les-infos"
url_rci_root = "https://rci.fm"

class RciScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)

    def scrape(self):
        print(f"Scraping {self.url}")

    def parse(self):
        print("Parsing content")      




new_scrap = RciScraper(url_rci)
soup= new_scrap.fetch_page(new_scrap.base_url)

if soup:
    headlines = soup.find_all(attrs={"role": "article"})
    for h in headlines[:2]:
        print('----------------------------------------------------------------------------------------------------------------------------------')
        
        test_article_url = f"{url_rci_root}{h.attrs['about']}"
        print(test_article_url)
        print('Waiting')
        time.sleep(120)

        new_fetch = new_scrap.fetch_page(test_article_url)
        new_headlines = new_fetch.find_all(attrs={"role": "article"})
        for n_h in new_headlines:
            print(f"{url_rci_root}{n_h.attrs['about']}")