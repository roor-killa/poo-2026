# -----------------------------
# Import des classes du projet
# -----------------------------

from modeles.bibliotheque import Bibliotheque
from modeles.utilisateurs import Etudiant, Enseignant
from services.fabrique import FabriqueDocument
from services.notifications import JournalEvenements, StatistiquesEmprunts
from services.statistiques import StatistiquesBibliotheque


# -----------------------------
# Création de la bibliothèque
# -----------------------------

biblio = Bibliotheque("Bibliothèque Universitaire")

print("Bibliothèque créée :", biblio.nom)


# -----------------------------
# Ajouter des documents via Factory
# -----------------------------

documents_data = [
    {"type": "livre", "titre": "Python avancé", "auteur": "Dupont", "isbn": "123"},
    {"type": "magazine", "titre": "Tech Review", "editeur": "TechPub", "numero": 5},
    {"type": "dvd", "titre": "Formation Python", "realisateur": "Martin", "duree": 120}
]


for data in documents_data:

    # récupérer le type
    type_doc = data.pop("type")

    # créer le document avec la factory
    doc = FabriqueDocument.creer(type_doc, **data)

    # ajouter au catalogue
    biblio.ajouter_document(doc)


print("Documents ajoutés au catalogue :", len(biblio.catalogue))


# -----------------------------
# Créer des utilisateurs
# -----------------------------

etudiant = Etudiant("Dubois", "Marie", "E12345")
enseignant = Enseignant("Leroy", "Jean", "T001")

biblio.ajouter_utilisateur(etudiant)
biblio.ajouter_utilisateur(enseignant)

print("Utilisateurs enregistrés :", len(biblio.utilisateurs))


# -----------------------------
# Système de notifications (Observer)
# -----------------------------

journal = JournalEvenements()
stats = StatistiquesEmprunts()

biblio.ajouter_observateur(journal)
biblio.ajouter_observateur(stats)


# -----------------------------
# Emprunter un document
# -----------------------------

livre = biblio.rechercher_document("Python avancé")

if livre:

    emprunt = biblio.emprunter(etudiant, livre)


# -----------------------------
# Afficher statistiques
# -----------------------------

print("\n--- Statistiques générales ---")

print("Documents par type :")
print(StatistiquesBibliotheque.documents_par_type(biblio.catalogue))

print("Emprunts par utilisateur :")
print(StatistiquesBibliotheque.emprunts_par_utilisateur(biblio.utilisateurs))

print("Taux d'utilisation :")
print(StatistiquesBibliotheque.taux_utilisation(biblio.catalogue), "%")


# -----------------------------
# Statistiques internes
# -----------------------------

print("\n--- Statistiques bibliothèque ---")
biblio.afficher_statistiques()