class Etudiant:
    def __init__(self, nom, prenom, numero_etudiant):
        # On initialise les attributs propres à chaque étudiant
        self.nom = nom  # Nom de l'étudiant
        self.prenom = prenom  # Prénom de l'étudiant
        self.numero_etudiant = numero_etudiant  # Numéro étudiant
        self.notes = []  # Liste vide pour stocker les notes (propre à chaque objet)

    def ajouter_note(self, note):
        # Vérifie que la note est comprise entre 0 et 20
        if 0 <= note <= 20:
            self.notes.append(note)  # Ajoute la note à la liste
        else:
            raise ValueError("La note doit être comprise entre 0 et 20")

    def calculer_moyenne(self):
        # Vérifie qu'il y a au moins une note
        if len(self.notes) == 0:
            return 0  # Évite division par zéro
        return sum(self.notes) / len(self.notes)  # Moyenne

    def est_admis(self):
        # Retourne True si moyenne >= 10
        return self.calculer_moyenne() >= 10


class Promotion:
    def __init__(self, nom_promotion):
        self.nom_promotion = nom_promotion  # Nom de la promotion
        self.etudiants = []  # Liste des étudiants

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)  # Ajoute un objet Etudiant

    def calculer_moyenne_promotion(self):
        if len(self.etudiants) == 0: 
            return 0
        total = sum(e.calculer_moyenne() for e in self.etudiants)
        return total / len(self.etudiants)

    def lister_admis(self):
        return [e for e in self.etudiants if e.est_admis()]
