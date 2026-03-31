import socket
import json
import threading
from wallet import Wallet


def handle_client(conn, wallet):

    data = conn.recv(4096).decode()

    if not data:
        return

    request = json.loads(data)

    action = request.get("action")

    # obtenir les infos du wallet
    if action == "get_info":

        response = {
            "status": "success",
            "wallet": wallet.get_info()
        }

    # recevoir des BKN
    elif action == "receive":

        amount = request.get("amount")
        from_address = request.get("from_address")

        try:
            txn_id = wallet.receive(amount, from_address)

            response = {
                "status": "success",
                "message": f"Réception de {amount} BKN confirmée",
                "transaction_id": txn_id,
                "new_balance": wallet.balance
            }

        except Exception as e:

            response = {
                "status": "error",
                "message": str(e)
            }

    else:

        response = {
            "status": "error",
            "message": "Action inconnue"
        }

    conn.send(json.dumps(response).encode())


def start_server():

    print("\n🌐 SERVEUR DE WALLET BKN")

    owner = input("Nom du propriétaire du wallet: ")
    balance = float(input("Solde initial (BKN): "))

    host = input("Host (Enter = localhost): ") or "localhost"
    port_input = input("Port (Enter = 5555): ")
    port = int(port_input) if port_input else 5555

    wallet = Wallet(owner, balance, "BKN-SERVER")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"\n🌐 Serveur BKN démarré sur {host}:{port}")
    print(f"🏦 Wallet: {wallet.owner}")
    print(f"💰 Solde initial: {wallet.balance:.2f} BKN")
    print("En attente de connexions...\n")

    def accept_clients():
        while True:
            try:
                conn, addr = server.accept()
                print(f"🔗 Connexion reçue de {addr}")
                handle_client(conn, wallet)
                conn.close()
            except OSError:
                break

    thread = threading.Thread(target=accept_clients, daemon=True)
    thread.start()

    # Commandes locales
    print("Commandes locales : info | hist | quit\n")

    while True:
        cmd = input("[Serveur] > ").strip().lower()

        if cmd == "info":
            info = wallet.get_info()
            print(f"\n🏦 WALLET BKN - {info['owner']}")
            print(f"Adresse: {info['address']}")
            print(f"Solde: {info['balance']:.2f} BKN\n")

        elif cmd == "hist":
            if not wallet.history:
                print("Aucune transaction.\n")
            else:
                for txn in wallet.history:
                    print(f"{txn['date']} | {txn['type']} | {txn['amount']} BKN | {txn['id']}")
                print()

        elif cmd == "quit":
            print("👋 Fermeture du serveur")
            server.close()
            break

        else:
            print("Commandes : info | hist | quit")


if __name__ == "__main__":
    start_server()
