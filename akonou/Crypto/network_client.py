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
import sys

from wallet import Wallet, InsufficientFundsError, InvalidAmountError
from transfer_strategies import NetworkTransferStrategy

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

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
        sock.sendall(json.dumps(payload).encode("utf-8"))
        response_data = sock.recv(4096).decode("utf-8")
        return json.loads(response_data)
    except socket.timeout as e:
        raise TimeoutError(f"Timeout de connexion/réponse vers {host}:{port}") from e
    finally:
        sock.close()


def action_get_info(host: str, port: int) -> None:
    """
    Récupère et affiche les informations du wallet distant.

    TODO : Appeler send_request avec {"action": "get_info"}
           et afficher le résultat.
    """
    print(f"\n🔍 Récupération des infos du wallet distant ({host}:{port})...")
    try:
        response = send_request(host, port, {"action": "get_info"})
        if response.get("status") != "success":
            print(f"❌ Erreur serveur : {response.get('message', 'inconnue')}")
            return

        wallet_info = response.get("wallet", {})
        print("✅ Infos reçues :")
        print(f"   Propriétaire : {wallet_info.get('owner', 'N/A')}")
        print(f"   Adresse      : {wallet_info.get('address', 'N/A')}")
        print(f"   Solde        : {wallet_info.get('balance', 0):.2f} BKN")
    except ConnectionRefusedError:
        print("❌ Connexion refusée : serveur indisponible.")
    except TimeoutError as e:
        print(f"❌ {e}")
    except json.JSONDecodeError:
        print("❌ Réponse serveur invalide (JSON).")


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

    try:
        strategy = NetworkTransferStrategy(send_request)
        result = strategy.transfer(local_wallet, amount, host=host, port=port)
        print(f"📍 Wallet distant : {result['remote_address']}")
        print("✅ Crédit distant confirmé !")
        print(f"   Transaction ID : {result['transaction_id']}")
        print("\n✅ Transfert réussi")
        print("\n📊 Nouveaux soldes :")
        print(f"   Votre wallet : {result['sender_balance']:.2f} BKN")
        print(f"   Wallet distant : {result['remote_balance']:.2f} BKN")

    except (InsufficientFundsError, InvalidAmountError) as e:
        print(f"❌ {e}")
    except RuntimeError as e:
        print(f"❌ Erreur serveur : {e}")
    except ConnectionRefusedError:
        print("❌ Connexion refusée : serveur indisponible.")
    except TimeoutError as e:
        print(f"❌ {e}")
    except json.JSONDecodeError:
        print("❌ Réponse serveur invalide (JSON).")


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
            host = input(f"Host (Entrée = {default_host}) : ").strip() or default_host
            try:
                port_input = input(f"Port (Entrée = {default_port}) : ").strip()
                port = int(port_input) if port_input else default_port
            except ValueError:
                print("Port invalide, utilisation du port par défaut.")
                port = default_port

            action_get_info(host, port)

        elif choix == "4":
            action_transfer(wallet, default_host, default_port)

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
