from wallet import Wallet


def afficher_menu():
    """Affiche le menu principal."""
    print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
    print("1. Afficher les wallets")
    print("2. Transférer BKN (Wallet1 → Wallet2)")
    print("3. Transférer BKN (Wallet2 → Wallet1)")
    print("4. Historique Wallet1")
    print("5. Historique Wallet2")
    print("0. Quitter")


def effectuer_transfert(expediteur: Wallet, destinataire: Wallet):
    """Gère le transfert de BKN entre deux wallets."""
    print(f"\n💸 Transfert : {expediteur.proprietaire} → {destinataire.proprietaire}")
    print(f"   Solde disponible : {expediteur.solde:.2f} BKN")

    try:
        saisie = input("   Montant à transférer : ").strip()
        montant = float(saisie)

        tx_id = expediteur.envoyer(destinataire, montant)

        print(f"\n✅ Transfert de {montant:.2f} BKN réussi !")
        print(f"   Transaction : {tx_id}")
        print(f"\n📊 Nouveaux soldes :")
        print(f"   {expediteur.proprietaire} : {expediteur.solde:.2f} BKN")
        print(f"   {destinataire.proprietaire} : {destinataire.solde:.2f} BKN")

    except ValueError as e:
        # Gestion des erreurs : solde insuffisant, montant invalide
        print(f"\n❌ Erreur : {e}")


def main():
    print("\n🚀 Bienvenue dans le système BKN - Mode Local")

    # Création des deux wallets avec soldes initiaux
    wallet1 = Wallet("Alice", solde_initial=1000.0, prefix="BKN")
    wallet2 = Wallet("Bob", solde_initial=500.0, prefix="BKN")

    print("\n✅ Wallets créés avec succès !")
    wallet1.afficher_info()
    wallet2.afficher_info()

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            # Affichage des deux wallets
            wallet1.afficher_info()
            wallet2.afficher_info()

        elif choix == "2":
            # Transfert de Wallet1 vers Wallet2
            effectuer_transfert(wallet1, wallet2)

        elif choix == "3":
            # Transfert de Wallet2 vers Wallet1
            effectuer_transfert(wallet2, wallet1)

        elif choix == "4":
            # Historique du premier wallet
            wallet1.afficher_historique()

        elif choix == "5":
            # Historique du second wallet
            wallet2.afficher_historique()

        elif choix == "0":
            print("\n👋 Au revoir ! Vos BKN sont en sécurité.")
            break

        else:
            print("❌ Choix invalide. Veuillez entrer un numéro entre 0 et 5.")


if __name__ == "__main__":
    main()
