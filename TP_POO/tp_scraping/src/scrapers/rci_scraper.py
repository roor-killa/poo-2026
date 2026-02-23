
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
if soup:
    headlines = soup.find_all(class_='data')

    print(headlines)
    print('------------------------------------')
    for h in headlines:
        list_p = h.find_all('p')
        for p in list_p:
            print(p.text)

        list_h2 = h.find_all('h2')
        for h2 in list_h2:
            print(h2.text)

        list_span = h.find_all('span')
        for span in list_span:
            print(span.text)