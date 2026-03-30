from wallet import Wallet, InsufficientFundsError, InvalidAmountError

def main():
    # création de deux portefeuilles avec des soldes initiaux
    wallet1 = Wallet("Alice", 1000.0)
    wallet2 = Wallet("Bob", 500.0)

    # boucle du menu interactif
    while True:
        print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
        print("1. Afficher les wallets")
        print("2. Transférer BKN (Wallet1 → Wallet2)")
        print("3. Transférer BKN (Wallet2 → Wallet1)")
        print("4. Historique Wallet1")
        print("5. Historique Wallet2")
        print("0. Quitter")

        choix = input("\n👉 Votre choix: ")

        if choix == "1":
            wallet1.display_info()
            wallet2.display_info()

        elif choix == "2":
            print(f"\n💸 Transfert: {wallet1.owner} → {wallet2.owner}")
            print(f"Solde disponible: {wallet1.balance:.2f} BKN")
            montant_str = input("Montant à transférer (BKN): ")
            
            try:
                montant = float(montant_str)
                tx_id = wallet1.send(montant, wallet2)
                print(f"✅ Transfert de {montant} BKN réussi !")
                print(f"   Transaction: {tx_id}")
            except ValueError:
                print("❌ Erreur : Veuillez entrer un nombre valide.")
            except (InvalidAmountError, InsufficientFundsError) as e:
                print(f"❌ Erreur : {e}")

        elif choix == "3":
            print(f"\n💸 Transfert: {wallet2.owner} → {wallet1.owner}")
            print(f"Solde disponible: {wallet2.balance:.2f} BKN")
            montant_str = input("Montant à transférer (BKN): ")
            
            try:
                montant = float(montant_str)
                tx_id = wallet2.send(montant, wallet1)
                print(f"✅ Transfert de {montant} BKN réussi !")
                print(f"   Transaction: {tx_id}")
            except ValueError:
                print("❌ Erreur : Veuillez entrer un nombre valide.")
            except (InvalidAmountError, InsufficientFundsError) as e:
                print(f"❌ Erreur : {e}")

        elif choix == "4":
            wallet1.display_history()

        elif choix == "5":
            wallet2.display_history()

        elif choix == "0":
            print("Au revoir ! 👋")
            break
            
        else:
            print("⚠️ Option en construction ou invalide...")

# cette ligne permet de lancer la fonction main() quand on exécute le fichier
if __name__ == "__main__":
    main()