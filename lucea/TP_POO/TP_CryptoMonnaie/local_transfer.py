from wallet import Wallet
import datetime
import random

# Création de deux wallets
wallet1 = Wallet("1", "Alice", 1000)
wallet2 = Wallet("2", "Bob", 1000)

reponse = -1

while reponse != 0:
    print("💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
    print("1. Afficher les wallets")
    print("2. Transférer BKN (Wallet1 → Wallet2)")
    print("3. Transférer BKN (Wallet2 → Wallet1)")
    print("4. Historique Wallet1")
    print("5. Historique Wallet2")
    print("0. Quitter\n")
    reponse = int(input(("👉 Votre choix: ")))

    if reponse == 1:
        print("\nWallet1: ", wallet1.adresse, wallet1.nom_proprietaire, wallet1.solde)
        print("\nWallet2: ", wallet2.adresse, wallet2.nom_proprietaire, wallet2.solde)

    elif reponse == 2:
        print(f"\nTransfert: {wallet1.nom_proprietaire} → {wallet2.nom_proprietaire}")
        print(f"Solde disponible: {wallet1.solde} BKN")
        montant = float(input("Montant à transférer: "))
        resultat = wallet1.envoyer(montant, wallet2)
        print(resultat)
        transaction_id = f"TXN-BKN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100,999)}"
        print(f"Transaction: {transaction_id}")

        print("📊 Nouveaux soldes:")
        print(f"{wallet1.nom_proprietaire} : {wallet1.solde} BKN")
        print(f"{wallet2.nom_proprietaire} : {wallet2.solde} BKN")

    elif reponse == 3:
        print(f"\nTransfert: {wallet2.nom_proprietaire} → {wallet1.nom_proprietaire}")
        print(f"Solde disponible: {wallet2.solde} BKN")
        montant = float(input("Montant à transférer: "))
        resultat = wallet2.envoyer(montant, wallet1)
        print(resultat)
        transaction_id = f"TXN-BKN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100,999)}"
        print(f"Transaction: {transaction_id}")
        print("📊 Nouveaux soldes:")
        print(f"{wallet2.nom_proprietaire} : {wallet2.solde} BKN")
        print(f"{wallet1.nom_proprietaire} : {wallet1.solde} BKN")

    elif reponse == 4:
        historique_wallet1 = wallet1.consulter_historique()
        print(f"\nHistorique de {wallet1.nom_proprietaire}: ")
        for transaction in historique_wallet1:
            print(transaction)

    elif reponse == 5:
        historique_wallet2 = wallet2.consulter_historique()
        print(f"\nHistorique de {wallet2.nom_proprietaire}: ")
        for transaction in historique_wallet2:
            print(transaction)

