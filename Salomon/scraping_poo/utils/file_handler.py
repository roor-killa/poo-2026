import json
import csv
from pathlib import Path
from typing import List, Dict
import pandas as pd


class FileHandler:
    """Gestion de l'export des données scrapées"""

    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_filepath(self, filename: str) -> Path:
        """Construit le chemin complet du fichier"""
        return self.output_dir / filename

    def save_json(self, data: List[Dict], filename: str):
        """Sauvegarde en JSON avec indentation"""
        filepath = self._get_filepath(filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"JSON sauvegardé : {filepath}")

    def save_csv(self, data: List[Dict], filename: str):
        """Sauvegarde en CSV"""
        if not data:
            raise ValueError("Aucune donnée à sauvegarder")

        filepath = self._get_filepath(filename)

        keys = data[0].keys()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"CSV sauvegardé : {filepath}")

    def load_json(self, filename: str) -> List[Dict]:
        """Charge des données JSON"""
        filepath = self._get_filepath(filename)

        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} introuvable")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def create_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """Crée un DataFrame pandas pour analyse"""
        if not data:
            raise ValueError("Impossible de créer un DataFrame vide")

        df = pd.DataFrame(data)
        return df

    def export_excel(self, data: List[Dict], filename: str):
        """
        Exporte vers Excel.
        Si plusieurs types de données sont détectés,
        crée plusieurs feuilles automatiquement.
        """
        filepath = self._get_filepath(filename)

        df = self.create_dataframe(data)

        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            # Cas simple : une seule feuille
            if "category" not in df.columns:
                df.to_excel(writer, sheet_name="Data", index=False)
            else:
                # Une feuille par catégorie
                for category, subset in df.groupby("category"):
                    sheet_name = str(category)[:31]  # limite Excel
                    subset.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )

        print(f"Excel exporté : {filepath}")