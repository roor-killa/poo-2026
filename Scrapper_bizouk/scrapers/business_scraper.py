from typing import Dict, List, Optional
import re

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class BusinessScraper(BaseScraper):
    """Ancien scraper du projet: il recupere des fiches restaurants Bizouk."""

    def __init__(self):
        """Initialise le scraper avec l'URL de base du site Bizouk."""
        super().__init__(base_url="https://www.bizouk.com", delay=2)

    def clean_phone(self, phone: str) -> str:
        """Nettoie un numero en gardant seulement les chiffres et le signe plus."""
        phone = phone.strip()
        digits = re.sub(r"[^\d+]", "", phone)
        return digits if digits else phone

    def extract_email(self, text: str) -> Optional[str]:
        """Cherche une adresse email dans un bloc de texte."""
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Cherche un numero antillais dans un bloc de texte."""
        match = re.search(
            r"(\+596|\+590|0596|0590|0696|0690)[\s\-\.]?\d{2}[\s\-\.]?\d{2}[\s\-\.]?\d{2}[\s\-\.]?\d{2}",
            text,
        )
        return self.clean_phone(match.group(0)) if match else None

    def get_restaurant_links(self, soup: BeautifulSoup) -> List[str]:
        """Recupere les liens uniques vers les fiches detail restaurants."""
        links = []
        seen = set()

        for a in soup.select("a[href]"):
            href = a.get("href", "").strip()

            if "/restaurants/details/" not in href:
                continue

            if href.startswith("/"):
                full_url = f"{self.base_url}{href}"
            elif href.startswith("http"):
                full_url = href
            else:
                full_url = f"{self.base_url}/{href}"

            if full_url not in seen:
                seen.add(full_url)
                links.append(full_url)

        return links

    def parse_business_detail(self, soup: BeautifulSoup, url: str) -> Dict:
        """Analyse une fiche restaurant pour extraire nom, adresse, contact et description."""
        name = None
        title_tag = soup.select_one("h1")
        if title_tag:
            name = title_tag.get_text(strip=True)

        address = None
        if title_tag:
            current = title_tag.find_next(string=True)

            while current:
                text = current.strip()

                if (
                    text
                    and text != name
                    and "voir le plan d'acces" not in text.lower()
                    and "contacter la boutique" not in text.lower()
                ):
                    if re.search(r"\b\d{5}\b", text):
                        address = text
                        break

                current = current.find_next(string=True)

        text_blob = soup.get_text(" ", strip=True)
        email = self.extract_email(text_blob)
        phone = self.extract_phone(text_blob)

        description = ""
        desc_title = soup.find(
            ["h2", "h3", "strong"],
            string=re.compile(r"description", re.IGNORECASE),
        )

        if desc_title:
            parts = []
            current = desc_title.find_next(string=True)

            while current:
                text = current.strip()

                if text.lower() in [
                    "partager cet evenement",
                    "copier ce lien",
                    "votre panier",
                    "vos articles",
                    "contacter la boutique",
                    "",
                ]:
                    break

                if text:
                    parts.append(text)

                current = current.find_next(string=True)

            description = " ".join(parts).strip()

        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "description": description,
            "url": url,
        }

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse une page liste et retourne les URLs detail trouvees."""
        return [{"url": link} for link in self.get_restaurant_links(soup)]

    def scrape_category(self, category: str, max_results: int = 20) -> List[Dict]:
        """Parcourt les pages d'une categorie et ouvre chaque fiche detail."""
        results = []
        page = 1
        seen_links = set()

        while len(results) < max_results:
            url = f"{self.base_url}/{category}?page={page}"
            soup = self.fetch_page(url)
            if not soup:
                break

            page_links = self.parse(soup)
            new_count = 0

            for item in page_links:
                detail_url = item["url"]

                if detail_url in seen_links:
                    continue

                seen_links.add(detail_url)
                new_count += 1

                detail_soup = self.fetch_page(detail_url)
                if not detail_soup:
                    continue

                business_data = self.parse_business_detail(detail_soup, detail_url)
                results.append(business_data)

                if len(results) >= max_results:
                    break

            if new_count == 0:
                break

            page += 1

        return results

    def scrape(self) -> List[Dict]:
        """Scrape par defaut la categorie restaurants."""
        return self.scrape_category("restaurants", max_results=20)
