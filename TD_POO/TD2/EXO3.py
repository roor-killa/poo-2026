# -----------------------------
# Classe Section
# -----------------------------

# Une section représente une partie de la bibliothèque
# Exemple : Sciences, Littérature, Informatique

class Section:

    def __init__(self, nom, capacite):

        # nom de la section
        self.nom = nom

        # capacité maximale de documents
        self.capacite = capacite

        # liste des documents présents dans la section
        self.documents = []

    # méthode pour ajouter un document dans la section
    def ajouter_document(self, titre):

        # on vérifie que la section n'est pas pleine
        if len(self.documents) < self.capacite:

            self.documents.append(titre)

        else:

            print("Section pleine")


# -----------------------------
# Classe Bibliotheque
# -----------------------------

class Bibliotheque:

    def __init__(self, nom):

        # nom de la bibliothèque
        self.nom = nom

        # liste des sections de la bibliothèque
        self.sections = []

    # méthode pour ajouter une section
    def ajouter_section(self, section):

        self.sections.append(section)

    # méthode pour rechercher un document dans toutes les sections
    def rechercher_document(self, titre):

        # on parcourt toutes les sections
        for section in self.sections:

            # on vérifie si le document est dans la section
            if titre in section.documents:

                return f"Document trouvé dans la section {section.nom}"

        return "Document non trouvé"

    # méthode pour afficher le nombre de documents par section
    def afficher_statistiques(self):

        print(f"Statistiques de la bibliothèque : {self.nom}")

        for section in self.sections:

            print(f"{section.nom} : {len(section.documents)} documents")


# création de la bibliothèque
biblio = Bibliotheque("Bibliothèque Schoelcher")

# création des sections
section_sciences = Section("Sciences", 1000)
section_litterature = Section("Littérature", 800)

# ajout des sections à la bibliothèque
biblio.ajouter_section(section_sciences)
biblio.ajouter_section(section_litterature)

# ajout de documents
section_sciences.ajouter_document("Livre Python")
section_sciences.ajouter_document("Machine Learning")

section_litterature.ajouter_document("Les Misérables")

# recherche d'un document
print(biblio.rechercher_document("Livre Python"))

# affichage des statistiques
biblio.afficher_statistiques()
