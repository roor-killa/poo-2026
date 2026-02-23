class Vehicule:
    nombre_vehicules = 0

    def __init__(self, marque, modele, annee, prix):
        Vehicule.nombre_vehicules += 1
        self.marque = marque
        self.modele = modele
        self.annee = annee
        self.prix = prix
        self.kilometrage = 0

    def aLicher_info(self):
        return f"{self.marque} {self.modele} ({self.annee}) - {self.prix}€"

    def rouler(self, distance):
        self.kilometrage += distance

    def calculer_decote(self):
        age = 2024 - self.annee
        decote = self.prix * (age * 0.10)
        return max(0, self.prix - decote)


class Voiture(Vehicule):
    def __init__(self, marque, modele, annee, prix, nb_portes, type_carburant):
        super().__init__(marque, modele, annee, prix)
        self.nb_portes = nb_portes
        self.type_carburant = type_carburant

    def aLicher_info(self):
        return f"{super().aLicher_info()} - {self.nb_portes} portes - {self.type_carburant}"

    def rouler(self, distance):
        super().rouler(distance)
        conso = distance * 0.06
        print(f"{distance} km parcourus – {conso:.1f} L consommés")


class Moto(Vehicule):
    def __init__(self, marque, modele, annee, prix, cylindree, type_moto):
        super().__init__(marque, modele, annee, prix)
        self.cylindree = cylindree
        self.type_moto = type_moto


class Camion(Vehicule):
    def __init__(self, marque, modele, annee, prix, charge_max, nb_essieux):
        super().__init__(marque, modele, annee, prix)
        self.charge_max = charge_max
        self.nb_essieux = nb_essieux

    def rouler(self, distance, charge_actuelle=0):
        if charge_actuelle > self.charge_max:
            raise ValueError("Surcharge!")
        self.kilometrage += distance


class VehiculeElectrique(Vehicule):
    def __init__(self, marque, modele, annee, prix, autonomie_km, capacite_batterie):
        super().__init__(marque, modele, annee, prix)
        self.autonomie_km = autonomie_km
        self.capacite_batterie = capacite_batterie
        self.charge_actuelle = 100

    def rouler(self, distance):
        pourcentage = (distance / self.autonomie_km) * 100
        self.charge_actuelle -= pourcentage
        self.kilometrage += distance

    def recharger(self):
        self.charge_actuelle = 100

    def autonomie_restante(self):
        return int(self.autonomie_km * self.charge_actuelle / 100)

#EXERCICE 3.2
from abc import ABC, abstractmethod
from datetime import datetime

class MoyenPaiement(ABC):
    def __init__(self, titulaire):
        self.titulaire = titulaire
        self._historique = []

    @abstractmethod
    def payer(self, montant, description=""):
        pass

    @abstractmethod
    def valider_paiement(self, montant):
        pass

    def enregistrer_transaction(self, montant, description, statut):
        self._historique.append({
            "date": datetime.now(),
            "montant": montant,
            "description": description,
            "statut": statut
        })

    def afficher_historique(self):
        for t in self._historique:
            print(f"{t['date']:%d/%m/%Y %H:%M} - {t['montant']}€ - {t['description']} [{t['statut']}]")

class CarteBancaire(MoyenPaiement):
    def __init__(self, titulaire, numero, solde, plafond_mensuel=3000):
        super().__init__(titulaire)
        self.numero = numero
        self.solde = solde
        self.plafond = plafond_mensuel
        self.depenses = 0

    def valider_paiement(self, montant):
        return montant <= self.solde and self.depenses + montant <= self.plafond

    def payer(self, montant, description=""):
        if not self.valider_paiement(montant):
            self.enregistrer_transaction(montant, description, "REFUSÉ")
            raise ValueError("Paiement refusé")
        self.solde -= montant
        self.depenses += montant
        self.enregistrer_transaction(montant, description, "ACCEPTÉ")

class PayPal(MoyenPaiement):
    def __init__(self, titulaire, email, solde):
        super().__init__(titulaire)
        self.email = email
        self.solde = solde

    def valider_paiement(self, montant):
        frais = montant * 0.029 + 0.30
        return self.solde >= montant + frais

    def payer(self, montant, description=""):
        frais = montant * 0.029 + 0.30
        total = montant + frais
        if not self.valider_paiement(montant):
            raise ValueError("Solde insuffisant")
        self.solde -= total
        self.enregistrer_transaction(montant, description, "ACCEPTÉ")

#EXERCICE 3.3
from datetime import datetime

class Employe:
    def __init__(self, nom, prenom, matricule, date_embauche, salaire_base):
        self.nom = nom
        self.prenom = prenom
        self.matricule = matricule
        self.date_embauche = datetime.strptime(date_embauche, "%d/%m/%Y")
        self.salaire_base = salaire_base

    def calculer_anciennete(self):
        return (datetime.now() - self.date_embauche).days // 365

    def calculer_prime_anciennete(self):
        return self.salaire_base * 0.01 * self.calculer_anciennete()

    def calculer_salaire_mensuel(self):
        return self.salaire_base

class Technicien(Employe):
    def __init__(self, nom, prenom, matricule, date_embauche, salaire_base, specialite):
        super().__init__(nom, prenom, matricule, date_embauche, salaire_base)
        self.specialite = specialite

    def calculer_salaire_mensuel(self):
        return self.salaire_base + self.calculer_prime_anciennete() + 300

class Manager(Employe):

    def __init__(self, nom, prenom, matricule, date_embauche, salaire_base, taille_equipe):
        # ⚠️ On passe UNIQUEMENT les arguments attendus par Employe
        super().__init__(nom, prenom, matricule, date_embauche, salaire_base)

        # Attribut spécifique à Manager
        self.taille_equipe = taille_equipe
        self.equipe = []

    def ajouter_membre_equipe(self, employe):
        if len(self.equipe) >= self.taille_equipe:
            raise ValueError("Équipe complète")
        self.equipe.append(employe)

    def calculer_salaire_mensuel(self):
        return self.salaire_base + 500 + len(self.equipe) * 100


class DirecteurTechnique(Manager, Technicien):
    def __init__(self, nom, prenom, matricule, date_embauche,
                 salaire_base, taille_equipe, specialite):

        # Initialisation directe de Employe
        Employe.__init__(self, nom, prenom, matricule, date_embauche, salaire_base)

        # Attributs Manager
        self.taille_equipe = taille_equipe
        self.equipe = []

        # Attribut Technicien
        self.specialite = specialite

    def calculer_salaire_mensuel(self):
        return (
            self.salaire_base
            + self.calculer_prime_anciennete()
            + 500
            + len(self.equipe) * 100
            + 300
        )


#Test EXERCICE 3.1
print("EXERCICE 3.1\n")
v1 = Voiture("Renault", "Clio", 2020, 15000, 5, "Essence")
print(v1.aLicher_info())
v1.rouler(100)

m1 = Moto("Yamaha", "R1", 2022, 18000, 1000, "Sportive")

c1 = Camion("Volvo", "FH16", 2019, 80000, 25000, 5)
try:
    c1.rouler(200, charge_actuelle=30000)
except ValueError as e:
    print("✓", e)

e1 = VehiculeElectrique("Tesla", "Model 3", 2023, 45000, 500, 75)
e1.rouler(250)
print("Autonomie restante:", e1.autonomie_restante(), "km")

print("Décote voiture:", v1.calculer_decote())
print("Total véhicules:", Vehicule.nombre_vehicules)
print(" ")

#Test EXERCICE 3.2
print("EXERCICE 3.2\n")
carte = CarteBancaire("Alice", "1234", 5000, 2000)
paypal = PayPal("Alice", "alice@mail.com", 1000)

carte.payer(50, "Restaurant")
paypal.payer(29.99, "Netflix")

try:
    carte.payer(3000, "TV")
except ValueError as e:
    print("✓ Paiement refusé")

carte.afficher_historique()
print(" ")

#Test EXERCICE 3.3
print("EXERCICE 3.3\n")
tech = Technicien("Dupont", "Jean", "T01", "01/01/2020", 2500, "Dev")
manager = Manager("Martin", "Sophie", "M01", "15/06/2018", 3500, 5)

manager.ajouter_membre_equipe(tech)

dt = DirecteurTechnique(
    "Leroy", "Marie", "DT01", "01/09/2015",
    4500, 10, "Système"
)

print("Salaire Technicien:", tech.calculer_salaire_mensuel())
print("Salaire Manager:", manager.calculer_salaire_mensuel())
print("Salaire DT:", dt.calculer_salaire_mensuel())
print("MRO:\n", DirecteurTechnique.__mro__)