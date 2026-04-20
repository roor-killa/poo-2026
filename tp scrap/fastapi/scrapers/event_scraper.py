from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import Any, Optional
from urllib.parse import urljoin
import json
import re


class BizoukEventScraper(BaseScraper):
    DEFAULT_REGIONS = ["martinique"]

    def __init__(self, delay: float = 2.0):
        super().__init__(base_url="https://www.bizouk.com", delay=delay)

    def clean_text(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        text = re.sub(r"\s+", " ", value).strip()
        return text or None

    def source_id_from_url(self, url: str) -> Optional[str]:
        match = re.search(r"/(\d+)(?:[/?#].*)?$", url)
        return match.group(1) if match else None

    def first_image(self, image: Any) -> Optional[str]:
        if isinstance(image, list) and image:
            return image[0]
        if isinstance(image, str):
            return image
        return None

    def parse_price(self, value: Any) -> Optional[float]:
        if value in (None, ""):
            return None
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return None

    def normalize_type(self, value: Optional[str]) -> Optional[str]:
        value = self.clean_text(value)
        if not value:
            return None
        value = value.lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-") or None

    def parse_listing_card(self, card: BeautifulSoup, region: str) -> Optional[dict]:
        link = card.find("a", href=re.compile(r"/events/details/"))
        if not link:
            return None

        source_url = urljoin(self.base_url, link.get("href", ""))
        image = card.find("img")
        image_url = image.get("src") or image.get("data-src") if image else None
        image_alt = image.get("alt") if image else None

        title_tag = card.select_one(".bzk-event-title")
        location_tag = card.select_one(".bzk-event-location")
        date_tag = card.select_one(".bzk-event-date")

        title = (
            image_alt
            or card.get("data-title")
            or (title_tag.get_text(" ", strip=True) if title_tag else None)
        )

        return {
            "source_id": self.source_id_from_url(source_url),
            "source_url": source_url,
            "title": self.clean_text(title) or "Evenement Bizouk",
            "event_type": self.normalize_type(card.get("data-type")),
            "region": region,
            "venue": self.clean_text(card.get("data-location") or (location_tag.get_text(" ", strip=True) if location_tag else None)),
            "start_date": self.clean_text(card.get("data-dates-iso")),
            "date_text": self.clean_text(card.get("data-date") or (date_tag.get_text(" ", strip=True) if date_tag else None)),
            "image_url": image_url,
        }

    def parse(self, soup: BeautifulSoup) -> list[dict]:
        cards = soup.select(".bzk-event-card")
        return [item for item in (self.parse_listing_card(card, "martinique") for card in cards) if item]

    def extract_json_ld(self, soup: BeautifulSoup) -> Optional[dict]:
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = script.string or script.get_text()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            candidates = data if isinstance(data, list) else [data]
            for item in candidates:
                if isinstance(item, dict) and item.get("@type") == "Event":
                    return item
        return None

    def parse_offers(self, event_data: dict) -> tuple[list[dict], Optional[float], Optional[str]]:
        raw_offers = event_data.get("offers") or []
        offers = raw_offers if isinstance(raw_offers, list) else [raw_offers]
        clean_offers = []
        prices = []
        currency = None

        for offer in offers:
            if not isinstance(offer, dict):
                continue
            price = self.parse_price(offer.get("price"))
            if price is not None:
                prices.append(price)
            currency = currency or offer.get("priceCurrency")
            clean_offers.append({
                "name": offer.get("name"),
                "price": price,
                "currency": offer.get("priceCurrency"),
                "availability": offer.get("availability"),
            })

        return clean_offers, min(prices) if prices else None, currency

    def parse_address(self, location: dict) -> tuple[Optional[str], Optional[str], Optional[str]]:
        if not isinstance(location, dict):
            return None, None, None

        address = location.get("address")
        if isinstance(address, str):
            return self.clean_text(address), None, None
        if not isinstance(address, dict):
            return None, None, None

        street = self.clean_text(address.get("streetAddress"))
        postal = self.clean_text(address.get("postalCode"))
        city = self.clean_text(address.get("addressLocality"))
        country = self.clean_text(address.get("addressCountry"))
        full_address = ", ".join(part for part in [street, postal, city] if part)
        return self.clean_text(full_address), city, country

    def extract_contact(self, soup: BeautifulSoup) -> dict:
        text = soup.get_text("\n", strip=True)
        email_match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)
        phone_match = re.search(r"(?:\+?596\s*)?0[56]\d(?:[\s.-]?\d{2}){3}", text)

        ignored_domains = ("bizouk.com", "twitter.com", "facebook.com", "plus.google.com", "send")
        website = None
        for link in soup.find_all("a", href=True):
            href = link["href"].strip()
            if not href.startswith(("http://", "https://")):
                continue
            if any(domain in href for domain in ignored_domains):
                continue
            website = href
            break

        return {
            "contact_email": email_match.group(0) if email_match else None,
            "contact_phone": phone_match.group(0) if phone_match else None,
            "website": website,
        }

    def parse_detail(self, soup: BeautifulSoup, fallback: dict) -> dict:
        event_data = self.extract_json_ld(soup) or {}
        location = event_data.get("location") if isinstance(event_data, dict) else {}
        organizer = event_data.get("organizer") if isinstance(event_data.get("organizer"), dict) else {}
        offers, min_price, currency = self.parse_offers(event_data)
        address, city, country = self.parse_address(location)

        hero_type = soup.select_one(".evh-hero-eyebrow")
        contact = self.extract_contact(soup)

        detail = {
            **fallback,
            "title": self.clean_text(event_data.get("name")) or fallback.get("title"),
            "description": self.clean_text(event_data.get("description")) or fallback.get("description"),
            "start_date": event_data.get("startDate") or fallback.get("start_date"),
            "end_date": event_data.get("endDate") or fallback.get("end_date"),
            "source_url": event_data.get("url") or fallback.get("source_url"),
            "image_url": self.first_image(event_data.get("image")) or fallback.get("image_url"),
            "venue": self.clean_text(location.get("name")) if isinstance(location, dict) else fallback.get("venue"),
            "address": address,
            "city": city,
            "country": country,
            "organizer": self.clean_text(organizer.get("name")) if organizer else None,
            "event_type": fallback.get("event_type") or self.normalize_type(hero_type.get_text(" ", strip=True) if hero_type else None),
            "offers": offers,
            "min_price": min_price,
            "currency": currency,
            **contact,
        }
        detail["source_id"] = fallback.get("source_id") or self.source_id_from_url(detail["source_url"])
        return detail

    def scrape_region(self, region: str, max_results: int = 30, fetch_details: bool = True) -> list[dict]:
        url = f"{self.base_url}/?region={region}"
        print(f"[Scraping] {url}")
        soup = self.fetch_page(url)
        if not soup:
            return []

        cards = soup.select(".bzk-event-card")
        listing_items = []
        for card in cards:
            item = self.parse_listing_card(card, region)
            if item:
                listing_items.append(item)
            if len(listing_items) >= max_results:
                break

        if not fetch_details:
            return listing_items

        results = []
        seen_urls = set()
        for item in listing_items:
            if item["source_url"] in seen_urls:
                continue
            seen_urls.add(item["source_url"])

            detail_soup = self.fetch_page(item["source_url"])
            if not detail_soup:
                results.append(item)
                continue
            results.append(self.parse_detail(detail_soup, item))

        return results

    def scrape(
        self,
        regions: Optional[list[str]] = None,
        max_per_region: int = 30,
        fetch_details: bool = True,
    ) -> list[dict]:
        regions = regions or self.DEFAULT_REGIONS
        all_results = []

        for region in regions:
            region = self.normalize_type(region) or "martinique"
            print(f"\n=== Region : {region} ===")
            results = self.scrape_region(
                region=region,
                max_results=max_per_region,
                fetch_details=fetch_details,
            )
            all_results.extend(results)
            print(f"[OK] {len(results)} evenements recuperes pour '{region}'")

        return all_results
