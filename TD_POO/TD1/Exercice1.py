class Etudiant:
    def __init__(self, nom, prenom, numero_etudiant):
        self.nom = nom
        self.prenom = prenom
        self.numero_etudiant = numero_etudiant
        self.notes = []

    def ajouter_note(self, note):
        if not isinstance(note, (int, float)):
            raise TypeError("La note doit être un nombre.")
        if not 0 <= note <= 20:
            raise ValueError("Note invalide: elle doit être entre 0 et 20.")
        self.notes.append(float(note))

    def calculer_moyenne(self):
        if len(self.notes) == 0:
            return 0.0
        return sum(self.notes) / len(self.notes)

    def est_admis(self):
        return self.calculer_moyenne() >= 10

    def __repr__(self):
        return f"Etudiant({self.nom} {self.prenom}, {self.numero_etudiant})"


class Promotion:
    def __init__(self, nom_promotion):
        self.nom_promotion = nom_promotion
        self.etudiants = []

    def ajouter_etudiant(self, etudiant):
        if not isinstance(etudiant, Etudiant):
            raise TypeError("Seuls des objets Etudiant peuvent être ajoutés.")

        for e in self.etudiants:
            if e.numero_etudiant == etudiant.numero_etudiant:
                raise ValueError(
                    f"Un étudiant avec le numéro {etudiant.numero_etudiant} existe déjà."
                )

        self.etudiants.append(etudiant)

    def calculer_moyenne_promotion(self):
        if len(self.etudiants) == 0:
            return 0.0
        total = 0.0
        for etudiant in self.etudiants:
            total += etudiant.calculer_moyenne()
        return total / len(self.etudiants)

    def lister_admis(self):
        admis = []
        for etudiant in self.etudiants:
            if etudiant.est_admis():
                admis.append(etudiant)
        return admis


# Réponses aux questions
Q1 = "notes doit être un attribut d'instance pour que chaque étudiant ait ses propres notes."
Q2 = (
    "Si notes = [] est un attribut de classe, la même liste est partagée par tous les étudiants."
)
Q3 = (
    "On valide dans ajouter_note et on lève une exception (ValueError) si la note n'est pas entre 0 et 20."
)


# Créer des étudiants
etudiant1 = Etudiant("Dupont", "Marie", "E12345")
etudiant1.ajouter_note(15)
etudiant1.ajouter_note(12)
etudiant1.ajouter_note(14)

etudiant2 = Etudiant("Martin", "Pierre", "E12346")
etudiant2.ajouter_note(8)
etudiant2.ajouter_note(9)

# Créer une promotion
promo = Promotion("L2 Informatique 2025")
promo.ajouter_etudiant(etudiant1)
promo.ajouter_etudiant(etudiant2)

# Afficher résultats
print(f"Moyenne de {etudiant1.prenom} : {etudiant1.calculer_moyenne():.2f}")
print(f"Est admis ? {etudiant1.est_admis()}")
print(f"Moyenne de la promotion : {promo.calculer_moyenne_promotion():.2f}")
print(f"Étudiants admis : {len(promo.lister_admis())}")

# Affichage Q/R demandé
print("\nQ1:", Q1)
print("Q2:", Q2)
print("Q3:", Q3)
