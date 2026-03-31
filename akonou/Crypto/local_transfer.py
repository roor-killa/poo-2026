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

import sys

from wallet import Wallet, InsufficientFundsError, InvalidAmountError
from transfer_strategies import LocalTransferStrategy

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def afficher_wallets(w1: Wallet, w2: Wallet) -> None:
    """Affiche les informations des deux wallets."""
    w1.display_info()
    w2.display_info()


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

    try:
        montant = float(input("Montant à transférer (BKN) : ").strip())
    except ValueError:
        print("❌ Montant invalide.")
        return

    try:
        strategy = LocalTransferStrategy()
        result = strategy.transfer(expediteur, montant, recipient=destinataire)
        print(f"\n✅ Transfert de {montant:.1f} BKN réussi")
        print(f"   Transaction : {result['transaction_id']}")
        print("\n📊 Nouveaux soldes :")
        print(f"   {expediteur.owner} : {result['sender_balance']:.2f} BKN")
        print(f"   {destinataire.owner} : {result['recipient_balance']:.2f} BKN")
    except (InsufficientFundsError, InvalidAmountError) as e:
        print(f"❌ {e}")


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
    wallet1 = Wallet(owner="Alice", initial_balance=1000, prefix="LOCAL")
    wallet2 = Wallet(owner="Bob", initial_balance=500, prefix="LOCAL")

    print("\n✅ Wallets créés avec succès !")
    afficher_wallets(wallet1, wallet2)

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            afficher_wallets(wallet1, wallet2)

        elif choix == "2":
            effectuer_transfert(wallet1, wallet2)

        elif choix == "3":
            effectuer_transfert(wallet2, wallet1)

        elif choix == "4":
            wallet1.display_history()

        elif choix == "5":
            wallet2.display_history()

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
