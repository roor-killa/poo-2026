
class Etudiant:
    def __init__(self, nom, prenom, numero_etudiant):
        self.nom = nom
        self.prenom = prenom

        # numero_etudiant privé + validation "E" + 5 chiffres
        if not (isinstance(numero_etudiant, str)
                and len(numero_etudiant) == 6
                and numero_etudiant[0] == "E"
                and numero_etudiant[1:].isdigit()):
            raise ValueError("Le numéro étudiant doit commencer par 'E' suivi de 5 chiffres (ex: E12347).")

        self.__numero_etudiant = numero_etudiant  # privé, pas de setter
        self._notes = []  # protégé

    @property
    def numero_etudiant(self):
        # lecture seule (pas de setter)
        return self.__numero_etudiant

    def ajouter_note(self, note):
        # bloquer si déjà 10 notes
        if len(self._notes) >= 10:
            raise ValueError("Impossible d'ajouter une note : l'étudiant a déjà 10 notes.")

        # validation note 0..20
        if not isinstance(note, (int, float)):
            raise ValueError("Note invalide : la note doit être un nombre.")
        if note < 0 or note > 20:
            raise ValueError("Note invalide : la note doit être entre 0 et 20.")

        self._notes.append(float(note))

    @property
    def moyenne(self):
        # lecture seule
        if not self._notes:
            return 0
        return sum(self._notes) / len(self._notes)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_etudiant}) - Moyenne: {self.moyenne:.2f} - Notes: {len(self._notes)}/10"

 


class Promotion:
    def __init__(self, nom_promo=""):
        self.etudiants = []
        self.nom_promo = nom_promo

    def ajouter_etudiant(self, etudiant):
        etudiant.__class__.nombre_etudiants += 1

        self.etudiants.append(etudiant)
        etudiant.__class__.nombre_etudiants += 1  # Incrémente le nombre d'étudiants à chaque ajout

    def calculer_moyenne_promo(self):
        if not self.etudiants:
            return 0
        total_moyenne = sum(etudiant.calculer_moyenne() for etudiant in self.etudiants)
        return total_moyenne / len(self.etudiants)
    
    def lister_admis(self,):
        etu_admis = []
        for etudiant in self.etudiants:
            if etudiant.est_admis():
                etu_admis.append(etudiant)
        return etu_admis #ici on cree iune liste pour stocker les etudiants qui sont admis par "est_amis" on verifie si c'est true et on les affiche 
                
#q1 : Parce que sinon tous les etudiants vont partager la meme liste de notes car une liste de classe est partagée entre toutes les instances de la classe. 
#q2 :tous les objets partagent la même liste
#q3 : notes est encapsulée pour éviter les modifications donc il est privé de plus dans ajouter_notes il y a cette ligne :if __notes < 0 or __notes > 20:



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
print(f"Moyenne de {etudiant1.prenom} : {etudiant1.calculer_moyenne()}")
print(f"Est admis ? {etudiant1.est_admis()}")
print(f"Moyenne de la promotion : {promo.calculer_moyenne_promotion()}")
print(f"Étudiants admis : {len(promo.lister_admis())}")


#Challenge IA : dans le fichier etudiant_challenge_ia.py
#Générez le code avec une IA de votre choix
#Identifiez 3 problèmes ou améliorations possibles dans le code généré
#Proposez et implémentez vos corrections

#Q1 : Quelle est la différence entre _attribut et __attribut ?
#Q2 : Peut-on vraiment rendre un attribut privé en Python ?
#Q3 : Pourquoi utiliser @property plutôt qu'une méthode get_moyenne() ?

# Q1 :
# _attribut est protégé  (on ne doit pas y toucher hors de la classe).
# __attribut est privé grâce au name mangling (Python modifie son nom en interne).

# Q2 :
# Non on ne peut pas rendre un attribut totalement privé en Python.
# On peut seulement limiter l’accès par convention ou name mangling.

# Q3 :
# @property permet d’utiliser une méthode comme un attribut.
# C’est plus lisible (etudiant.moyenne au lieu de etudiant.get_moyenne()).
# On peut aussi empêcher la modification en ne mettant pas de setter.
