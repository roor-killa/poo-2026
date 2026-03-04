class CompteurNotes:
    # Attribut de classe : partagé par tous
    # Il stocke TOUTES les notes de TOUS les étudiants
    historique_notes = []

    @classmethod
    def ajouter_note_historique(cls, note):
        # cls représente la classe elle-même
        # On ajoute la note dans la liste globale
        cls.historique_notes.append(float(note))

    @classmethod
    def statistiques(cls):
        # Si aucune note n'existe
        if not cls.historique_notes:
            return {"min": None, "max": None, "moyenne": None}

        # Calcul des statistiques sur toutes les notes
        mini = min(cls.historique_notes)
        maxi = max(cls.historique_notes)
        moyenne = sum(cls.historique_notes) / len(cls.historique_notes)

        return {"min": mini, "max": maxi, "moyenne": moyenne}


class Etudiant:
    # Attributs de classe (partagés par tous les étudiants)
    compteur_total = 0
    universite = "Université des Antilles"

    def __init__(self, nom, prenom, numero_etudiant):
        self.nom = nom
        self.prenom = prenom

        # Vérifie que le numéro commence par "E" et contient 5 chiffres
        # Exemple valide : E12345
        if not (isinstance(numero_etudiant, str)
                and len(numero_etudiant) == 6
                and numero_etudiant[0] == "E"
                and numero_etudiant[1:].isdigit()):
            raise ValueError("Le numéro étudiant doit commencer par 'E' suivi de 5 chiffres.")

        # __numero_etudiant est privé
        # Python modifie son nom en interne pour éviter l'accès direct
        self.__numero_etudiant = numero_etudiant

        # _notes est protégé (convention : ne pas modifier hors classe)
        self._notes = []

        # On incrémente le compteur à chaque création d'étudiant
        Etudiant.compteur_total += 1

    @property
    def numero_etudiant(self):
        # Property en lecture seule (pas de setter)
        # On peut lire mais pas modifier
        return self.__numero_etudiant

    def ajouter_note(self, note):
        # Limite à 10 notes maximum
        if len(self._notes) >= 10:
            raise ValueError("Impossible d'ajouter plus de 10 notes.")

        # Vérifie que la note est un nombre
        if not isinstance(note, (int, float)):
            raise ValueError("La note doit être un nombre.")

        # Vérifie que la note est entre 0 et 20
        if note < 0 or note > 20:
            raise ValueError("La note doit être entre 0 et 20.")

        self._notes.append(float(note))

        # On ajoute aussi la note dans l'historique global
        CompteurNotes.ajouter_note_historique(note)

    def calculer_moyenne(self):
        # Méthode simple qui retourne la property moyenne
        return self.moyenne

    @property
    def moyenne(self):
        # Si aucune note, moyenne = 0
        if not self._notes:
            return 0

        # Calcul classique moyenne = somme / nombre
        return sum(self._notes) / len(self._notes)

    def est_admis(self, base=10):
        # L'étudiant est admis si moyenne >= 10
        return self.moyenne >= base

    def __str__(self):
        # Méthode spéciale appelée avec print(objet)
        # Permet un affichage propre
        return f"{self.prenom} {self.nom} ({self.numero_etudiant}) - Moyenne: {self.moyenne:.2f}"

    @classmethod
    def get_nombre_etudiants(cls):
        # Retourne le nombre total d'étudiants créés
        return cls.compteur_total

    @classmethod
    def changer_universite(cls, nouvelle_universite):
        # Change l'université pour TOUS les étudiants
        # car universite est un attribut de classe
        cls.universite = nouvelle_universite


class Promotion:
    def __init__(self, nom_promo=""):
        self.etudiants = []
        self.nom_promo = nom_promo

    def ajouter_etudiant(self, etudiant):
        # On ajoute simplement l'étudiant à la liste
        self.etudiants.append(etudiant)

    def calculer_moyenne_promo(self):
        if not self.etudiants:
            return 0

        # On calcule la moyenne des moyennes
        return sum(e.moyenne for e in self.etudiants) / len(self.etudiants)

    def lister_admis(self, base=10):
        # Compréhension de liste :
        # on garde seulement les étudiants admis
        return [e for e in self.etudiants if e.est_admis(base)]

print(Etudiant.get_nombre_etudiants())  # 0

e1 = Etudiant("A", "A", "E00001")
e2 = Etudiant("B", "B", "E00002")
e3 = Etudiant("C", "C", "E00003")

print(Etudiant.get_nombre_etudiants())  # 3
print(e1.universite)  # Université des Antilles

Etudiant.changer_universite("UA - Campus de Schoelcher")
print(e2.universite)  # UA Campus de Schoelcher

# Test statistiques
e1.ajouter_note(15)
e2.ajouter_note(12)
e3.ajouter_note(18)
print(CompteurNotes.statistiques())