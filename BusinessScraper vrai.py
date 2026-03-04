# scrapers/business_scraper.py

from .base_scraper import BaseScraper
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re


class BusinessScraper(BaseScraper):

    def __init__(self):
        super().__init__(base_url="https://www.pagesjaunes.fr/annuaire/martinique", delay=2.0)

    def clean_phone(self, phone: str) -> str:
        """
        Nettoie un numéro de téléphone.
        Format attendu : 0596 XX XX XX
        """

        # Supprime tout sauf les chiffres
        digits = re.sub(r"\D", "", phone)

        if len(digits) == 10 and digits.startswith("0596"):
            # Reformate
            return f"{digits[:4]} {digits[4:6]} {digits[6:8]} {digits[8:]}"
        
        return phone  # retourne original si invalide

    def extract_email(self, text: str) -> Optional[str]:
        """
        Recherche une adresse email avec regex.
        """
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        return match.group(0) if match else None

    def parse_business(self, business_soup: BeautifulSoup) -> Dict:

        name = business_soup.find("h1")
        name = name.text.strip() if name else "Nom inconnu"

        address = business_soup.find("div", class_="address")
        address = address.text.strip() if address else None

        phone = business_soup.find("span", class_="phone")
        phone = self.clean_phone(phone.text) if phone else None

        text_content = business_soup.text
        email = self.extract_email(text_content)

        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email
        }

    def scrape_category(self, category: str, max_results: int = 50) -> List[Dict]:

        url = f"{self.base_url}/{category}"

        soup = self.fetch_page(url)
        if not soup:
            return []

        results = []
        businesses = soup.find_all("article")[:max_results]

        for business in businesses:
            data = self.parse_business(business)
            data["category"] = category
            results.append(data)

        return results