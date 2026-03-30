from wallet import Wallet


def afficher_menu():
    # affiche le menu principal
    print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
    print("1. afficher les wallets")
    print("2. transférer BKN de wallet1 vers wallet2")
    print("3. transférer BKN de wallet2 vers wallet1")
    print("4. historique wallet1")
    print("5. historique wallet2")
    print("0. quitter")


def afficher_wallets(wallet1: Wallet, wallet2: Wallet):
    # affiche les informations des deux wallets
    print("\n📊 INFORMATIONS DES WALLETS")
    wallet1.show_info()
    print()
    wallet2.show_info()


def effectuer_transfert(source: Wallet, destination: Wallet):
    # affiche les infos avant transfert
    print(f"\n💸 transfert {source.owner} vers {destination.owner}")
    print(f"solde disponible {source.balance:.2f} BKN")

    try:
        # récupère le montant saisi
        montant = float(input("montant à transférer "))
    except ValueError:
        print("❌ montant invalide")
        return

    try:
        # débite le wallet source
        transaction_id = source.send(montant, destination.address)

        # crédite le wallet destination
        destination.receive(montant, source.address)

        print(f"\n✅ transfert de {montant:.2f} BKN réussi")
        print(f"transaction {transaction_id}")

        print("\n📊 nouveaux soldes")
        print(f"{source.owner} {source.balance:.2f} BKN")
        print(f"{destination.owner} {destination.balance:.2f} BKN")

    except ValueError as e:
        print(f"❌ erreur {e}")


def main():
    # crée les deux wallets locaux
    wallet1 = Wallet("Alice", 1000, "LOCAL")
    wallet2 = Wallet("Bob", 500, "LOCAL")

    while True:
        # affiche le menu
        afficher_menu()

        # récupère le choix utilisateur
        choix = input("👉 votre choix ").strip()

        if choix == "1":
            afficher_wallets(wallet1, wallet2)

        elif choix == "2":
            effectuer_transfert(wallet1, wallet2)

        elif choix == "3":
            effectuer_transfert(wallet2, wallet1)

        elif choix == "4":
            wallet1.show_history()

        elif choix == "5":
            wallet2.show_history()

        elif choix == "0":
            print("👋 fermeture du programme")
            break

        else:
            print("❌ choix invalide")


if __name__ == "__main__":
    main()