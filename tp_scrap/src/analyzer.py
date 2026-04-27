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
            titre = row.get('titre', 'Film Inconnu').replace("'", "\\'")
            horaires = row.get('horaires', 'Non dispo')
            image = row.get('image', '')
            synopsis = row.get('synopsis', 'Pas de résumé.').replace("'", "\\'").replace("\n", " ")
            
            # Chaque carte appelle la fonction JS 'openModal' au clic
            cards_html += f"""
            <div class="glass-card" onclick="openModal('{titre}', '{synopsis}', '{image}', '{horaires}')">
                <div class="img-container">
                    <img src="{image}" class="movie-img">
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
                .glass-card {{ background: #222; border-radius: 10px; overflow: hidden; cursor: pointer; transition: 0.3s; border: 1px solid #333; }}
                .glass-card:hover {{ transform: scale(1.05); border-color: #E50914; }}
                .img-container {{ height: 350px; position: relative; }}
                .movie-img {{ width: 100%; height: 100%; object-fit: cover; }}
                .badge {{ position: absolute; top: 10px; right: 10px; background: #E50914; padding: 2px 8px; font-size: 0.7rem; border-radius: 4px; }}
                .card-content {{ padding: 15px; }}
                .time-badge {{ color: #ff4d4d; font-weight: bold; font-size: 0.8rem; margin-top: 10px; }}
                
                /* MODAL STYLE */
                #movieModal {{ display: none; position: fixed; z-index: 100; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); backdrop-filter: blur(5px); }}
                .modal-content {{ background: #181818; margin: 5% auto; padding: 0; width: 80%; max-width: 800px; border-radius: 15px; overflow: hidden; border: 1px solid #333; animation: slideIn 0.3s; }}
                @keyframes slideIn {{ from {{ transform: translateY(50px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
                .modal-header {{ position: relative; height: 300px; }}
                #modalImg {{ width: 100%; height: 100%; object-fit: cover; mask-image: linear-gradient(to bottom, black 60%, transparent 100%); }}
                .close {{ position: absolute; top: 20px; right: 20px; font-size: 30px; color: white; cursor: pointer; z-index: 10; }}
                .modal-body {{ padding: 30px; }}
                #modalTitle {{ font-size: 2.5rem; margin: 0 0 10px 0; }}
                #modalDesc {{ color: #ccc; line-height: 1.6; font-size: 1.1rem; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <a href="index.html" style="color: #aaa; text-decoration: none; margin-bottom: 20px; display: block;"><i class="fas fa-arrow-left"></i> Retour</a>
            <div class="grid">{cards_html}</div>

            <div id="movieModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <span class="close" onclick="closeModal()">&times;</span>
                        <img id="modalImg">
                    </div>
                    <div class="modal-body">
                        <h2 id="modalTitle"></h2>
                        <div id="modalTime" class="time-badge" style="margin-bottom: 20px; font-size: 1rem;"></div>
                        <p id="modalDesc"></p>
                    </div>
                </div>
            </div>

            <script>
                function openModal(title, desc, img, time) {{
                    document.getElementById('modalTitle').innerText = title;
                    document.getElementById('modalDesc').innerText = desc;
                    document.getElementById('modalImg').src = img;
                    document.getElementById('modalTime').innerHTML = '<i class="fas fa-clock"></i> ' + time;
                    document.getElementById('movieModal').style.display = "block";
                }}
                function closeModal() {{
                    document.getElementById('movieModal').style.display = "none";
                }}
                window.onclick = function(event) {{
                    if (event.target == document.getElementById('movieModal')) closeModal();
                }}
            </script>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f: f.write(full_html)