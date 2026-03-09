from wallet import Wallet


def afficher_wallets(wallet1, wallet2):
    print("\n📊 État des Wallets")
    print("---------------------------")
    print(f"{wallet1.owner} ({wallet1.address}) : {wallet1.balance:.2f} BKN")
    print(f"{wallet2.owner} ({wallet2.address}) : {wallet2.balance:.2f} BKN")
    print("---------------------------")


def transferer(source, destination):

    try:
        print(f"\n💸 Transfert: {source.owner} → {destination.owner}")
        print(f"Solde disponible: {source.balance:.2f} BKN")

        montant = float(input("Montant à transférer: "))

        txn_id = source.send(montant, destination.address)
        destination.receive(montant, source.address)

        print("\n✅ Transfert réussi !")
        print(f"Transaction ID: {txn_id}")

        print("\n📊 Nouveaux soldes:")
        print(f"{source.owner}: {source.balance:.2f} BKN")
        print(f"{destination.owner}: {destination.balance:.2f} BKN")

    except ValueError as e:
        print(f"\n❌ Erreur: {e}")

    except Exception as e:
        print(f"\n⚠️ Problème inattendu: {e}")


def afficher_historique(wallet):

    print(f"\n📜 Historique des transactions de {wallet.owner}")
    print("-------------------------------------")

    if not wallet.history:
        print("Aucune transaction.")

    else:
        for txn in wallet.history:
            print(
                f"{txn['date']} | {txn['type']} | {txn['amount']} BKN | TXN: {txn['id']}"
            )


def menu():

    # création des wallets
    wallet1 = Wallet("Alice", 1000)
    wallet2 = Wallet("Bob", 500)

    while True:

        print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
        print("1️⃣  Afficher les wallets")
        print("2️⃣  Transférer BKN (Alice → Bob)")
        print("3️⃣  Transférer BKN (Bob → Alice)")
        print("4️⃣  Historique Alice")
        print("5️⃣  Historique Bob")
        print("0️⃣  Quitter")

        choix = input("\n👉 Votre choix: ")

        if choix == "1":
            afficher_wallets(wallet1, wallet2)

        elif choix == "2":
            transferer(wallet1, wallet2)

        elif choix == "3":
            transferer(wallet2, wallet1)

        elif choix == "4":
            afficher_historique(wallet1)

        elif choix == "5":
            afficher_historique(wallet2)

        elif choix == "0":
            print("\n👋 Merci d'avoir utilisé le système BKN")
            break

        else:
            print("\n❌ Choix invalide")


if __name__ == "__main__":
    menu()
