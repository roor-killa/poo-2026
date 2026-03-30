"""
local_transfer.py — Transferts locaux BKN (Partie 1)

TODO : Complétez les sections marquées TODO pour rendre le programme fonctionnel.

Fonctionnalités attendues :
  1. Créer deux wallets avec des soldes initiaux
  2. Afficher un menu interactif
  3. Transférer des BKN dans les deux sens
  4. Afficher l'historique des transactions
  5. Gérer les erreurs (solde insuffisant, montant invalide)
"""

from wallet import Wallet, InsufficientFundsError, InvalidAmountError


def afficher_wallets(w1: Wallet, w2: Wallet) -> None:
    """Affiche les informations des deux wallets."""
    # TODO : Appeler display_info() sur chaque wallet
    pass


def effectuer_transfert(expediteur: Wallet, destinataire: Wallet) -> None:
    """
    Demande un montant à l'utilisateur et effectue le transfert
    de `expediteur` vers `destinataire`.

    Gérez les cas d'erreur :
      - montant invalide (texte saisi, valeur <= 0)
      - solde insuffisant
    """
    print(f"\n💸 Transfert : {expediteur.owner} → {destinataire.owner}")
    print(f"   Solde disponible : {expediteur.balance:.2f} BKN")

    # TODO : Demander le montant avec input()
    # TODO : Convertir en float et gérer ValueError
    # TODO : Appeler expediteur.send(montant, destinataire)
    # TODO : Afficher le résultat (tx_id, nouveaux soldes)
    # TODO : Capturer InsufficientFundsError et InvalidAmountError
    pass


def afficher_menu() -> None:
    print("\n💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
    print("1. Afficher les wallets")
    print("2. Transférer BKN (Wallet1 → Wallet2)")
    print("3. Transférer BKN (Wallet2 → Wallet1)")
    print("4. Historique Wallet1")
    print("5. Historique Wallet2")
    print("0. Quitter")


def main() -> None:
    # ------------------------------------------------------------------ #
    # TODO : Créer les deux wallets                                       #
    #   - wallet1 : propriétaire "Alice", solde initial 1000, prefix "LOCAL"
    #   - wallet2 : propriétaire "Bob",   solde initial 500,  prefix "LOCAL"
    # ------------------------------------------------------------------ #
    wallet1 = None  # À remplacer
    wallet2 = None  # À remplacer

    print("\n✅ Wallets créés avec succès !")
    afficher_wallets(wallet1, wallet2)

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            afficher_wallets(wallet1, wallet2)

        elif choix == "2":
            # TODO : Appeler effectuer_transfert(wallet1, wallet2)
            pass

        elif choix == "3":
            # TODO : Appeler effectuer_transfert(wallet2, wallet1)
            pass

        elif choix == "4":
            # TODO : Afficher l'historique de wallet1
            pass

        elif choix == "5":
            # TODO : Afficher l'historique de wallet2
            pass

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
