# scrapers/business_scraper.py

# Import de la classe de base (héritage POO)
from .base_scraper import BaseScraper

# Typage pour rendre le code plus lisible
from typing import List, Dict, Optional

# Regex pour nettoyer téléphone et extraire email
import re

# Parser HTML
from bs4 import BeautifulSoup


# Classe spécialisée pour scraper des entreprises
# Hérite de BaseScraper (POO)
class BusinessScraper(BaseScraper):

    # Constructeur
    def __init__(self):
        # Appel du constructeur parent
        # base_url = site racine
        # delay = 2 secondes entre requêtes (respect scraping éthique)
        super().__init__(base_url="https://www.bizouk.com", delay=2)

    # --------------------------------------------------
    # Nettoyage du téléphone
    # --------------------------------------------------
    def clean_phone(self, phone: str) -> str:
        """
        Nettoie un numéro de téléphone.
        Exemple :
        +596 696 12 34 56 → 0596 96 12 34
        """

        # Supprime tout sauf les chiffres
        digits = re.sub(r"\D", "", phone)

        # Si numéro avec indicatif international (596)
        if digits.startswith("596"):
            digits = digits[3:]  # enlève l'indicatif

        # Si numéro au bon format (DOM souvent 9 chiffres après indicatif)
        if len(digits) == 9:
            # Reformatte avec espaces
            return f"0596 {digits[1:3]} {digits[3:5]} {digits[5:7]}"

        # Sinon retourne brut mais nettoyé
        return phone.strip()

    # --------------------------------------------------
    # Extraction d'email avec regex
    # --------------------------------------------------
    def extract_email(self, text: str) -> Optional[str]:
        """
        Cherche une adresse email dans un bloc de texte.
        Retourne None si aucune trouvée.
        """

        # Regex classique pour email
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        # Si trouvé → retourne email
        # Sinon → None
        return match.group(0) if match else None

    # --------------------------------------------------
    # Parse UNE fiche entreprise
    # --------------------------------------------------
    def parse_business(self, business_soup: BeautifulSoup) -> Dict:
        """
        Extrait les infos d'une entreprise depuis une carte HTML.
        business_soup = bloc HTML représentant une entreprise
        """

        # -------------------
        # Nom
        # -------------------
        # Cherche un <h2>
        name = business_soup.select_one("h2").get_text(strip=True)

        # -------------------
        # Adresse
        # -------------------
        # Sélection par classe CSS
        address = business_soup.select_one(".address")

        # Si trouvé → texte
        # Sinon → None
        address = address.get_text(strip=True) if address else None

        # -------------------
        # Téléphone
        # -------------------
        phone_tag = business_soup.select_one(".phone")

        # Nettoyage avec fonction précédente
        phone = self.clean_phone(phone_tag.get_text()) if phone_tag else None

        # -------------------
        # Email
        # -------------------
        # On prend tout le texte de la carte
        text_blob = business_soup.get_text(" ")

        # Puis on cherche un email dedans
        email = self.extract_email(text_blob)

        # -------------------
        # Description
        # -------------------
        description = business_soup.select_one(".description")
        description = description.get_text(strip=True) if description else ""

        # -------------------
        # Retour structuré
        # -------------------
        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "description": description,
        }

    # --------------------------------------------------
    # Scraper une catégorie entière
    # --------------------------------------------------
    def scrape_category(self, category: str, max_results: int = 50) -> List[Dict]:
        """
        Scrape plusieurs pages d'une catégorie.
        
        Args:
            category: ex: restaurants, bars, événements
            max_results: limite pour éviter scraping infini
        """

        # Liste résultats finale
        results = []

        # Pagination (page 1, 2, 3…)
        page = 1

        # Boucle jusqu'à atteindre le nombre max
        while len(results) < max_results:

            # Construction URL avec pagination
            url = f"{self.base_url}/{category}?page={page}"

            # Récupère la page via BaseScraper
            soup = self.fetch_page(url)

            # Si erreur réseau → stop
            if not soup:
                break

            # Sélectionne toutes les cartes entreprise
            cards = soup.select(".business-card")

            # Parcours chaque carte
            for card in cards:

                # Parse la carte en dictionnaire
                results.append(self.parse_business(card))

                # Stop si limite atteinte
                if len(results) >= max_results:
                    break

            # Page suivante
            page += 1

        # Retourne toutes les entreprises scrapées
        return results