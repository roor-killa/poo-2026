"""
network_client.py — Client de wallet BKN (Partie 2)

Fonctionnalités :
  1. Créer un wallet local
  2. Se connecter à un serveur distant
  3. Envoyer une requête JSON "get_info" pour récupérer les infos distantes
  4. Envoyer une requête JSON "receive" pour créditer le wallet distant
     et débiter le wallet local
  5. Gérer les erreurs réseau (timeout, connexion refusée)
"""

import socket
import json

from wallet import Wallet, InsufficientFundsError, InvalidAmountError

TIMEOUT = 10  # secondes


def send_request(host: str, port: int, payload: dict) -> dict:
    """
    Ouvre une connexion TCP vers (host, port), envoie `payload` en JSON
    et retourne la réponse JSON désérialisée.

    Raises
    ------
    ConnectionRefusedError
        Si le serveur n'est pas démarré.
    TimeoutError
        Si le serveur ne répond pas dans le délai imparti.
    json.JSONDecodeError
        Si la réponse n'est pas du JSON valide.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(payload).encode("utf-8"))
        raw = sock.recv(4096).decode("utf-8")
        return json.loads(raw)
    finally:
        sock.close()


def action_get_info(host: str, port: int) -> dict | None:
    """
    Récupère et affiche les informations du wallet distant.
    Retourne le dict wallet ou None en cas d'erreur.
    """
    print(f"\n🔍 Récupération des infos du wallet distant ({host}:{port})...")
    try:
        response = send_request(host, port, {"action": "get_info"})
        if response.get("status") == "success":
            w = response["wallet"]
            print(f"🏦 Wallet distant : {w['owner']}")
            print(f"   Adresse : {w['address']}")
            print(f"   Solde   : {w['balance']:.2f} BKN")
            return w
        else:
            print(f"❌ Erreur serveur : {response.get('message')}")
            return None
    except ConnectionRefusedError:
        print(f"❌ Connexion refusée — le serveur {host}:{port} n'est pas accessible.")
        return None
    except TimeoutError:
        print("❌ Timeout — le serveur ne répond pas.")
        return None
    except json.JSONDecodeError:
        print("❌ Réponse invalide reçue du serveur.")
        return None


def action_transfer(local_wallet: Wallet, host: str, port: int) -> None:
    """
    Demande un montant, débite le wallet local, et crédite le wallet distant.
    """
    print(f"\n💸 Transfert de BKN vers un wallet distant")
    print(f"   Votre solde : {local_wallet.balance:.2f} BKN")

    host_input = input("Host du serveur destinataire (Entrée = localhost) : ").strip()
    if host_input:
        host = host_input

    try:
        port_input = input(f"Port (Entrée = {port}) : ").strip()
        if port_input:
            port = int(port_input)
    except ValueError:
        print("Port invalide, utilisation du port par défaut.")

    try:
        amount = float(input("Montant à transférer (BKN) : ").strip())
    except ValueError:
        print("❌ Montant invalide.")
        return

    # Étape 1 — Récupérer l'adresse distante
    print(f"\n💸 Transfert de {amount} BKN en cours...")
    print(f"🔗 Connexion à {host}:{port}...")
    remote_info = action_get_info(host, port)
    if remote_info is None:
        return
    remote_address = remote_info["address"]
    print("✅ Connecté !")
    print(f"📍 Wallet distant : {remote_address}")

    # Étape 2 — Vérifications locales
    if amount <= 0:
        print("❌ Le montant doit être strictement positif.")
        return
    if amount > local_wallet.balance:
        print(f"❌ Solde insuffisant : {local_wallet.balance:.2f} BKN disponibles.")
        return

    # Étape 3 — Envoyer la requête "receive" au serveur
    try:
        response = send_request(host, port, {
            "action": "receive",
            "amount": amount,
            "from_address": local_wallet.address
        })
    except ConnectionRefusedError:
        print("❌ Connexion refusée pendant le transfert.")
        return
    except TimeoutError:
        print("❌ Timeout pendant le transfert.")
        return

    # Étape 4 — Si succès, débiter le wallet local
    if response.get("status") == "success":
        # Débiter en interne (sans appeler send() car le destinataire est distant)
        local_wallet.balance -= amount
        local_wallet._record_transaction(
            tx_id=response["transaction_id"],
            kind="DEBIT",
            amount=amount,
            counterpart=remote_address
        )
        print("✅ Débit local effectué")
        print("✅ Crédit distant confirmé !")
        print(f"   Transaction ID : {response['transaction_id']}")
        print(f"\n✅ Transfert de {amount:.2f} BKN réussi")
        print(f"\n📊 Nouveaux soldes :")
        print(f"   Votre wallet  : {local_wallet.balance:.2f} BKN")
        print(f"   Wallet distant : {response['new_balance']:.2f} BKN")
    else:
        print(f"❌ Échec du transfert : {response.get('message')}")


def afficher_menu() -> None:
    print("\n💎 CLIENT WALLET BKN")
    print("1. Afficher mon wallet")
    print("2. Afficher l'historique")
    print("3. Obtenir infos d'un wallet distant")
    print("4. Transférer des BKN à un wallet distant")
    print("0. Quitter")


def main() -> None:
    print("🌐 CLIENT DE WALLET BKN")
    owner = input("Votre nom : ").strip() or "Bob"

    try:
        balance = float(input("Solde initial (BKN) : ").strip() or "500")
    except ValueError:
        print("Solde invalide, valeur par défaut : 500")
        balance = 500.0

    wallet = Wallet(owner=owner, initial_balance=balance, prefix="CLIENT")

    print(f"\n✅ Wallet créé !")
    print(f"   Adresse : {wallet.address}")
    print(f"   Solde   : {wallet.balance:.2f} BKN")

    default_host = "localhost"
    default_port = 5555

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            wallet.display_info()

        elif choix == "2":
            wallet.display_history()

        elif choix == "3":
            host_input = input("Host du serveur (Entrée = localhost) : ").strip() or default_host
            try:
                port_input = input(f"Port (Entrée = {default_port}) : ").strip()
                port = int(port_input) if port_input else default_port
            except ValueError:
                port = default_port
            action_get_info(host_input, port)

        elif choix == "4":
            action_transfer(wallet, default_host, default_port)

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()