from wallet import Wallet

def main():
    w1 = Wallet("Alice", 1000)
    w2 = Wallet("Bob", 500)

    while True:
        print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
        print("1. Afficher les wallets")
        print("2. Transférer BKN (Wallet1 → Wallet2)")
        print("3. Transférer BKN (Wallet2 → Wallet1)")
        print("4. Historique Wallet1")
        print("5. Historique Wallet2")
        print("0. Quitter")

        choice = input("\n👉 Votre choix: ")

        try:
            if choice == "1":
                w1.show_info()
                w2.show_info()

            elif choice == "2":
                print(f"\n💸 Transfert: {w1.owner} → {w2.owner}")
                print(f"Solde disponible: {w1.balance:.2f} BKN")

                amount = float(input("Montant à transférer: "))
                confirm = input("Confirmer (o/n): ")

                if confirm != "o":
                    print("❌ Annulé")
                    continue

                txn = w1.send(amount, w2)

                print(f"\n✅ Transfert de {amount} BKN réussi")
                print(f"   Transaction: {txn}")

                print("\n📊 Nouveaux soldes:")
                print(f"   {w1.owner}: {w1.balance:.2f} BKN")
                print(f"   {w2.owner}: {w2.balance:.2f} BKN")

            elif choice == "3":
                print(f"\n💸 Transfert: {w2.owner} → {w1.owner}")
                print(f"Solde disponible: {w2.balance:.2f} BKN")

                amount = float(input("Montant à transférer: "))
                confirm = input("Confirmer (o/n): ")

                if confirm != "o":
                    print("❌ Annulé")
                    continue

                txn = w2.send(amount, w1)

                print(f"\n✅ Transfert de {amount} BKN réussi")
                print(f"   Transaction: {txn}")

                print("\n📊 Nouveaux soldes:")
                print(f"   {w2.owner}: {w2.balance:.2f} BKN")
                print(f"   {w1.owner}: {w1.balance:.2f} BKN")

            elif choice == "4":
                w1.show_history()

            elif choice == "5":
                w2.show_history()

            elif choice == "0":
                break

        except Exception as e:
            print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main()