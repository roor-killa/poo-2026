class CompteBancaire:
    def __init__(self, numero, titulaire, solde=0):
        self.numero = numero
        self.titulaire = titulaire
        self.solde = solde
        self.historique = []

    def deposer(self, montant):
        if montant <= 0:
            print("Le montant doit être positif.")
            return
        self.solde += montant
        self.historique.append(f"Dépôt : +{montant}€")

    def retirer(self, montant):
        if montant <= 0:
            print("Le montant doit être positif.")
            return False
        if montant > self.solde:
            print("Solde insuffisant.")
            return False
        self.solde -= montant
        self.historique.append(f"Retrait : -{montant}€")
        return True

    def afficher_solde(self):
        print(f"Solde du compte : {self.solde}€")

    def afficher_historique(self):
        for operation in self.historique:
            print(operation)(self)

            
