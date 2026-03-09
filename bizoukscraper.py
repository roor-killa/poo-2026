# Import de BeautifulSoup pour parser le HTML
from bs4 import BeautifulSoup

# Import de la classe abstraite
from src.base_scraper import BaseScraper


class BizoukScraper(BaseScraper):
    """
    Scraper pour récupérer les annonces sur Bizouk.
    """

    def __init__(self):

        # Appel du constructeur de BaseScraper
        super().__init__("https://bizouk.com")

    def scrape(self):
        """
        Lance le processus de scraping.
        """

        # Récupération du HTML
        html = self.fetch_page()

        # Vérifie si la page a été récupérée
        if html:

            # Analyse du HTML
            self.parse(html)

    def parse(self, html: str):
        """
        Analyse le HTML pour extraire les annonces.
        """

        # Création de l'objet BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Recherche de toutes les annonces
        annonces = soup.find_all("div", class_="annonce")

        # Parcours de chaque annonce
        for annonce in annonces:

            # Recherche du titre
            titre = annonce.find("h2")

            # Recherche du prix
            prix = annonce.find("span", class_="price")

            # Recherche de la catégorie
            categorie = annonce.find("span", class_="category")

            # Recherche de la localisation
            localisation = annonce.find("span", class_="location")

            # Recherche de la date
            date = annonce.find("span", class_="date")

            # Ajout des données dans la liste
            self.data.append({

                "titre": titre.text.strip() if titre else None,

                "prix": prix.text.strip() if prix else None,

                "categorie": categorie.text.strip() if categorie else None,

                "localisation": localisation.text.strip() if localisation else None,

                "date": date.text.strip() if date else None

            })