# import de la classe de base
from .base_scraper import BaseScraper

# typage pour rendre le code plus lisible
from typing import List, Dict, Optional

# regex pour nettoyer téléphone et extraire email
import re

# parser html
from bs4 import BeautifulSoup


# classe spécialisée pour scraper des entreprises
class BusinessScraper(BaseScraper):

    def __init__(self):
        # initialise le scraper avec lurl du site
        super().__init__(base_url="https://www.bizouk.com", delay=5)

    # nettoie un numéro de téléphone
    def clean_phone(self, phone: str) -> str:

        # garde uniquement les chiffres
        digits = re.sub(r"\D", "", phone)

        # enlève lindicatif international si présent
        if digits.startswith("596"):
            digits = digits[3:]

        # reformate si le numéro semble valide
        if len(digits) == 9:
            return f"0596 {digits[1:3]} {digits[3:5]} {digits[5:7]}"

        # sinon retourne le téléphone nettoyé
        return phone.strip()

    # cherche un email dans un texte
    def extract_email(self, text: str) -> Optional[str]:

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        return match.group(0) if match else None

    # parse une carte entreprise
    def parse_business(self, business_soup: BeautifulSoup) -> Dict:

        # récupère le nom
        name_tag = business_soup.select_one("h2")
        name = name_tag.get_text(strip=True) if name_tag else None

        # récupère ladresse
        address_tag = business_soup.select_one(".address")
        address = address_tag.get_text(strip=True) if address_tag else None

        # récupère le téléphone
        phone_tag = business_soup.select_one(".phone")
        phone = self.clean_phone(phone_tag.get_text()) if phone_tag else None

        # récupère tout le texte pour chercher un email
        text_blob = business_soup.get_text(" ")
        email = self.extract_email(text_blob)

        # récupère la description
        desc_tag = business_soup.select_one(".description")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # retourne les données sous forme de dictionnaire
        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "description": description,
        }

    # méthode demandée par BaseScraper
    # parse une page complète
    def parse(self, soup: BeautifulSoup) -> List[Dict]:

        results = []

        # sélectionne toutes les cartes entreprise
        cards = soup.select(".business-card")

        # parcourt les cartes
        for card in cards:
            results.append(self.parse_business(card))

        return results

    # scrape une catégorie complète
    def scrape_category(self, category: str, max_results: int = 50) -> List[Dict]:

        results = []
        page = 1

        while len(results) < max_results:

            # construit lurl de la page
            url = f"{self.base_url}/{category}?page={page}"

            # récupère la page
            soup = self.fetch_page(url)

            if not soup:
                break

            # parse la page
            businesses = self.parse(soup)

            for b in businesses:
                results.append(b)

                if len(results) >= max_results:
                    break

            page += 1

        return results

    # méthode principale demandée par BaseScraper
    def scrape(self) -> List[Dict]:

        # scrape par défaut la catégorie restaurants
        return self.scrape_category("restaurants")