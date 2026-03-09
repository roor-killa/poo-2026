# Import du module ABC pour créer des classes abstraites
from abc import ABC, abstractmethod

# Bibliothèque pour faire des requêtes HTTP
import requests

# Bibliothèque pour sauvegarder les données au format JSON
import json

# Bibliothèque pour sauvegarder les données au format CSV
import csv

# Type hints pour préciser les types de données
from typing import List, Dict

# Bibliothèque pour afficher des logs
import logging


# Configuration du système de logs
logging.basicConfig(level=logging.INFO)


class BaseScraper(ABC):
    """
    Classe abstraite représentant un scraper générique.

    Tous les scrapers du projet doivent hériter de cette classe.
    """

    def __init__(self, url: str, timeout: int = 10):
        """
        Constructeur du scraper.

        Args:
            url (str): URL du site à scraper
            timeout (int): délai maximum d'attente pour la requête
        """

        # URL du site à scraper
        self.url = url

        # Timeout de la requête HTTP
        self.timeout = timeout

        # Header HTTP pour simuler un navigateur
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Liste qui stockera les données scrapées
        self.data: List[Dict] = []

    def fetch_page(self):
        """
        Télécharge la page HTML du site.
        """

        try:
            # Envoi de la requête HTTP GET
            response = requests.get(
                self.url,
                headers=self.headers,
                timeout=self.timeout
            )

            # Vérifie si la réponse HTTP est correcte
            response.raise_for_status()

            # Retourne le contenu HTML de la page
            return response.text

        except requests.exceptions.RequestException as e:

            # Gestion des erreurs réseau
            logging.error(f"Erreur réseau : {e}")

            return None

    @abstractmethod
    def scrape(self):
        """
        Méthode principale de scraping.
        """
        pass

    @abstractmethod
    def parse(self, html: str):
        """
        Analyse le HTML pour extraire les données.
        """
        pass

    def save_to_json(self, filename: str):
        """
        Sauvegarde les données scrapées en JSON.
        """

        with open(filename, "w", encoding="utf-8") as file:

            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def save_to_csv(self, filename: str):
        """
        Sauvegarde les données scrapées en CSV.
        """

        # Vérifie qu'il y a des données
        if not self.data:
            logging.warning("Aucune donnée à sauvegarder")
            return

        # Récupère les clés du premier dictionnaire
        keys = self.data[0].keys()

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=keys)

            writer.writeheader()

            writer.writerows(self.data)