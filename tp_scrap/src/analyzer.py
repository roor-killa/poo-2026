import pandas as pd
import os
from typing import List, Dict
import time 

class DataAnalyzer:
    def __init__(self, raw_data: List[Dict]):
        self.df = pd.DataFrame(raw_data)

    def show_statistics(self):
        if self.df.empty: return
        print(f"\n📊 Total : {len(self.df)} films scrapés.")

    def export_to_csv(self, filename: str = "donnees_globales"):
        output_dir = os.path.join("data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        self.df.to_csv(os.path.join(output_dir, f"{filename}.csv"), index=False, encoding='utf-8-sig')

    def export_to_html(self, file_name):
        os.makedirs(os.path.join("data", "processed"), exist_ok=True)
        path = f"data/processed/{file_name}.html"
        
        cards_html = ""
        for _, row in self.df.iterrows():
            cards_html += f"""
            <div style="background:#222; border-radius:10px; overflow:hidden; border:1px solid #333;">
                <img src="{row.get('image')}" style="width:100%; height:350px; object-fit:cover;">
                <div style="padding:15px;">
                    <h3 style="margin:0; font-size:1.1rem;">{row.get('titre')}</h3>
                    <p style="color:#E50914; font-weight:bold; margin-top:10px;">{row.get('horaires')}</p>
                </div>
            </div>
            """

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ background:#141414; color:white; font-family:sans-serif; padding:20px; }}
                .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); gap:20px; }}
            </style>
        </head>
        <body>
            <a href="index.html" style="color:#666; text-decoration:none;">← Retour</a>
            <h1 style="margin:20px 0;">Séances <span style="color:#E50914;">Madiana</span></h1>
            <div class="grid">{cards_html}</div>
        </body>
        </html>
        """
        with open(path, "w", encoding="utf-8") as f: f.write(full_html)