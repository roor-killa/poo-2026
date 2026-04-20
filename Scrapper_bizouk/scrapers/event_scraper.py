from typing import Dict, List, Optional
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup, Tag

from .base_scraper import BaseScraper


class EventScraper(BaseScraper):
    """
    Scraper principal du projet.

    Il travaille en deux temps:
    1. lire les cartes visibles sur les pages de liste Bizouk;
    2. ouvrir chaque fiche detail pour recuperer les infos absentes des cartes, surtout les prix.
    """

    def __init__(self, region: str = "martinique"):
        """Prepare la region cible et initialise la session HTTP heritee de BaseScraper."""
        self.region = region.strip().lower() or "martinique"
        super().__init__(base_url="https://www.bizouk.com", delay=0.35, timeout=25.0)

    def _absolute_url(self, href: Optional[str]) -> Optional[str]:
        """Transforme un lien relatif Bizouk en URL complete."""
        if not href:
            return None
        return urljoin(self.base_url, href.strip())

    def _clean_text(self, value: Optional[str]) -> Optional[str]:
        """Nettoie les espaces multiples pour obtenir un texte lisible dans le JSON."""
        if not value:
            return None
        text = re.sub(r"\s+", " ", value).strip()
        return text or None

    def _money_to_float(self, value: Optional[str]) -> Optional[float]:
        """Convertit un texte de prix comme '5,50 EUR' en nombre float."""
        if not value:
            return None
        match = re.search(r"(\d+(?:[,.]\d+)?)", value)
        if not match:
            return None
        return float(match.group(1).replace(",", "."))

    def _list_urls(self, page: int) -> List[str]:
        """Construit les URLs de liste a visiter selon la page demandee."""
        if page <= 1:
            return [
                f"{self.base_url}/?region={self.region}",
            ]

        return [
            f"{self.base_url}/?region={self.region}&page={page}",
        ]

    def _extract_image(self, card: Tag) -> Optional[str]:
        """Recupere l'image principale d'une carte evenement."""
        image = card.select_one("img[src]")
        if not image:
            return None
        return self._absolute_url(image.get("src"))

    def _parse_home_card(self, card: Tag) -> Dict:
        """Parse une carte evenement presente sur la page d'accueil Bizouk."""
        # La carte contient deja les infos de base: titre, lieu, date, image et lien detail.
        link = card.select_one("a[href*='/events/details/']")
        title = self._clean_text(
            card.select_one(".bzk-event-title").get_text(" ", strip=True)
            if card.select_one(".bzk-event-title")
            else card.get("data-title")
        )
        location = self._clean_text(
            card.select_one(".bzk-event-location").get_text(" ", strip=True)
            if card.select_one(".bzk-event-location")
            else card.get("data-location")
        )
        date = self._clean_text(
            card.select_one(".bzk-event-date").get_text(" ", strip=True)
            if card.select_one(".bzk-event-date")
            else card.get("data-date")
        )

        return {
            "title": title,
            "event_type": self._clean_text(card.get("data-type")),
            "location": location,
            "date": date,
            "date_iso": self._clean_text(card.get("data-dates-iso")),
            "image_url": self._extract_image(card),
            "detail_url": self._absolute_url(link.get("href") if link else None),
            "badge": self._clean_text(
                card.select_one(".bzk-badge-premium").get_text(" ", strip=True)
                if card.select_one(".bzk-badge-premium")
                else None
            ),
        }

    def _parse_agenda_card(self, card: Tag) -> Dict:
        """Parse une carte evenement issue du format agenda de Bizouk."""
        # Bizouk utilise parfois un second format HTML pour les evenements de type agenda.
        date_tag = card.select_one(".ag-event-bottom span")
        time_tag = card.select_one(".ag-event-time")
        title_tag = card.select_one(".ag-event-title")
        location_tag = card.select_one(".ag-event-location")
        type_tag = card.select_one(".ag-event-type-badge")

        return {
            "title": self._clean_text(
                title_tag.get_text(" ", strip=True) if title_tag else card.get("data-title")
            ),
            "event_type": self._clean_text(
                type_tag.get_text(" ", strip=True) if type_tag else card.get("data-type")
            ),
            "location": self._clean_text(
                location_tag.get_text(" ", strip=True) if location_tag else card.get("data-location")
            ),
            "date": self._clean_text(date_tag.get_text(" ", strip=True) if date_tag else None),
            "time": self._clean_text(time_tag.get_text(" ", strip=True) if time_tag else None),
            "image_url": self._extract_image(card),
            "detail_url": self._absolute_url(card.get("href")),
        }

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """Recupere les evenements visibles sur une page liste."""
        results: List[Dict] = []

        # Premier format de carte observe sur la page d'accueil.
        for card in soup.select(".bzk-event-card"):
            item = self._parse_home_card(card)
            if item.get("detail_url"):
                results.append(item)

        # Deuxieme format observe dans certaines pages agenda.
        for card in soup.select("a.ag-event[href*='/events/details/']"):
            item = self._parse_agenda_card(card)
            if item.get("detail_url"):
                results.append(item)

        return results

    def _extract_hero_meta(self, soup: BeautifulSoup) -> Dict:
        """Lit les informations principales de la fiche detail: date, lieu et plan."""
        meta = {"date": None, "location": None, "address": None}
        items = soup.select(".evh-hero-meta-item")

        # Les metadonnees sont reperees grace aux icones: calendrier pour la date, marker pour le lieu.
        for item in items:
            text = self._clean_text(item.get_text(" ", strip=True))
            if not text:
                continue
            icon = item.select_one("i")
            icon_class = " ".join(icon.get("class", [])) if icon else ""

            if "calendar" in icon_class and not meta["date"]:
                meta["date"] = text
            elif "map-marker" in icon_class and not meta["location"]:
                strong = item.select_one("strong")
                span = item.select_one("span")
                location = self._clean_text(strong.get_text(" ", strip=True)) if strong else text
                city = self._clean_text(span.get_text(" ", strip=True).lstrip("· ")) if span else None
                meta["location"] = " - ".join(part for part in [location, city] if part)

        map_link = soup.select_one(".evh-hero-map-link[href]")
        if map_link:
            meta["map_url"] = self._absolute_url(map_link.get("href"))

        return meta

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la description longue de la fiche evenement."""
        # Sur les fiches recentes, Bizouk place souvent la description dans #party_description.
        description = soup.select_one("#party_description")
        if description:
            return self._clean_text(description.get_text(" ", strip=True))

        # Fallback: si l'id change, on cherche un titre "description" puis on lit le texte qui suit.
        heading = soup.find(
            ["h2", "h3", "strong"],
            string=re.compile(r"description", re.IGNORECASE),
        )
        if not heading:
            return None

        parts = []
        current = heading.find_next(string=True)
        while current:
            text = current.strip()
            if text.lower() in {"share this event:", "partager cet evenement:", "contact"}:
                break
            if text:
                parts.append(text)
            current = current.find_next(string=True)
        return self._clean_text(" ".join(parts))

    def _extract_price_items(self, soup: BeautifulSoup) -> List[Dict]:
        """Recupere les billets disponibles avec prix, frais et total."""
        items: List[Dict] = []
        seen = set()

        # Les inputs de quantite contiennent les attributs price, fee et data-max.
        for quantity in soup.select("input.selectQuantity[price]"):
            product_id = quantity.get("product") or quantity.get("id")
            if product_id in seen:
                continue
            seen.add(product_id)

            container = quantity.find_parent(class_="panel-body") or quantity.find_parent("div")
            label_tag = container.find("span") if container else None
            label = self._clean_text(label_tag.get_text(" ", strip=True) if label_tag else None)

            price = self._money_to_float(quantity.get("price"))
            fee = self._money_to_float(quantity.get("fee")) or 0.0
            max_quantity = quantity.get("data-max")

            items.append(
                {
                    "label": label,
                    "price": price,
                    "fee": fee,
                    "total_with_fee": round(price + fee, 2) if price is not None else None,
                    "currency": "EUR",
                    "max_quantity": int(max_quantity) if max_quantity and max_quantity.isdigit() else None,
                }
            )

        return items

    def parse_detail(self, soup: BeautifulSoup, url: str, base_item: Optional[Dict] = None) -> Dict:
        """Fusionne les donnees de la carte avec les donnees completes de la fiche detail."""
        base_item = base_item or {}

        # Les selecteurs .evh-* correspondent au bloc hero de la page detail Bizouk.
        title_tag = soup.select_one(".evh-hero-title") or soup.select_one("h1")
        subtitle_tag = soup.select_one(".evh-hero-subtitle")
        type_tag = soup.select_one(".evh-hero-eyebrow")
        image_tag = soup.select_one("#flyer1[src]") or soup.select_one(".evh-hero img[src]")
        hero = self._extract_hero_meta(soup)

        price_items = self._extract_price_items(soup)

        # min_total_price sert dans le frontend pour afficher un prix de depart sur la carte.
        min_price = min(
            (item["total_with_fee"] for item in price_items if item.get("total_with_fee") is not None),
            default=None,
        )

        return {
            **base_item,
            "title": self._clean_text(title_tag.get_text(" ", strip=True)) or base_item.get("title"),
            "subtitle": self._clean_text(subtitle_tag.get_text(" ", strip=True)) if subtitle_tag else None,
            "event_type": (
                self._clean_text(type_tag.get_text(" ", strip=True)) if type_tag else None
            )
            or base_item.get("event_type"),
            "location": hero.get("location") or base_item.get("location"),
            "date": hero.get("date") or base_item.get("date"),
            "map_url": hero.get("map_url"),
            "description": self._extract_description(soup),
            "price_items": price_items,
            "min_total_price": min_price,
            "image_url": self._absolute_url(image_tag.get("src")) if image_tag else base_item.get("image_url"),
            "detail_url": url,
        }

    def scrape(
        self,
        max_pages: int = 1,
        include_details: bool = True,
        max_events: Optional[int] = None,
    ) -> List[Dict]:
        """Parcourt les pages Bizouk, dedoublonne les URLs et retourne les evenements."""
        max_pages = max(1, min(int(max_pages), 10))
        max_events = max(1, int(max_events)) if max_events else None
        results: List[Dict] = []
        seen_urls = set()

        # Boucle principale: page 1, page 2, etc. avec une limite de securite a 10 pages.
        for page in range(1, max_pages + 1):
            page_new_count = 0

            for url in self._list_urls(page):
                soup = self.fetch_page(url)
                if not soup:
                    continue

                for item in self.parse(soup):
                    detail_url = item.get("detail_url")

                    # On evite les doublons, car un meme evenement peut apparaitre dans plusieurs blocs.
                    if not detail_url or detail_url in seen_urls:
                        continue

                    seen_urls.add(detail_url)
                    page_new_count += 1

                    if include_details:
                        # Ouverture de la fiche detail pour enrichir les donnees de la carte.
                        detail_soup = self.fetch_page(detail_url)
                        if detail_soup:
                            item = self.parse_detail(detail_soup, detail_url, item)

                    results.append(item)

                    if max_events and len(results) >= max_events:
                        return results

            if page_new_count == 0:
                # Si une page ne donne aucun nouvel evenement, inutile de continuer la pagination.
                break

        return results
