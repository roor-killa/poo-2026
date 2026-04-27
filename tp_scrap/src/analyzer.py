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
        """Génère une galerie de films sombre et élégante (Look Netflix)."""
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        # 1. On prépare les "Cartes" de films en HTML
        cards_html = ""
        for _, row in self.df.iterrows():
            titre = row.get('titre', 'Film Inconnu')
            horaires = row.get('horaires', 'Séances non disponibles')
            image_url = row.get('image', '')
            # NOUVEAU : Récupération du synopsis
            synopsis = row.get('synopsis', 'Aucune description disponible pour ce film.')
            
            # Petit bonus : Un badge de qualité aléatoire pour le style Netflix
            badge_qualite = random.choice(["4K", "HD", "Ultra HD"])
            
            img_balise = f'<img src="{image_url}" class="movie-img" alt="{titre}">' if image_url else ''
            
            cards_html += f"""
            <div class="glass-card">
                <div class="img-container">
                    {img_balise}
                    <span class="badge">{badge_qualite}</span>
                </div>
                <div class="card-content">
                    <h3>{titre}</h3>
                    <p class="movie-synopsis">{synopsis}</p>
                    <div class="time-badge">
                        <i class="fas fa-clock"></i> {horaires}
                    </div>
                </div>
            </div>
            """

        # 2. Le template complet avec CSS mis à jour
        full_html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                body {{
                    background-color: #141414;
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    margin: 0;
                    padding: 40px;
                }}
                .header {{
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .back-btn {{
                    color: #aaa;
                    text-decoration: none;
                    font-size: 24px;
                    transition: 0.3s;
                }}
                .back-btn:hover {{ color: white; transform: translateX(-5px); }}
                h1 {{ margin: 0; font-size: 2rem; }}
                .highlight {{ color: #E50914; }}
                
                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 30px;
                }}
                .glass-card {{
                    background: rgba(40, 40, 40, 0.4);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    display: flex;
                    flex-direction: column;
                }}
                .glass-card:hover {{
                    transform: scale(1.03);
                    border-color: #E50914;
                    z-index: 10;
                }}
                .img-container {{
                    position: relative;
                    width: 100%;
                    height: 400px;
                }}
                .movie-img {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }}
                .badge {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-size: 0.7rem;
                    font-weight: bold;
                    border: 1px solid #555;
                }}
                .card-content {{
                    padding: 20px;
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                }}
                h3 {{ margin: 0 0 10px 0; font-size: 1.2rem; }}
                
                /* Style pour le synopsis */
                .movie-synopsis {{
                    font-size: 0.85rem;
                    color: #bbb;
                    margin-bottom: 20px;
                    line-height: 1.4;
                    flex-grow: 1;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }}
                
                .time-badge {{
                    display: inline-block;
                    background: rgba(229, 9, 20, 0.15);
                    color: #ff4d4d;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 0.85rem;
                    align-self: flex-start;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    color: #666;
                    font-size: 0.8rem;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <a href="index.html" class="back-btn" title="Retour à l'accueil">
                    <i class="fas fa-arrow-left"></i>
                </a>
                <h1>Séances <span class="highlight">Madiana</span></h1>
            </div>
            
            <div class="grid">
                {cards_html}
            </div>

            <div class="footer">
                Mis à jour le {time.strftime('%d/%m/%Y à %H:%M')}
            </div>
        </body>
        </html>
        """

        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"🌐 [HTML] Interface Premium avec descriptions générée : {path}")