class Wallet:
    def __init__(self, adresse, nom_proprietaire, solde):
        self.adresse = adresse
        self.nom_proprietaire = nom_proprietaire
        self.solde = solde
        self.historique = []

    
    def envoyer(self, montant, destinataire):
        if montant <= 0:
            return ("Montant invalide")
        if montant > self.solde :
            return ("Solde insuffisant")
        self.solde -= montant
        destinataire.recevoir(montant, self)
        self.historique.append(("envoyer", montant, destinataire.nom_proprietaire))
        return (f"✅ Transfert de {montant} BKN réussi")


    def recevoir(self, montant, expediteur):
        self.solde += montant
        self.historique.append(("recevoir", montant, expediteur.nom_proprietaire))
    

    def consulter_historique(self):
        return self.historique
