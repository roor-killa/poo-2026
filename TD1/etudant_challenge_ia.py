class Etudiant:
    nombre_etudiants = 0  # attribut de classe

    def __init__(self, nom, prenom, numetu, uni=""):
        self.nom = nom
        self.prenom = prenom
        self.num_etu = numetu
        self.uni = uni
        self.__notes = {}  # dict: {matiere: [notes]}

    def ajouter_note(self, matiere, note):
        # Vérif type
        if not isinstance(note, (int, float)):
            print("Note invalide. La note doit être un nombre.")
            return

        # Vérif intervalle
        if note < 0 or note > 20:
            print("Note invalide. La note doit être entre 0 et 20.")
            return

        # Ajout
        if matiere not in self.__notes:
            self.__notes[matiere] = []
        self.__notes[matiere].append(float(note))

    def calculer_moyenne(self):
        toutes_les_notes = []
        for liste in self.__notes.values():
            toutes_les_notes.extend(liste)

        if not toutes_les_notes:
            return 0

        return sum(toutes_les_notes) / len(toutes_les_notes)

    def moyenne_matiere(self, matiere):
        if matiere not in self.__notes or len(self.__notes[matiere]) == 0:
            return 0
        return sum(self.__notes[matiere]) / len(self.__notes[matiere])

    def est_admis(self, base=10):
        return self.calculer_moyenne() >= base

    def obtention_mention(self):
        m = self.calculer_moyenne()
        if m < 10:
            return "Aucune"
        elif m < 12:
            return "Passable"
        elif m < 14:
            return "Assez bien"
        elif m < 16:
            return "Bien"
        else:
            return "Très bien"

    def comparer_etudiant(self, autre):
        # >0 si self meilleur, <0 si autre meilleur, 0 égalité
        return self.calculer_moyenne() - autre.calculer_moyenne()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.num_etu}) - Moyenne: {self.calculer_moyenne():.2f}"


class Promotion:
    def __init__(self, nom_promo=""):
        self.etudiants = []
        self.nom_promo = nom_promo

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)
        Etudiant.nombre_etudiants += 1

    def calculer_moyenne_promo(self):
        if not self.etudiants:
            return 0
        total = sum(e.calculer_moyenne() for e in self.etudiants)
        return total / len(self.etudiants)

    def lister_admis(self, base=10):
        return [e for e in self.etudiants if e.est_admis(base)]

    def taux_de_reussite(self, base=10):
        if not self.etudiants:
            return 0
        nombre_admis = len(self.lister_admis(base))
        return (nombre_admis / len(self.etudiants)) * 100

    def best_etu(self):
        if not self.etudiants:
            return None
        return max(self.etudiants, key=lambda e: e.calculer_moyenne())


# -------------------
# TEST (corrigé)
# -------------------
alice = Etudiant("Alice", "Dupont", "E00001", "Informatique")
bob = Etudiant("Bob", "Martin", "E00002", "Mathématiques")

print(Etudiant.nombre_etudiants)  # 0
print(alice.uni)

alice.ajouter_note("Mathématiques", 15)
alice.ajouter_note("Mathématiques", 20)
alice.ajouter_note("Informatique", 18)

bob.ajouter_note("Mathématiques", 9)
bob.ajouter_note("Informatique", 12)
bob.ajouter_note("Informatique", 14)

print(f"La moyenne générale d'Alice est : {alice.calculer_moyenne():.2f}")
print(f"La moyenne générale de Bob est : {bob.calculer_moyenne():.2f}")
print(f"La moyenne de Mathématiques d'Alice est : {alice.moyenne_matiere('Mathématiques'):.2f}")
print(f"La moyenne de Informatique de Bob est : {bob.moyenne_matiere('Informatique'):.2f}")

difference = alice.comparer_etudiant(bob)
if difference > 0:
    print("Alice a une meilleure moyenne que Bob.")
elif difference < 0:
    print("Bob a une meilleure moyenne qu'Alice.")
else:
    print("Alice et Bob ont la même moyenne.")

promo = Promotion("L1 Informatique")
promo.ajouter_etudiant(alice)
promo.ajouter_etudiant(bob)

print(f"Moyenne de la promotion: {promo.calculer_moyenne_promo():.2f}")
print("Étudiants admis:")
for etu in promo.lister_admis():
    print(etu)

print(f"Taux de réussite de la promotion: {promo.taux_de_reussite():.2f}%")
best_student = promo.best_etu()
print(f"Le meilleur étudiant est : {best_student.nom} avec une moyenne de {best_student.calculer_moyenne():.2f}")

print(f"Alice a obtenu la mention : {alice.obtention_mention()}")
print(f"Bob a obtenu la mention : {bob.obtention_mention()}")



# Problème 1 : Incohérence sur l'attribut des notes
# Dans la première version, l'attribut était défini comme privé (__notes),
# mais certaines méthodes utilisaient self.notes.
# Cela provoquait une erreur car l'attribut n'existait pas sous ce nom.
# Correction : utilisation cohérente de self.__notes partout
# et stockage des notes dans un dictionnaire {matiere: [notes]}.


# Problème 2 : Attribut de classe non défini
# Le code utilisait nombre_etudiants dans Promotion.ajouter_etudiant(),
# mais cet attribut n'était pas défini dans la classe Etudiant.
# Cela provoquait une erreur AttributeError.
# Correction : ajout de l'attribut de classe
# nombre_etudiants = 0 dans la classe Etudiant.


# Problème 3 : Incohérence entre le constructeur et les tests
# Le constructeur initial ne prenait que 3 paramètres,
# alors que les tests en passaient 4 (avec la filière/université).
# De plus, plusieurs méthodes appelées dans les tests
# (moyenne_matiere, comparer_etudiant, obtention_mention)
# n'étaient pas implémentées.
# Correction : adaptation du constructeur avec le paramètre uni
# et implémentation des méthodes manquantes.

