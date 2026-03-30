

"""
network_client.py — Client de wallet BKN (Partie 2)

TODO : Complétez les sections marquées TODO.

Fonctionnalités attendues :
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

    TODO : Implémenter la fonction.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(TIMEOUT)
        sock.connect((host, port))

        message = json.dumps(payload).encode("utf-8")
        sock.sendall(message)

        raw_response = sock.recv(4096).decode("utf-8")
        return json.loads(raw_response)
    except socket.timeout as exc:
        raise TimeoutError("Le serveur n'a pas répondu dans le délai imparti.") from exc
    finally:
        sock.close()


def action_get_info(host: str, port: int) -> None:
    """
    Récupère et affiche les informations du wallet distant.

    TODO : Appeler send_request avec {"action": "get_info"}
           et afficher le résultat.
    """
    print(f"\n🔍 Récupération des infos du wallet distant ({host}:{port})...")
    # TODO : Appeler send_request et afficher wallet["owner"], wallet["address"], wallet["balance"]
    try:
        response = send_request(host, port, {"action": "get_info"})
        if response.get("status") != "success":
            print(f"❌ Erreur serveur: {response.get('message', 'Réponse invalide')}")
            return

        wallet = response.get("wallet", {})
        print("✅ Wallet distant trouvé:")
        print(f"   Propriétaire : {wallet.get('owner', 'N/A')}")
        print(f"   Adresse      : {wallet.get('address', 'N/A')}")
        print(f"   Solde        : {float(wallet.get('balance', 0.0)):.2f} BKN")
    except ConnectionRefusedError:
        print("❌ Connexion refusée: le serveur n'est pas démarré ou le port est incorrect.")
    except TimeoutError:
        print("❌ Timeout: le serveur n'a pas répondu à temps.")
    except json.JSONDecodeError:
        print("❌ Réponse invalide: le serveur a renvoyé un JSON incorrect.")


def action_transfer(local_wallet: Wallet, host: str, port: int) -> None:
    """
    Demande un montant, débite le wallet local, et crédite le wallet distant.

    Étapes :
      1. Récupérer les infos du wallet distant (get_info) pour afficher l'adresse
      2. Demander le montant à l'utilisateur
      3. Vérifier que le solde local est suffisant
      4. Envoyer la requête "receive" au serveur
      5. Si succès → débiter le wallet local avec wallet.receive() en sens inverse
         (ou directement soustraire le solde — voir TODO ci-dessous)
      6. Afficher les nouveaux soldes

    TODO : Implémenter les étapes ci-dessus.
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

    # TODO : Étape 1 — get_info pour récupérer l'adresse distante
    # TODO : Étape 2 — Vérifier amount > 0 et amount <= local_wallet.balance
    # TODO : Étape 3 — send_request avec {"action": "receive", "amount": amount, "from_address": local_wallet.address}
    # TODO : Étape 4 — Si réponse "success", débiter local_wallet
    #                  (utiliser wallet.balance -= amount directement OU créer une méthode dédiée)
    # TODO : Afficher transaction_id et nouveaux soldes
    try:
        info_resp = send_request(host, port, {"action": "get_info"})
        if info_resp.get("status") != "success":
            print(f"❌ Erreur serveur: {info_resp.get('message', 'Réponse invalide')}")
            return

        distant_wallet = info_resp.get("wallet", {})
        distant_address = distant_wallet.get("address", "UNKNOWN")
        print(f"   Adresse distante : {distant_address}")

        if amount <= 0:
            raise InvalidAmountError("Le montant doit être strictement positif.")
        if amount > local_wallet.balance:
            raise InsufficientFundsError(
                f"Solde insuffisant: {local_wallet.balance:.2f} BKN disponibles."
            )

        transfer_resp = send_request(
            host,
            port,
            {
                "action": "receive",
                "amount": amount,
                "from_address": local_wallet.address,
            },
        )

        if transfer_resp.get("status") != "success":
            print(f"❌ Transfert refusé par le serveur: {transfer_resp.get('message', 'Erreur inconnue')}")
            return

        local_wallet.balance -= amount

        tx_id = transfer_resp.get("transaction_id", "N/A")
        distant_balance = float(transfer_resp.get("new_balance", 0.0))
        print("✅ Transfert effectué")
        print(f"   Transaction : {tx_id}")
        print(f"   Votre nouveau solde : {local_wallet.balance:.2f} BKN")
        print(f"   Solde distant       : {distant_balance:.2f} BKN")
    except (InvalidAmountError, InsufficientFundsError) as exc:
        print(f"❌ {exc}")
    except ConnectionRefusedError:
        print("❌ Connexion refusée: le serveur n'est pas démarré ou le port est incorrect.")
    except TimeoutError:
        print("❌ Timeout: le serveur n'a pas répondu à temps.")
    except json.JSONDecodeError:
        print("❌ Réponse invalide: le serveur a renvoyé un JSON incorrect.")


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

    # Hôte et port par défaut pour les connexions sortantes
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
            # TODO : Demander host/port et appeler action_get_info()
            host_input = input(f"Host (Entrée = {default_host}) : ").strip()
            host = host_input or default_host
            try:
                port_input = input(f"Port (Entrée = {default_port}) : ").strip()
                port = int(port_input) if port_input else default_port
            except ValueError:
                print("Port invalide, utilisation du port par défaut.")
                port = default_port
            action_get_info(host, port)

        elif choix == "4":
            # TODO : Appeler action_transfer(wallet, default_host, default_port)
            action_transfer(wallet, default_host, default_port)

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()