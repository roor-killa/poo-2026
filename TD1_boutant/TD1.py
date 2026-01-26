# EXERCICE 1.1
class CompteBancaire:
    # Constructeur : initialise un compte bancaire
    def __init__(self, numero, titulaire, solde=0.0):
        self.numero = numero          # Numéro du compte
        self.titulaire = titulaire    # Nom du titulaire
        self.solde = solde            # Solde initial
        self.historique = []          # Liste des opérations effectuées

    # Méthode pour déposer de l'argent sur le compte
    def deposer(self, montant):
        # Vérifie que le montant est positif
        if montant <= 0:
            raise ValueError("Le montant doit être positif")

        # Ajoute le montant au solde
        self.solde += montant

        # Message décrivant l'opération
        message = f"Dépôt de {montant}€ sur le compte {self.titulaire}"

        # Ajoute le message à l'historique
        self.historique.append(message)

        # Affiche le message
        print(message)

        # Affiche le solde après l'opération
        self.afficher_solde()

    # Méthode pour retirer de l'argent du compte
    def retirer(self, montant):
        # Vérifie que le montant est positif
        if montant <= 0:
            raise ValueError("Le montant doit être positif")

        # Vérifie si le solde est suffisant
        if montant > self.solde:
            print("Retrait refusé : solde insuffisant")
            self.afficher_solde()
            return False

        # Soustrait le montant du solde
        self.solde -= montant

        # Message décrivant l'opération
        message = f"Retrait de {montant}€ sur le compte {self.titulaire}"

        # Ajoute le message à l'historique
        self.historique.append(message)

        # Affiche le message
        print(message)

        # Affiche le solde après l'opération
        self.afficher_solde()

        # Indique que le retrait a réussi
        return True

    # Méthode pour afficher le solde actuel du compte
    def afficher_solde(self):
        print(f"Solde actuel du compte {self.titulaire} : {self.solde}€\n")

    # Méthode pour afficher l'historique des opérations
    def afficher_historique(self):
        print(f"Historique du compte {self.numero} :")
        for operation in self.historique:
            print(operation)

    # Méthode pour effectuer un virement vers un autre compte
    def virement(self, montant, autre_compte):
        # Tente de retirer le montant du compte source
        if self.retirer(montant):

            # Ajoute le montant au solde du compte destinataire
            autre_compte.solde += montant

            # Message pour le compte émetteur
            message_envoye = (
                f"Virement de {montant}€ du compte {self.titulaire} "
                f"vers le compte {autre_compte.titulaire}"
            )

            # Message pour le compte destinataire
            message_recu = (
                f"Virement de {montant}€ du compte {self.titulaire} "
                f"vers le compte {autre_compte.titulaire}"
            )

            # Ajoute les messages dans les historiques
            self.historique.append(message_envoye)
            autre_compte.historique.append(message_recu)

            # Affiche le message et le solde du compte émetteur
            print(message_envoye)
            self.afficher_solde()

            # Affiche le message et le solde du compte destinataire
            print(
                f"Réception d'un virement de {montant}€ "
                f"du compte {self.titulaire} sur le compte {autre_compte.titulaire}"
            )
            autre_compte.afficher_solde()

            # Indique que le virement a réussi
            return True

        # Message si le virement échoue
        print("Virement impossible")
        return False
    
#EXERCICE 1.2
class Etudiant:
    universite = "Université des Antilles"
    nombre_etudiants = 0

    def __init__(self, nom, prenom, numero_etudiant, filiere):
        self.nom = nom
        self.prenom = prenom
        self.numero_etudiant = numero_etudiant
        self.filiere = filiere
        self.notes = {}  # {matiere: [notes]}
        Etudiant.nombre_etudiants += 1

    def ajouter_note(self, matiere, note):
        if not 0 <= note <= 20:
            raise ValueError("La note doit être entre 0 et 20")
        self.notes.setdefault(matiere, []).append(note)

    def calculer_moyenne(self):
        total = 0
        count = 0
        for notes_matiere in self.notes.values():
            total += sum(notes_matiere)
            count += len(notes_matiere)
        return total / count if count > 0 else 0

    def calculer_moyenne_matiere(self, matiere):
        if matiere not in self.notes:
            return 0
        return sum(self.notes[matiere]) / len(self.notes[matiere])

    def est_admis(self, seuil=10):
        return self.calculer_moyenne() >= seuil

    def obtenir_mention(self):
        moyenne = self.calculer_moyenne()
        if moyenne < 10:
            return "Ajourné"
        elif moyenne < 12:
            return "Passable"
        elif moyenne < 14:
            return "Mention Assez bien"
        elif moyenne < 16:
            return "Mention Bien"
        else:
            return "Mention Très bien"

    def comparer_avec(self, autre_etudiant):
        if self.calculer_moyenne() > autre_etudiant.calculer_moyenne():
            return f"{self.prenom} a une meilleure moyenne que {autre_etudiant.prenom}"
        elif self.calculer_moyenne() < autre_etudiant.calculer_moyenne():
            return f"{autre_etudiant.prenom} a une meilleure moyenne que {self.prenom}"
        else:
            return "Les deux étudiants ont la même moyenne"

    def __str__(self):
        return (
            f"{self.prenom} {self.nom} ({self.numero_etudiant})\n"
            f"Filière : {self.filiere}\n"
            f"Moyenne : {self.calculer_moyenne():.2f}"
        )
    
class Promotion:
    def __init__(self, nom):
        self.nom = nom
        self.etudiants = []

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)

    def moyenne_promotion(self):
        if not self.etudiants:
            return 0
        return sum(e.calculer_moyenne() for e in self.etudiants) / len(self.etudiants)

    def taux_reussite(self):
        admis = [e for e in self.etudiants if e.est_admis()]
        return len(admis) / len(self.etudiants) * 100 if self.etudiants else 0

    def meilleur_etudiant(self):
        return max(self.etudiants, key=lambda e: e.calculer_moyenne(), default=None)

#EXERCICE 1.3
class Vecteur2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vecteur({self.x}, {self.y})"

    def __repr__(self):
        return f"Vecteur2D({self.x}, {self.y})"

    def __add__(self, autre):
        return Vecteur2D(self.x + autre.x, self.y + autre.y)

    def __sub__(self, autre):
        return Vecteur2D(self.x - autre.x, self.y - autre.y)

    def __mul__(self, scalaire):
        return Vecteur2D(self.x * scalaire, self.y * scalaire)

    def __rmul__(self, scalaire):
        return self.__mul__(scalaire)

    def __eq__(self, autre):
        return self.x == autre.x and self.y == autre.y

    def __abs__(self):
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self):
        return Vecteur2D(-self.x, -self.y)

    def produit_scalaire(self, autre):
        return self.x * autre.x + self.y * autre.y

    def angle_avec(self, autre):
        import math
        norme1 = abs(self)
        norme2 = abs(autre)
        if norme1 == 0 or norme2 == 0:
            raise ValueError("Angle indéfini avec un vecteur nul")
        cos_theta = self.produit_scalaire(autre) / (norme1 * norme2)
        cos_theta = max(-1, min(1, cos_theta))  # sécurité numérique
        return math.degrees(math.acos(cos_theta))


#Test EXERCICE 1.1
# Création de deux comptes bancaires
c1 = CompteBancaire("FR01", "Alice", 1000)
c2 = CompteBancaire("FR02", "Bob", 500)

# Dépôt d'argent sur le compte d'Alice
c1.deposer(500)

# Retrait d'argent sur le compte d'Alice
c1.retirer(100)

# Virement du compte d'Alice vers celui de Bob
c1.virement(200, c2)

# Affichage des soldes finaux
c1.afficher_solde()  # 1200€
c2.afficher_solde()  # 700€

#Test EXERCICE 1.2 - Classe Etudiant
alice = Etudiant("Dupont", "Alice", "E12345", "Informatique")
bob = Etudiant("Martin", "Bob", "E12346", "Informatique")

print("Nombre d'étudiants :",Etudiant.nombre_etudiants)  # Nombre d'étudiants : 2
print("Université d'Alice :",alice.universite)           # Université d'Alice : Université des Antilles

alice.ajouter_note("POO", 15)
alice.ajouter_note("Web", 14)
alice.ajouter_note("POO", 16)
alice.ajouter_note("Mobile", 13)

print("Moyenne Alice :",alice.calculer_moyenne())            # Moyenne Alice : 14.5
print("Moyenne POO Alice :",alice.calculer_moyenne_matiere("POO"))  # Moyenne POO Alice : 15.5
print("Alice est admis ? :",alice.est_admis())                   # Alice est admis ? True
print("Mention d'Alice :",alice.obtenir_mention())             # Mention d'Alice : Mention Bien

# Test EXERCICE 1.2 - Classe Promotion
# Création d'une promotion
promo_info = Promotion("Licence 2 Informatique")

# Ajout des étudiants à la promotion
promo_info.ajouter_etudiant(alice)
promo_info.ajouter_etudiant(bob)

# Ajout de notes à Bob pour avoir des comparaisons cohérentes
bob.ajouter_note("POO", 10)
bob.ajouter_note("Web", 11)
bob.ajouter_note("POO", 15)
bob.ajouter_note("Mobile", 12)

# Affichage des statistiques de la promotion
print("Nom de la promotion :", promo_info.nom) # Nom de la promotion : Licence 2 Informatique
print("Moyenne de la promotion :", promo_info.moyenne_promotion()) # Moyenne de la promotion : 12.75
print("Taux de réussite :", promo_info.taux_reussite(), "%") # Taux de réussite : 100 %

# Meilleur étudiant
meilleur = promo_info.meilleur_etudiant()
print("Meilleur étudiant :", meilleur.prenom, meilleur.nom) # Meilleur étudiant : Alice Dupont

# Comparaison entre deux étudiants
print(alice.comparer_avec(bob)) # Alice a une meilleure moyenne que Bob

#Test EXERCICE 1.3
v1 = Vecteur2D(3, 4)
v2 = Vecteur2D(1, 2)

print("v1 + V2 =",(v1 + v2))        # v1 + v2 = Vecteur(4, 6)
print("v1 - v2 =",(v1 - v2))        # v1 - v2 = Vecteur(2, 2)
print("v1 * 2 =",(v1 * 2))         # v1 * 2 = Vecteur(6, 8)
print("3 * v1 =",(3 * v1))         # 3* v1 = Vecteur(9, 12)
print("v1 = vecteur2D(3,4) ?",v1 == Vecteur2D(3, 4))  # v1 = vecteur2D(3,4) ? True
print("abs v1 =",abs(v1))        # abs v1 = 5.0
print("- v1 =",-v1)            # - v1 = Vecteur(-3, -4)
print("produit scalaire v1 =",v1.produit_scalaire(v2))  # produit scalaire v1 = 11
print("angle avec v2 =",v1.angle_avec(v2))        # angle avec v2 ≈ 10.3°