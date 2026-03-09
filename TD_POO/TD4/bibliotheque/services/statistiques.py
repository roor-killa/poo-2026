# -----------------------------
# Classe StatistiquesBibliotheque
# -----------------------------

# Cette classe permet de calculer différentes statistiques
# à partir de la bibliothèque

class StatistiquesBibliotheque:

    @staticmethod
    def documents_par_type(catalogue):

        stats = {}

        for doc in catalogue:

            # récupérer le type du document
            type_doc = doc.__class__.__name__

            if type_doc not in stats:
                stats[type_doc] = 0

            stats[type_doc] += 1

        return stats


    @staticmethod
    def emprunts_par_utilisateur(utilisateurs):

        stats = {}

        for user in utilisateurs:

            stats[user.nom] = len(user.emprunts)

        return stats


    @staticmethod
    def taux_utilisation(catalogue):

        total = len(catalogue)

        if total == 0:
            return 0

        empruntes = 0

        for doc in catalogue:

            if not doc.disponible:
                empruntes += 1

        return (empruntes / total) * 100