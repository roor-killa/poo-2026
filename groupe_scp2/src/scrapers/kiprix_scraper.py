"""
KiprixScraper — Scraper pour kiprix.com.

RESPONSABILITÉS :
- MEMBRE 1 : méthodes __init__, scrape(), parse() — navigation et extraction de base
- MEMBRE 2 : méthodes avancées get_products_by_category(), get_average_price_difference(),
             scrape_all_territories() — analyse et enrichissement des données
"""

import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

from ..base_scraper import BaseScraper


# ============================================================
# MEMBRE 1 — Navigation, pagination et extraction de base
# ============================================================

class KiprixScraper(BaseScraper):
    """
    Scraper pour kiprix.com — comparateur de prix entre la France et les DOM.

    kiprix.com permet de comparer les prix des produits alimentaires
    entre la France métropolitaine et les territoires d'outre-mer (Guadeloupe,
    Martinique, etc.).

    Attributes:
        territory (str): Code du territoire (ex: 'gp' pour Guadeloupe, 'mq' pour Martinique).

    Example:
        >>> scraper = KiprixScraper(territory='gp')
        >>> data = scraper.scrape(max_pages=5)
        >>> scraper.save_to_json('kiprix_gp.json')
    """

    # Territoires disponibles sur le site
    TERRITORIES = {
        'gp': 'Guadeloupe',
        'mq': 'Martinique',
        're': 'La Réunion',
        'gf': 'Guyane',
    }

    def __init__(self, territory: str = 'gp', delay: float = 1.5) -> None:
        """
        Initialise le scraper Kiprix pour un territoire donné.

        Args:
            territory: Code du territoire DOM (défaut: 'gp' pour Guadeloupe).
            delay: Délai entre les requêtes en secondes.

        Raises:
            ValueError: Si le code territoire n'est pas reconnu.
        """
        if territory not in self.TERRITORIES:
            raise ValueError(
                f"Territoire '{territory}' invalide. "
                f"Choisir parmi : {list(self.TERRITORIES.keys())}"
            )
        base_url = f"https://www.kiprix.com/fr-{territory}"
        super().__init__(base_url, delay)
        self.territory = territory

    def scrape(self, max_pages: int = 10) -> List[Dict]:
        """
        Scrape les pages de produits Kiprix avec gestion de la pagination.

        Parcourt les pages une par une jusqu'à max_pages ou jusqu'à
        ce qu'une page retourne 0 produits (fin du catalogue).

        Args:
            max_pages: Nombre maximum de pages à scraper.

        Returns:
            Liste de dictionnaires, un par produit trouvé.
        """
        self.data = []

        for page_num in range(1, max_pages + 1):
            # Construction de l'URL paginée
            if page_num == 1:
                url = f"{self.base_url}/produits"
            else:
                url = f"{self.base_url}/produits?page={page_num}"

            soup = self.fetch_page(url)
            if not soup:
                self.logger.warning(f"Page {page_num} inaccessible, arrêt.")
                break

            items = self.parse(soup)

            # Si la page est vide, on a atteint la fin du catalogue
            if not items:
                self.logger.info(f"Fin du catalogue à la page {page_num}.")
                break

            self.data.extend(items)
            self.logger.info(f"Page {page_num} : {len(items)} produits. Total : {len(self.data)}")

        return self.data

    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extrait les données produits depuis une page de résultats Kiprix.

        Sélecteurs identifiés sur le site (classes Tailwind CSS) :
        - Card produit : div.group.relative.bg-gray-100
        - Nom : h3 a
        - Prix France / DOM : p.text-gray-900 (1er et 2ème)
        - Écart % : span.text-red-600

        Args:
            soup: HTML de la page parsé par BeautifulSoup.

        Returns:
            Liste de dicts avec les clés : name, url, price_france,
            price_dom, difference, territory.
        """
        items = []

        cards = soup.select('div.group.relative.bg-gray-100')

        for card in cards:
            try:
                # Nom et URL du produit
                link_elem = card.select_one('h3 a')
                if not link_elem:
                    continue

                name = link_elem.get_text(strip=True)
                href = link_elem.get('href', '')
                url = f"https://www.kiprix.com{href}" if href.startswith('/') else href

                # Prix France et prix DOM
                prices = card.find_all('p', class_='text-gray-900')
                price_france = prices[0].get_text(strip=True) if len(prices) > 0 else ""
                price_dom = prices[1].get_text(strip=True) if len(prices) > 1 else ""

                # Écart en pourcentage (ex: "+ 45,81%")
                diff_elem = card.select_one('span.text-red-600')
                difference = diff_elem.get_text(strip=True) if diff_elem else ""

                items.append({
                    'name': name,
                    'url': url,
                    'price_france': price_france,
                    'price_dom': price_dom,
                    'difference': difference,
                    'territory': self.territory,
                    'territory_name': self.TERRITORIES[self.territory],
                })

            except Exception as e:
                self.logger.warning(f"Erreur parsing card : {e}")

        return items

    # ============================================================
    # MEMBRE 2 — Méthodes d'analyse avancée
    # ============================================================

    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Filtre les produits par catégorie.

        TODO MEMBRE 2 :
            - Parcourir self.data
            - Retourner les produits dont le champ 'category' correspond
            - La catégorie est à extraire depuis l'URL (ex: /epicerie-sucree/)
              ou le fil d'Ariane de la page produit

        Args:
            category: Catégorie à filtrer (ex: 'epicerie-sucree').

        Returns:
            Liste des produits correspondants.
        """
        # TODO : implémenter le filtrage par catégorie
        raise NotImplementedError("MEMBRE 2 : à implémenter")

    def get_average_price_difference(self) -> float:
        """
        Calcule l'écart de prix moyen (%) entre la France et le DOM.

        TODO MEMBRE 2 :
            - Parcourir self.data
            - Extraire le float de la colonne 'difference' (ex: "+ 45,81%" → 45.81)
            - Retourner la moyenne

        Returns:
            Moyenne des écarts en pourcentage (float).

        Example:
            >>> scraper.scrape(max_pages=3)
            >>> print(scraper.get_average_price_difference())
            42.5
        """
        # TODO : implémenter le calcul de la moyenne
        raise NotImplementedError("MEMBRE 2 : à implémenter")

    def scrape_all_territories(self, max_pages: int = 5) -> List[Dict]:
        """
        Scrape plusieurs territoires et fusionne les résultats.

        TODO MEMBRE 2 :
            - Boucler sur self.TERRITORIES
            - Pour chaque territoire, créer une instance KiprixScraper(territory=t)
            - Appeler scrape(max_pages)
            - Fusionner dans une liste globale

        Args:
            max_pages: Pages à scraper par territoire.

        Returns:
            Liste combinée de tous les produits de tous les territoires.
        """
        # TODO : implémenter le scraping multi-territoire
        raise NotImplementedError("MEMBRE 2 : à implémenter")
