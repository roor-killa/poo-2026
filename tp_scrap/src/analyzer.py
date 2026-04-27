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
            
            # --- TRANSFORMATION DES HORAIRES EN PILULES ---
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
                    --bg-dark: #0f0f0f;
                    --glass: rgba(255, 255, 255, 0.03);
                }}
                
                body {{
                    background-color: var(--bg-dark);
                    color: white;
                    font-family: 'Inter', -apple-system, sans-serif;
                    margin: 0;
                    padding: 15px;
                }}

                .container {{ max-width: 1200px; margin: 0 auto; }}

                .header {{ 
                    display: flex; 
                    align-items: center; 
                    margin: 20px 0 30px 0; 
                    gap: 15px; 
                }}
                
                .back-btn {{ 
                    color: white; 
                    background: rgba(255,255,255,0.05); 
                    padding: 10px 14px; 
                    border-radius: 50%; 
                    text-decoration: none; 
                    font-size: 1.2rem;
                }}

                h1 {{ font-size: 1.5rem; margin: 0; font-weight: 900; letter-spacing: -1px; }}
                h1 span {{ color: var(--netflix-red); }}

                /* --- GRILLE RESPONSIVE --- */
                .grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr); /* 2 colonnes par défaut sur Mobile */
                    gap: 12px;
                }}

                /* Si l'écran fait plus de 768px (Tablette/PC) */
                @media (min-width: 768px) {{
                    body {{ padding: 40px; }}
                    h1 {{ font-size: 2.2rem; }}
                    .grid {{ 
                        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); 
                        gap: 25px; 
                    }}
                    .img-container {{ height: 380px !important; }}
                    h3 {{ font-size: 1.2rem !important; }}
                }}

                .glass-card {{
                    background: var(--glass);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}

                .img-container {{ 
                    position: relative; 
                    height: 220px; /* Hauteur adaptée pour le 2 colonnes mobile */
                }}
                
                .movie-img {{ width: 100%; height: 100%; object-fit: cover; }}
                .overlay {{ 
                    position: absolute; 
                    bottom: 0; left: 0; right: 0; 
                    height: 50%; 
                    background: linear-gradient(transparent, rgba(15,15,15,0.9)); 
                }}

                .card-content {{ padding: 12px; flex-grow: 1; }}
                
                h3 {{ 
                    margin: 0 0 10px 0; 
                    font-size: 0.95rem; 
                    font-weight: 700;
                    line-height: 1.2;
                    min-height: 2.4em;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }}

                .pills-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 6px;
                }}

                .time-pill {{
                    background: rgba(229, 9, 20, 0.1);
                    border: 1px solid rgba(229, 9, 20, 0.2);
                    color: #ff4d4d;
                    padding: 4px 8px;
                    border-radius: 6px;
                    font-size: 0.75rem;
                    font-weight: 700;
                }}

                .footer {{ margin-top: 50px; text-align: center; color: #333; font-size: 0.7rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <a href="index.html" class="back-btn"><i class="fas fa-chevron-left"></i></a>
                    <h1>Ciné<span>Madiana</span></h1>
                </div>

                <div class="grid">
                    {cards_html}
                </div>

                <div class="footer">
                    Généré automatiquement • {time.strftime('%H:%M')}
                </div>
            </div>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"📱 Interface Mobile-First générée : {path}")