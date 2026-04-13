import pandas as pd
import os
from typing import List, Dict
import time 

class DataAnalyzer:
    """
    Classe responsable de l'analyse et de l'exportation des données scrapées.
    Utilise la bibliothèque Pandas pour la manipulation de données.
    """

    def __init__(self, raw_data: List[Dict]):
        # convertit la liste de dictionnaires en DataFrame Pandas (un tableau type Excel)
        self.df = pd.DataFrame(raw_data)

    def show_statistics(self):
        """Affiche des statistiques descriptives basiques."""
        if self.df.empty:
            print("⚠️ Aucune donnée à analyser.")
            return

        print("\n📊 STATISTIQUES DES DONNÉES :")
        print("-" * 30)
        print(f"Total d'éléments scrapés : {len(self.df)}")
        
        # compte combien d'éléments on a par source (RCI, Bizouk, etc.)
        if 'source' in self.df.columns:
            print("\nRépartition par site :")
            repartition = self.df['source'].value_counts()
            print(repartition.to_string())
        print("-" * 30)

    def export_to_csv(self, filename: str = "donnees_globales"):
        """Exporte les données nettoyées au format CSV."""
        if self.df.empty:
            return

        # assure que le dossier "processed" existe
        output_dir = os.path.join("data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f"{filename}.csv")
        
        # sauvegarde sans l'index de Pandas
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"📁 Données exportées avec succès dans : {filepath}")

        
    def export_to_html(self, file_name):
        """Génère une page web élégante avec les résultats."""
        # On s'assure que le dossier existe pour éviter les erreurs
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        # --- ASTUCE : On force l'ordre des colonnes pour le rendu ---
        # On définit l'ordre idéal
        ordre = ['titre', 'horaires', 'source']
        # On ne garde que celles qui existent vraiment dans le tableau
        colonnes_a_afficher = [c for c in ordre if c in self.df.columns]
        df_propre = self.df[colonnes_a_afficher]

        # Design CSS pour Chrome
        style = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f8f9fa; }
            h2 { color: #2c3e50; text-align: center; border-bottom: 2px solid #e67e22; padding-bottom: 10px; }
            table { border-collapse: collapse; width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            th { background-color: #e67e22; color: white; padding: 15px; text-align: left; text-transform: uppercase; font-size: 14px; }
            td { padding: 12px 15px; border-bottom: 1px solid #eee; color: #34495e; font-size: 14px; }
            tr:hover { background-color: #fff5eb; }
            .footer { margin-top: 20px; font-size: 12px; color: #7f8c8d; text-align: center; }
        </style>
        """
        
        # On utilise le tableau trié (df_propre) au lieu de self.df
        html_table = df_propre.to_html(index=False, border=0)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"<html><head><meta charset='utf-8'>{style}</head><body>")
            f.write(f"<h2>🎬 Cinéma Martinique - Résultats du Scraping</h2>")
            f.write(html_table)
            f.write(f"<div class='footer'>Généré automatiquement le {time.strftime('%d/%m/%Y')}</div>")
            f.write("</body></html>")
        
        print(f"🌐 [HTML] Page web créée avec succès : {path}")