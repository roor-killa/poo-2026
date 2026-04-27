import sys
from src.manager import ScraperManager
from src.analyzer import DataAnalyzer

# On ajoute PrettyTable pour le rendu visuel
from prettytable import PrettyTable 

def afficher_joli_tableau(donnees, titre_tableau):
    """Génère un tableau stylé dans le terminal pour l'oral."""
    if not donnees:
        return
    
    table = PrettyTable()
    # On définit les colonnes
    table.field_names = ["🎬 Film", "⏰ Horaires", "📍 Source"]
    
    # Alignement à gauche pour les textes longs
    table.align["🎬 Film"] = "l"
    table.align["⏰ Horaires"] = "l"

    for item in donnees:
        # On récupère les infos (avec des valeurs par défaut si vide)
        titre = item.get('titre', 'Inconnu')
        horaire = item.get('horaires', 'Non spécifié')
        source = item.get('source', 'Madiana')
        table.add_row([titre, horaire, source])

    print(f"\n📊 {titre_tableau}")
    print(table)

def main():
    # ==========================================================
    # 🎯 CAS 1 : L'utilisateur cible un site (ex: python main.py madiana)
    # ==========================================================
    if len(sys.argv) > 1:
        site_cible = sys.argv[1].lower()
        print(f"\n🎯 DÉMARRAGE DU SCRAPING CIBLÉ : {site_cible.upper()} 🎯")
        print("==================================================")
        
        manager = ScraperManager()
        scraper = manager.create_scraper(site_cible)
        
        if scraper:
            donnees_recoltees = scraper.scrape()
            print(f"\n✅ Scraping de {site_cible.capitalize()} terminé !")
            
            if donnees_recoltees:
                # --- RENDU 1 : LE TERMINAL ---
                afficher_joli_tableau(donnees_recoltees, f"RÉSULTATS DE {site_cible.upper()}")
                
                print("\n🧠 Analyse des données de ce site...")
                analyste = DataAnalyzer(donnees_recoltees)
                analyste.show_statistics()
                
                # --- RENDU 2 & 3 : CSV + HTML ---
                nom_fichier = f"scraping_{site_cible}_uniquement"
                analyste.export_to_csv(nom_fichier)
                # CORRECTION ICI : On utilise bien le nom_fichier pour générer la galerie de films
                analyste.export_to_html(nom_fichier) 
        else:
            print(f"\n❌ Erreur : Le scraper pour '{site_cible}' n'existe pas.")

    # ==========================================================
    # 🌍 CAS 2 : Comportement de base (python main.py)
    # ==========================================================
    else:
        print("🌟 DÉMARRAGE DU PROGRAMME DE SCRAPING GLOBAL 🌟")
        print("==================================================")
        
        manager = ScraperManager()
        donnees_recoltees = manager.run_all()
        
        if donnees_recoltees:
            # --- RENDU 1 : LE TERMINAL ---
            afficher_joli_tableau(donnees_recoltees, "RÉCAPITULATIF GLOBAL")

            print("\n🧠 Début de l'analyse des données...")
            analyste = DataAnalyzer(donnees_recoltees)
            analyste.show_statistics()
            
            # --- RENDU 2 & 3 : CSV + HTML ---
            nom_global = "scraping_final_martinique"
            analyste.export_to_csv(nom_global)
            # CORRECTION ICI : On utilise bien le nom_global
            analyste.export_to_html(nom_global) 
            
        print("\n✅ PROGRAMME TERMINÉ AVEC SUCCÈS ! ✅")

if __name__ == "__main__":
    main()