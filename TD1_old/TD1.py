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
        message = f"Dépôt de {montant}€ sur le compte {self.numero}"

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
