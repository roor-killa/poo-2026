import pandas as pd
import os
from typing import List, Dict
import time 

class DataAnalyzer:
    def __init__(self, raw_data: List[Dict]):
        self.df = pd.DataFrame(raw_data)

    def show_statistics(self):
        if self.df.empty: return
        print(f"\n📊 Analyse terminée : {len(self.df)} films prêts.")

    def export_to_csv(self, filename: str = "donnees_globales"):
        output_dir = os.path.join("data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        self.df.to_csv(os.path.join(output_dir, f"{filename}.csv"), index=False, encoding='utf-8-sig')

    def export_to_html(self, file_name):
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        cards_html = ""
        for _, row in self.df.iterrows():
            image = row.get('image') or "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=400&h=600&auto=format&fit=crop"
            titre = row.get('titre', 'Film')
            horaires_brut = row.get('horaires', 'Non disponible')
            
            # --- TRANSFORMATION DES HORAIRES EN PILULES INDIVIDUELLES ---
            # On sépare le texte par le caractère "|" et on crée un petit badge pour chaque heure
            horaires_pills = ""
            if "|" in horaires_brut:
                liste_heures = horaires_brut.split("|")
                for h in liste_heures:
                    horaires_pills += f'<span class="time-pill">{h.strip()}</span>'
            else:
                horaires_pills = f'<span class="time-pill">{horaires_brut}</span>'

            cards_html += f"""
            <div class="glass-card">
                <div class="img-container">
                    <img src="{image}" class="movie-img" alt="{titre}">
                    <div class="overlay"></div>
                </div>
                <div class="card-content">
                    <h3>{titre}</h3>
                    <div class="pills-container">
                        {horaires_pills}
                    </div>
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
                    --glass: rgba(255, 255, 255, 0.03);
                }}
                
                body {{
                    background-color: var(--bg-dark);
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    margin: 0;
                    padding: 40px;
                }}

                .container {{ max-width: 1200px; margin: 0 auto; }}

                .header {{ display: flex; align-items: center; margin-bottom: 40px; gap: 20px; }}
                .back-btn {{ color: white; background: rgba(255,255,255,0.1); padding: 12px 15px; border-radius: 50%; text-decoration: none; transition: 0.3s; }}
                .back-btn:hover {{ background: var(--netflix-red); transform: scale(1.1); }}

                h1 {{ font-size: 2.2rem; margin: 0; font-weight: 800; }}
                h1 span {{ color: var(--netflix-red); }}

                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 35px;
                }}

                .glass-card {{
                    background: var(--glass);
                    backdrop-filter: blur(15px);
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    overflow: hidden;
                    transition: 0.4s ease;
                }}

                .glass-card:hover {{
                    transform: translateY(-10px);
                    border-color: rgba(229, 9, 20, 0.5);
                    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
                }}

                .img-container {{ position: relative; height: 400px; }}
                .movie-img {{ width: 100%; height: 100%; object-fit: cover; }}
                .overlay {{ position: absolute; bottom: 0; left: 0; right: 0; height: 60%; background: linear-gradient(transparent, var(--bg-dark)); }}

                .card-content {{ padding: 20px; }}
                h3 {{ margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700; }}

                /* --- STYLE MODERNE DES HORAIRES --- */
                .pills-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }}

                .time-pill {{
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: #fff;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                    transition: 0.3s;
                }}

                .glass-card:hover .time-pill {{
                    border-color: var(--netflix-red);
                    color: var(--netflix-red);
                    background: rgba(229, 9, 20, 0.05);
                    box-shadow: 0 0 10px rgba(229, 9, 20, 0.2);
                }}

                .footer {{ margin-top: 80px; text-align: center; color: #444; font-size: 0.8rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <a href="index.html" class="back-btn"><i class="fas fa-arrow-left"></i></a>
                    <h1>Ciné<span>Madiana</span></h1>
                </div>

                <div class="grid">
                    {cards_html}
                </div>

                <div class="footer">
                    Mise à jour automatique • {time.strftime('%H:%M')}
                </div>
            </div>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"✨ Interface Modernisée générée : {path}")