import pandas as pd
import os
from typing import List, Dict
import time 

class DataAnalyzer:
    def __init__(self, raw_data: List[Dict]):
        # convertit la liste de dictionnaires en DataFrame Pandas
        self.df = pd.DataFrame(raw_data)

    def show_statistics(self):
        """Affiche des statistiques descriptives basiques."""
        if self.df.empty:
            print("⚠️ Aucune donnée à analyser.")
            return

        print(f"\n📊 Analyse terminée : {len(self.df)} films prêts pour l'affichage.")

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
        """Génère une galerie de films look Netflix avec boutons Bandes-Annonces."""
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        cards_html = ""
        for _, row in self.df.iterrows():
            image = row.get('image')
            titre = row.get('titre', 'Film')
            horaires = row.get('horaires', 'Séances non dispo')
            ba_url = row.get('ba', '#') # On récupère le lien de la bande-annonce
            
            # Gestion de l'image par défaut
            if not image:
                image = "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=400&h=600&auto=format&fit=crop"

            # --- LOGIQUE DU BOUTON BANDE-ANNONCE ---
            # On n'affiche le bouton que si le lien n'est pas vide ou égal à "#"
            ba_button = ""
            if ba_url and ba_url != "#":
                ba_button = f"""
                <a href="{ba_url}" target="_blank" class="ba-btn">
                    <i class="fas fa-play"></i> Bande-annonce
                </a>
                """

            cards_html += f"""
            <div class="glass-card">
                <div class="img-container">
                    <img src="{image}" class="movie-img" alt="{titre}">
                    <div class="overlay"></div>
                </div>
                <div class="card-content">
                    <h3>{titre}</h3>
                    <div class="time-container">
                        <i class="fas fa-clock"></i>
                        <span>{horaires}</span>
                    </div>
                    {ba_button}
                </div>
            </div>
            """

        full_html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                :root {{
                    --netflix-red: #E50914;
                    --bg-dark: #141414;
                    --card-bg: rgba(45, 45, 45, 0.6);
                }}
                
                body {{
                    background-color: var(--bg-dark);
                    color: white;
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    margin: 0;
                    padding: 40px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}

                .container {{ max-width: 1200px; width: 100%; }}

                .header {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 40px;
                    gap: 15px;
                }}

                .back-btn {{
                    text-decoration: none;
                    color: #fff;
                    background: rgba(255,255,255,0.1);
                    padding: 10px 15px;
                    border-radius: 50%;
                    transition: 0.3s;
                }}
                .back-btn:hover {{ background: var(--netflix-red); }}

                h1 {{ font-size: 2.5rem; margin: 0; }}
                h1 span {{ color: var(--netflix-red); }}

                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
                    gap: 30px;
                }}

                .glass-card {{
                    background: var(--card-bg);
                    backdrop-filter: blur(10px);
                    border-radius: 12px;
                    overflow: hidden;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
                    display: flex;
                    flex-direction: column;
                }}

                .glass-card:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 15px 35px rgba(0,0,0,0.5);
                    border-color: var(--netflix-red);
                }}

                .img-container {{
                    position: relative;
                    height: 380px;
                    overflow: hidden;
                }}

                .movie-img {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }}

                .overlay {{
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    height: 50%;
                    background: linear-gradient(to top, rgba(20,20,20,0.9), transparent);
                }}

                .card-content {{ 
                    padding: 20px; 
                    display: flex; 
                    flex-direction: column; 
                    flex-grow: 1;
                }}

                h3 {{
                    margin: 0 0 15px 0;
                    font-size: 1.2rem;
                    letter-spacing: 0.5px;
                    min-height: 2.4em;
                    display: flex;
                    align-items: center;
                }}

                .time-container {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: #ff4d4d;
                    font-weight: bold;
                    font-size: 0.85rem;
                    background: rgba(229, 9, 20, 0.1);
                    padding: 8px 12px;
                    border-radius: 6px;
                    width: fit-content;
                }}

                /* BOUTON BANDE-ANNONCE */
                .ba-btn {{
                    margin-top: auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    background: white;
                    color: black;
                    text-decoration: none;
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 0.85rem;
                    transition: 0.3s;
                    margin-top: 20px;
                }}

                .ba-btn:hover {{
                    background: var(--netflix-red);
                    color: white;
                }}

                .footer {{
                    margin-top: 60px;
                    color: #555;
                    font-size: 0.8rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <a href="index.html" class="back-btn"><i class="fas fa-arrow-left"></i></a>
                    <h1>Séances <span>Madiana</span></h1>
                </div>

                <div class="grid">
                    {cards_html}
                </div>

                <div class="footer">
                    Généré par CineScrap Martinique • {time.strftime('%H:%M')}
                </div>
            </div>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"🌐 [Interface Netflix] Galerie avec bandes-annonces prête : {path}")