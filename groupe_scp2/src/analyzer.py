"""
DataAnalyzer — Analyse statistique des données Kiprix.

MEMBRE 2 : Ce fichier est entièrement sous ta responsabilité.
"""

import re
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

import pandas as pd


class DataAnalyzer:
    """
    Analyse les données scrapées depuis kiprix.com avec pandas.

    Fournit des statistiques descriptives, des analyses de tendances
    de prix et des exports multi-formats.

    Attributes:
        df (pd.DataFrame): DataFrame contenant les données chargées.

    Example:
        >>> analyzer = DataAnalyzer()
        >>> analyzer.load_from_json('data/raw/kiprix_gp.json')
        >>> stats = analyzer.descriptive_stats()
        >>> analyzer.export_to_excel('rapport_kiprix.xlsx')
    """

    def __init__(self) -> None:
        self.df: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_from_json(self, filepath: str) -> None:
        """
        Charge un fichier JSON dans le DataFrame.

        Args:
            filepath: Chemin vers le fichier JSON (ex: 'data/raw/kiprix_gp.json').

        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {filepath}")
        self.df = pd.read_json(filepath)
        self.logger.info(f"Chargé {len(self.df)} entrées depuis {filepath}")

    def descriptive_stats(self) -> Dict[str, Any]:
        """
        Retourne des statistiques descriptives sur les données chargées.

        Returns:
            Dictionnaire avec : total, colonnes, valeurs_manquantes,
            valeurs_uniques par colonne.

        TODO MEMBRE 2 :
            Enrichir avec des stats supplémentaires si pertinent.
        """
        if self.df is None or self.df.empty:
            return {"erreur": "Aucune donnée chargée."}

        return {
            'total': len(self.df),
            'colonnes': list(self.df.columns),
            'valeurs_manquantes': self.df.isnull().sum().to_dict(),
            'valeurs_uniques': {
                col: self.df[col].nunique()
                for col in self.df.columns
                if self.df[col].dtype == object
            }
        }

    def detect_price_trends(self) -> Dict[str, Any]:
        """
        Analyse les écarts de prix entre France et DOM.

        Nettoie la colonne 'difference' (ex: "+ 45,81%" → 45.81)
        et calcule des statistiques par territoire.

        Returns:
            Dict avec moyenne, max, min, médiane des écarts.

        TODO MEMBRE 2 — Compléter cette méthode :
            1. Nettoyer la colonne 'difference' avec regex
               ex: re.search(r'(\\d+[,\\d]*)', val) -> float
            2. Calculer moyenne, max, min, médiane
            3. (Optionnel) Grouper par territoire si plusieurs territoires

        Example:
            >>> trends = analyzer.detect_price_trends()
            >>> print(trends['moyenne'])  # ex: 42.5
        """
        # TODO MEMBRE 2 : implémenter l'analyse des tendances de prix
        raise NotImplementedError("MEMBRE 2 : à implémenter")

    def export_to_excel(self, filename: str) -> None:
        """
        Exporte le DataFrame vers un fichier Excel dans data/processed/.

        Args:
            filename: Nom du fichier (ex: 'rapport_kiprix.xlsx').

        TODO MEMBRE 2 :
            Optionnellement : ajouter des styles (couleurs, gras) avec openpyxl.
        """
        if self.df is None:
            self.logger.error("Aucune donnée à exporter.")
            return
        path = Path("data/processed") / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_excel(path, index=False)
        self.logger.info(f"Exporté Excel : {path}")

    def export_to_csv(self, filename: str) -> None:
        """
        Exporte le DataFrame vers un fichier CSV dans data/processed/.

        Args:
            filename: Nom du fichier (ex: 'rapport_kiprix.csv').
        """
        if self.df is None:
            self.logger.error("Aucune donnée à exporter.")
            return
        path = Path("data/processed") / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=False, encoding='utf-8')
        self.logger.info(f"Exporté CSV : {path}")

    def get_summary_report(self) -> str:
        """
        Génère un rapport texte lisible sur les données.

        TODO MEMBRE 2 — Enrichir ce rapport avec :
            - Le résultat de detect_price_trends()
            - Les top 5 produits les plus chers en DOM
            - La répartition par territoire

        Returns:
            Rapport formaté en chaîne de caractères.
        """
        stats = self.descriptive_stats()
        lines = [
            "=" * 40,
            "  RAPPORT DONNÉES KIPRIX",
            "=" * 40,
            f"Total produits    : {stats.get('total', 0)}",
            f"Colonnes          : {stats.get('colonnes', [])}",
            "",
            "Valeurs manquantes :",
        ]
        for col, count in stats.get('valeurs_manquantes', {}).items():
            lines.append(f"  {col:<20} {count}")
        lines.append("=" * 40)
        return "\n".join(lines)
