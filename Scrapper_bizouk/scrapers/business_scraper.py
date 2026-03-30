from .base_scraper import BaseScraper
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re


class BusinessScraper(BaseScraper):

    def __init__(self):
        # initialise le scraper avec lurl du site
        super().__init__(base_url="https://www.bizouk.com", delay=2)

    def clean_phone(self, phone: str) -> str:
        # garde uniquement les chiffres et le signe plus
        phone = phone.strip()
        digits = re.sub(r"[^\d+]", "", phone)
        return digits if digits else phone

    def extract_email(self, text: str) -> Optional[str]:
        # cherche une adresse email dans un texte
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        # cherche un téléphone dans le texte
        match = re.search(
            r"(\+596|\+590|0596|0590|0696|0690)[\s\-\.]?\d{2}[\s\-\.]?\d{2}[\s\-\.]?\d{2}[\s\-\.]?\d{2}",
            text
        )
        return self.clean_phone(match.group(0)) if match else None

    def get_restaurant_links(self, soup: BeautifulSoup) -> List[str]:
        # récupère les liens vers les fiches restaurants
        links = []
        seen = set()

        for a in soup.select("a[href]"):
            href = a.get("href", "").strip()

            # garde uniquement les liens détail restaurant
            if "/restaurants/details/" in href:
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
        # récupère le nom principal
        name = None
        title_tag = soup.select_one("h1")
        if title_tag:
            name = title_tag.get_text(strip=True)

        # récupère ladresse juste après le titre
        address = None
        if title_tag:
            current = title_tag.find_next(string=True)

            while current:
                text = current.strip()

                # garde une vraie ligne de texte utile
                if (
                    text
                    and text != name
                    and "voir le plan d'accès" not in text.lower()
                    and "contacter la boutique" not in text.lower()
                ):
                    # cherche une adresse avec code postal
                    if re.search(r"\b\d{5}\b", text):
                        address = text
                        break

                current = current.find_next(string=True)

        # récupère tout le texte de la page
        text_blob = soup.get_text(" ", strip=True)

        # cherche un email et un téléphone
        email = self.extract_email(text_blob)
        phone = self.extract_phone(text_blob)

        # récupère la description après le bloc description
        description = ""
        desc_title = soup.find(
            ["h2", "h3", "strong"],
            string=re.compile(r"description", re.IGNORECASE)
        )

        if desc_title:
            parts = []
            current = desc_title.find_next(string=True)

            while current:
                text = current.strip()

                # arrête la lecture si on entre dans une autre section
                if text.lower() in [
                    "partager cet évènement",
                    "copier ce lien",
                    "votre panier",
                    "vos articles",
                    "contacter la boutique" 
                    ""
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
            "url": url
        }

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        # parse la page liste et retourne les urls détail
        links = self.get_restaurant_links(soup)

        results = []
        for link in links:
            results.append({"url": link})

        return results

    def scrape_category(self, category: str, max_results: int = 20) -> List[Dict]:
        # récupère les fiches détail depuis la page liste
        results = []
        page = 1
        seen_links = set()

        while len(results) < max_results:
            # construit lurl de la page
            url = f"{self.base_url}/{category}?page={page}"

            # récupère la page
            soup = self.fetch_page(url)
            if not soup:
                break

            # récupère les urls trouvées sur la page
            page_links = self.parse(soup)

            # compte les nouveaux liens trouvés
            new_count = 0

            for item in page_links:
                detail_url = item["url"]

                if detail_url in seen_links:
                    continue

                seen_links.add(detail_url)
                new_count += 1

                # ouvre la fiche détail
                detail_soup = self.fetch_page(detail_url)
                if not detail_soup:
                    continue

                # parse la fiche détail
                business_data = self.parse_business_detail(detail_soup, detail_url)
                results.append(business_data)

                if len(results) >= max_results:
                    break

            # arrête la boucle si aucune nouvelle fiche na été trouvée
            if new_count == 0:
                break

            page += 1

        return results

    def scrape(self) -> List[Dict]:
        # scrape par défaut la catégorie restaurants
        return self.scrape_category("restaurants", max_results=20)