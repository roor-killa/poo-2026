"""
network_server.py — Serveur de wallet BKN (Partie 2)

TODO : Complétez les sections marquées TODO.

Architecture :
  - Un thread écoute les connexions réseau entrantes
  - Le thread principal gère les commandes locales (info, hist, quit)

Protocole JSON attendu du client :
  {"action": "get_info"}
      → {"status": "success", "wallet": {...}}

  {"action": "receive", "amount": 100.0, "from_address": "BKN-..."}
      → {"status": "success", "message": "...", "transaction_id": "...", "new_balance": ...}
"""

import socket
import threading
import json
import sys

from wallet import Wallet, InvalidAmountError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def handle_client(conn: socket.socket, addr: tuple, wallet: Wallet) -> None:
    """
    Gère une connexion client entrante.

    Reçoit une requête JSON, traite l'action, renvoie une réponse JSON.

    Actions supportées :
      - "get_info"  : retourne les infos du wallet
      - "receive"   : crédite le wallet et confirme

    TODO : Implémenter le traitement des deux actions.
    """
    print(f"\n🔗 Connexion de {addr}")
    try:
        # Réception des données brutes
        data = conn.recv(4096).decode("utf-8")
        if not data:
            return

        request = json.loads(data)

        action = request.get("action")

        if action == "get_info":
            response = {
                "status": "success",
                "wallet": wallet.to_dict(),
            }

        elif action == "receive":
            amount = request.get("amount")
            from_address = request.get("from_address", "UNKNOWN")
            try:
                tx_id = wallet.receive(amount, from_address=from_address)
                response = {
                    "status": "success",
                    "message": f"Réception de {amount} BKN confirmée",
                    "transaction_id": tx_id,
                    "new_balance": wallet.balance,
                }
            except InvalidAmountError as e:
                response = {"status": "error", "message": str(e)}

        else:
            response = {"status": "error", "message": f"Action inconnue : {action}"}

        # TODO : Sérialiser `response` en JSON et l'envoyer via conn.sendall()
        conn.sendall(json.dumps(response).encode("utf-8"))

    except json.JSONDecodeError:
        error_resp = {"status": "error", "message": "JSON invalide"}
        conn.sendall(json.dumps(error_resp).encode("utf-8"))
    except Exception as e:
        print(f"[Erreur handle_client] {e}")
    finally:
        conn.close()


def start_server(wallet: Wallet, host: str, port: int) -> None:
    """
    Lance le serveur TCP et traite les connexions dans des threads séparés.

    TODO : Créer le socket, le configurer (SO_REUSEADDR), le binder,
           l'écouter, et accepter les connexions en boucle.
           Chaque connexion doit être traitée dans un thread daemon.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen()

    print(f"🌐 Serveur BKN démarré sur {host}:{port}")
    print(f"🏦 Wallet : {wallet.owner}")
    print(f"💰 Solde initial : {wallet.balance:.2f} BKN")
    print("En attente de connexions...\n")

    try:
        while True:
            conn, addr = server_sock.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr, wallet),
                daemon=True,
            ).start()
    finally:
        server_sock.close()


def commandes_locales(wallet: Wallet) -> None:
    """
    Boucle de commandes locales (thread principal).

    Commandes :
      info  → affiche les infos du wallet
      hist  → affiche l'historique
      quit  → arrête le serveur
    """
    print("Commandes locales : info | hist | quit")
    while True:
        cmd = input("[Serveur] > ").strip().lower()
        if cmd == "info":
            wallet.display_info()
        elif cmd == "hist":
            wallet.display_history()
        elif cmd == "quit":
            print("🛑 Arrêt du serveur.")
            break
        else:
            print("Commandes disponibles : info | hist | quit")


def main() -> None:
    print("🌐 SERVEUR DE WALLET BKN")
    owner = input("Nom du propriétaire du wallet : ").strip() or "Alice"

    try:
        balance = float(input("Solde initial (BKN) : ").strip() or "1000")
    except ValueError:
        print("Solde invalide, valeur par défaut : 1000")
        balance = 1000.0

    host = input("Host (Entrée = localhost) : ").strip() or "localhost"

    try:
        port = int(input("Port (Entrée = 5555) : ").strip() or "5555")
    except ValueError:
        print("Port invalide, valeur par défaut : 5555")
        port = 5555

    wallet = Wallet(owner=owner, initial_balance=balance, prefix="SERVER")

    # Lancement du serveur dans un thread daemon
    server_thread = threading.Thread(
        target=start_server, args=(wallet, host, port), daemon=True
    )
    server_thread.start()

    # Commandes locales dans le thread principal
    commandes_locales(wallet)


if __name__ == "__main__":
    main()
