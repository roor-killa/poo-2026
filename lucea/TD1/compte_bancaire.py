class Compte_bancaire:
    def __init__(self, numero, titulaire, solde,):
        self.numero = numero
        self.titulaire = titulaire
        self.solde = solde
        self.historique = []
        
    def deposer(self, montant):
        if montant > 0:
            self.solde += montant
            self.historique.append(f"Dépôt de {montant}€")
            return "dépôt effectuer"
        return "montant invalide"
    
    def retirer(self, montant):
        if montant <= 0:
            print("montant invalide")
            return False
        if self.solde - montant < 0:
            print("solde insuffisant, retrait refusé")
            return False
        else:
            self.solde -= montant
            print("retrait effectuer")
            self.historique.append(f"Retrait de {montant}€")
            return True
    
    def afficher_solde(self):
        return f"Solde : {self.solde()}"
    
    def afficher_historique(self):
        return f"Historique : {self.historique}"
    
    def virement(self, montant, autre_compte):
        if self.retirer(montant) == True:
            autre_compte.deposer(montant)
            self.historique.append(f"Virement de {montant}€ vers le compte {autre_compte.numero}")
            return "virement effectuer avec succes"
        else:
            return "virement echoué, solde insuffisant"