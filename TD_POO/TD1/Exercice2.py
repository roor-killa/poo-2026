class Etudiant:

    def __init__(self, nom, prenom, numero_etudiant):

        # validation du numero étudiant
        if not (numero_etudiant.startswith("E") and len(numero_etudiant) == 6):
            raise ValueError("Le numéro étudiant doit commencer par E et contenir 5 chiffres")

        self.nom = nom
        self.prenom = prenom

        # attribut privé
        self.__numero_etudiant = numero_etudiant

        # attribut protégé
        self._notes = []

    # property pour lire le numero étudiant
    @property
    def numero_etudiant(self):
        return self.__numero_etudiant

    # property moyenne (lecture seule)
    @property
    def moyenne(self):

        if len(self._notes) == 0:
            return 0

        return sum(self._notes) / len(self._notes)

    # ajouter une note
    def ajouter_note(self, note):

        if len(self._notes) >= 10:
            print("❌ Maximum 10 notes atteint")
            return

        if 0 <= note <= 20:
            self._notes.append(note)
        else:
            print("❌ Note invalide")

    # affichage lisible
    def __str__(self):

        return f"{self.prenom} {self.nom} ({self.numero_etudiant}) - Moyenne : {self.moyenne:.2f}"


etudiant = Etudiant("Dubois", "Jean", "E12347")

etudiant.ajouter_note(15)
etudiant.ajouter_note(12)
etudiant.ajouter_note(14)

print(etudiant.moyenne)

print(etudiant.numero_etudiant)

print(etudiant)

# test erreur
try:
    etudiant_invalide = Etudiant("Test", "Test", "12345")
except ValueError as e:
    print(f"Erreur attendue : {e}")
