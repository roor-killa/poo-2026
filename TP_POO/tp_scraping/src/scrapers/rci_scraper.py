
from base_scraper import BaseScraper

url_rci = "https://rci.fm/deuxiles"

class RciScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)

    def scrape(self):
        print(f"Scraping {self.url}")

    def parse(self):
        print("Parsing content")


new_scrap = RciScraper(url_rci)
soup= new_scrap.fetch_page(new_scrap.base_url)

print()
print('---------')
headlines = soup.find_all("h3")

print(headlines)
for h in headlines:
    print(h.text)