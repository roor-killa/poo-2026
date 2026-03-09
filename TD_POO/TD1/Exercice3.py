class CompteurNotes:

    historique_notes = []

    @classmethod
    def ajouter_note_historique(cls, note):

        cls.historique_notes.append(note)

    @classmethod
    def statistiques(cls):

        if len(cls.historique_notes) == 0:
            return "Aucune note"

        minimum = min(cls.historique_notes)
        maximum = max(cls.historique_notes)
        moyenne = sum(cls.historique_notes) / len(cls.historique_notes)

        return {
            "min": minimum,
            "max": maximum,
            "moyenne": moyenne
        }


class Etudiant:

    compteur_total = 0
    universite = "Université des Antilles"

    def __init__(self, nom, prenom, numero_etudiant):

        self.nom = nom
        self.prenom = prenom
        self.numero_etudiant = numero_etudiant
        self.notes = []

        Etudiant.compteur_total += 1

    def ajouter_note(self, note):

        if 0 <= note <= 20:

            self.notes.append(note)

            CompteurNotes.ajouter_note_historique(note)

        else:

            print("Note invalide")

    @classmethod
    def get_nombre_etudiants(cls):

        return cls.compteur_total

    @classmethod
    def changer_universite(cls, nouvelle_universite):

        cls.universite = nouvelle_universite


print(Etudiant.get_nombre_etudiants())

e1 = Etudiant("A", "A", "E00001")
e2 = Etudiant("B", "B", "E00002")
e3 = Etudiant("C", "C", "E00003")

print(Etudiant.get_nombre_etudiants())

print(e1.universite)

Etudiant.changer_universite("UA - Campus de Schoelcher")

print(e2.universite)

# ajouter notes
e1.ajouter_note(15)
e2.ajouter_note(12)
e3.ajouter_note(18)

print(CompteurNotes.statistiques())
