"""
local_transfer.py - Système de transfert BKN en mode local (Partie 1)

Permet de transférer des BKN entre deux wallets sur le même terminal.
"""

from wallet import Wallet


# ──────────────────────────────────────────────────────────────
# Helpers d'affichage
# ──────────────────────────────────────────────────────────────

def print_header():
    print("\n" + "═" * 50)
    print("  💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL")
    print("═" * 50)


def print_menu():
    print("\n┌─────────────────────────────────────────┐")
    print("│           MENU PRINCIPAL                │")
    print("├─────────────────────────────────────────┤")
    print("│  1. Afficher les wallets                │")
    print("│  2. Transférer BKN (Wallet1 → Wallet2)  │")
    print("│  3. Transférer BKN (Wallet2 → Wallet1)  │")
    print("│  4. Historique Wallet1                  │")
    print("│  5. Historique Wallet2                  │")
    print("│  0. Quitter                             │")
    print("└─────────────────────────────────────────┘")


def print_wallets(w1: Wallet, w2: Wallet):
    print("\n" + "─" * 50)
    print(w1)
    print("─" * 50)
    print(w2)
    print("─" * 50)


def saisir_montant(prompt: str) -> float:
    """Lit un montant valide depuis l'entrée standard."""
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"'{raw}' n'est pas un montant valide.")


def effectuer_transfert(expediteur: Wallet, destinataire: Wallet):
    """Gère la saisie et l'exécution d'un transfert entre deux wallets."""
    print(f"\n💸 Transfert : {expediteur.owner} → {destinataire.owner}")
    print(f"   Solde disponible : {expediteur.balance:.2f} BKN")

    try:
        montant = saisir_montant("   Montant à transférer : ")
        tx_id = expediteur.envoyer(montant, destinataire)

        print(f"\n✅ Transfert de {montant:.2f} BKN réussi")
        print(f"   Transaction : {tx_id}")
        print(f"\n📊 Nouveaux soldes :")
        print(f"   {expediteur.owner} : {expediteur.balance:.2f} BKN")
        print(f"   {destinataire.owner} : {destinataire.balance:.2f} BKN")

    except ValueError as e:
        print(f"\n❌ Erreur : {e}")


# ──────────────────────────────────────────────────────────────
# Initialisation des wallets
# ──────────────────────────────────────────────────────────────

def creer_wallets() -> tuple[Wallet, Wallet]:
    """Crée les deux wallets avec saisie interactive."""
    print("\n🔧 Configuration des wallets\n")

    print("── Wallet 1 ──")
    nom1 = input("Nom du propriétaire (Enter = Alice) : ").strip() or "Alice"
    while True:
        try:
            solde1 = float(input(f"Solde initial de {nom1} (BKN, Enter = 1000) : ").strip() or "1000")
            if solde1 < 0:
                print("   ⚠️  Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("   ⚠️  Valeur invalide, réessayez.")

    print("\n── Wallet 2 ──")
    nom2 = input("Nom du propriétaire (Enter = Bob) : ").strip() or "Bob"
    while True:
        try:
            solde2 = float(input(f"Solde initial de {nom2} (BKN, Enter = 500) : ").strip() or "500")
            if solde2 < 0:
                print("   ⚠️  Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("   ⚠️  Valeur invalide, réessayez.")

    w1 = Wallet(nom1, solde1, prefix="BKN-LOCAL")
    w2 = Wallet(nom2, solde2, prefix="BKN-LOCAL")

    print(f"\n✅ Wallets créés avec succès !")
    print(f"   {w1.owner} : {w1.address}  |  {w1.balance:.2f} BKN")
    print(f"   {w2.owner} : {w2.address}  |  {w2.balance:.2f} BKN")

    return w1, w2


# ──────────────────────────────────────────────────────────────
# Boucle principale
# ──────────────────────────────────────────────────────────────

def main():
    print_header()
    wallet1, wallet2 = creer_wallets()

    while True:
        print_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            print_wallets(wallet1, wallet2)

        elif choix == "2":
            effectuer_transfert(wallet1, wallet2)

        elif choix == "3":
            effectuer_transfert(wallet2, wallet1)

        elif choix == "4":
            wallet1.afficher_historique()

        elif choix == "5":
            wallet2.afficher_historique()

        elif choix == "0":
            print("\n👋 Au revoir ! À bientôt sur BKN ! 💎\n")
            break

        else:
            print("\n⚠️  Choix invalide. Veuillez entrer un chiffre entre 0 et 5.")


if __name__ == "__main__":
    main()
