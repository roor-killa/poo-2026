from wallet import Wallet

def main():
    w1 = Wallet("ADDR1", "Alice", 1000)
    w2 = Wallet("ADDR2", "Bob", 500)

    while True:
        print("\n💎 TRANSFERT LOCAL BKN")
        print("1. Afficher wallets")
        print("2. Alice → Bob")
        print("3. Bob → Alice")
        print("4. Historique Alice")
        print("5. Historique Bob")
        print("0. Quitter")

        choix = input("👉 Choix: ")

        try:
            if choix == "1":
                w1.show_info()
                w2.show_info()

            elif choix == "2":
                amount = float(input("Montant: "))
                tx = w1.send(amount, w2)
                print(f"✅ TX: {tx}")

            elif choix == "3":
                amount = float(input("Montant: "))
                tx = w2.send(amount, w1)
                print(f"✅ TX: {tx}")

            elif choix == "4":
                w1.show_history()

            elif choix == "5":
                w2.show_history()

            elif choix == "0":
                break

        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()