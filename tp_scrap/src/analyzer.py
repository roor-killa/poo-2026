import pandas as pd
import os
from typing import List, Dict
import time 
import random # Pour les petits badges aléatoires

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
        
        if 'source' in self.df.columns:
            print("\nRépartition par site :")
            repartition = self.df['source'].value_counts()
            print(repartition.to_string())
        print("-" * 30)

    def export_to_csv(self, filename: str = "donnees_globales"):
        """Exporte les données nettoyées au format CSV."""
        if self.df.empty:
            return

        output_dir = os.path.join("data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, f"{filename}.csv")
        
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"📁 Données exportées avec succès dans : {filepath}")

    def export_to_html(self, file_name):
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        cards_html = ""
        for _, row in self.df.iterrows():
            titre = row.get('titre', 'Film').replace('"', '&quot;')
            horaires = row.get('horaires', 'Non dispo')
            image = row.get('image', '')
            synopsis = row.get('synopsis', '').replace('"', '&quot;')
            
            cards_html += f"""
            <div class="glass-card" onclick="openModal('{titre}', '{synopsis}', '{image}', '{horaires}')">
                <div class="img-container">
                    <img src="{image}" class="movie-img" onerror="this.src='https://placehold.co/400x600/222/white?text=Affiche+Indisponible'">
                    <span class="badge">INFO</span>
                </div>
                <div class="card-content">
                    <h3>{row.get('titre')}</h3>
                    <div class="time-badge"><i class="fas fa-clock"></i> {horaires}</div>
                </div>
            </div>
            """

        full_html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                body {{ background: #141414; color: white; font-family: 'Segoe UI', sans-serif; padding: 40px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 25px; }}
                .glass-card {{ background: #222; border-radius: 10px; overflow: hidden; cursor: pointer; transition: 0.3s; border: 1px solid #333; height: 100%; }}
                .glass-card:hover {{ transform: scale(1.05); border-color: #E50914; }}
                .img-container {{ height: 380px; position: relative; background: #111; }}
                .movie-img {{ width: 100%; height: 100%; object-fit: cover; }}
                .badge {{ position: absolute; top: 10px; right: 10px; background: #E50914; padding: 4px 10px; font-size: 0.7rem; border-radius: 4px; font-weight: bold; }}
                .card-content {{ padding: 15px; }}
                h3 {{ margin: 0; font-size: 1.1rem; min-height: 2.5em; }}
                .time-badge {{ color: #ff4d4d; font-weight: bold; font-size: 0.85rem; margin-top: 10px; display: flex; align-items: center; gap: 5px; }}
                
                #movieModal {{ display: none; position: fixed; z-index: 100; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); }}
                .modal-content {{ background: #181818; margin: 5% auto; width: 90%; max-width: 600px; border-radius: 15px; overflow: hidden; border: 1px solid #333; }}
                .modal-body {{ padding: 30px; }}
                #modalImg {{ width: 100%; height: 250px; object-fit: cover; border-bottom: 3px solid #E50914; }}
                .close-btn {{ float: right; font-size: 28px; cursor: pointer; color: #aaa; }}
                .close-btn:hover {{ color: white; }}
            </style>
        </head>
        <body>
            <a href="index.html" style="color: #666; text-decoration: none; margin-bottom: 30px; display: inline-block;"><i class="fas fa-arrow-left"></i> Retour à l'accueil</a>
            <div class="grid">{cards_html}</div>

            <div id="movieModal">
                <div class="modal-content">
                    <img id="modalImg">
                    <div class="modal-body">
                        <span class="close-btn" onclick="closeModal()">&times;</span>
                        <h2 id="modalTitle" style="margin-top:0"></h2>
                        <div id="modalTime" class="time-badge" style="margin-bottom: 20px;"></div>
                        <p id="modalDesc" style="line-height:1.6; color: #ccc;"></p>
                    </div>
                </div>
            </div>

            <script>
                function openModal(t, d, i, h) {{
                    document.getElementById('modalTitle').innerText = t;
                    document.getElementById('modalDesc').innerText = d;
                    document.getElementById('modalImg').src = i;
                    document.getElementById('modalTime').innerHTML = '<i class="fas fa-clock"></i> ' + h;
                    document.getElementById('movieModal').style.display = "block";
                }}
                function closeModal() {{ document.getElementById('movieModal').style.display = "none"; }}
                window.onclick = function(e) {{ if(e.target == document.getElementById('movieModal')) closeModal(); }}
            </script>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f: f.write(full_html)