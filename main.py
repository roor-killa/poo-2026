# main.py
from modeles.bibliotheque import Bibliotheque
from modeles.utilisateurs import Etudiant, Enseignant
from services.fabrique import FabriqueDocument
from services.notifications import JournalEvenements, StatistiquesEmprunts

# 1️⃣ Créer la bibliothèque
biblio = Bibliotheque("Bibliothèque Universitaire")

# 2️⃣ Ajouter des documents via la fabrique
documents_data = [
    {"type": "livre", "titre": "Python avancé", "auteur": "Dupont", "isbn": "123"},
    {"type": "magazine", "titre": "Tech Review", "editeur": "TechPub", "numero": 5},
    {"type": "dvd", "titre": "Formation Python", "realisateur": "Martin", "duree": 120},
    {"type": "ebook", "titre": "Python pour débutants", "auteur": "Durand", "fichier": "python_debut.pdf"}
]

for data in documents_data:
    type_doc = data.pop("type")
    doc = FabriqueDocument.creer(type_doc, **data)
    biblio.ajouter_document(doc)

# 3️⃣ Créer des utilisateurs
etudiant = Etudiant("Dubois", "Marie", "E12345")
enseignant = Enseignant("Leroy", "Jean", "T001")
biblio.ajouter_utilisateur(etudiant)
biblio.ajouter_utilisateur(enseignant)

# 4️⃣ Ajouter des observateurs
journal = JournalEvenements()
stats = StatistiquesEmprunts()
biblio.ajouter_observateur(journal)
biblio.ajouter_observateur(stats)

# 5️⃣ Effectuer des emprunts
livre = biblio.rechercher_document("Python avancé")
if livre:
    biblio.emprunter(etudiant, livre)

dvd = biblio.rechercher_document("Formation Python")
if dvd:
    biblio.emprunter(enseignant, dvd)

# 6️⃣ Retourner un document pour tester les frais et notifications
from datetime import datetime, timedelta
# Simuler un retour après 35 jours pour le livre
emprunt_livre = biblio.emprunts_actifs[0]
emprunt_livre.date_emprunt -= timedelta(days=35)
biblio.retourner(emprunt_livre)

# 7️⃣ Afficher les statistiques
biblio.afficher_statistiques()
stats.afficher_stats()