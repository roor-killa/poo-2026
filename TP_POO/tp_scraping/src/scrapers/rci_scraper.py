
from ..base_scraper import base_scraper
import time

url_rci = "https://rci.fm/deuxiles/infos/toutes-les-infos"
url_rci_root = "https://rci.fm"

class RciScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)

    def scrape(self):
        soup = self.fetch_page(self.base_url)

        if soup:
            headlines = soup.find_all(attrs={"role": "article"})
            for h in headlines[:2]:
                print('----------------------------------------------------------------------------------------------------------------------------------')
                
                test_article_url = f"{url_rci_root}{h.attrs['about']}"
                print(test_article_url)
                print('Waiting')
                time.sleep(120)

                new_fetch = self.fetch_page(test_article_url)
                new_headlines = new_fetch.find_all(attrs={"role": "article"})
                for n_h in new_headlines:
                    print(f"{url_rci_root}{n_h.attrs['about']}")

    def parse(self):
        print("Parsing content")      




