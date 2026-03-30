import socket
import json
import threading
import uuid
from wallet import Wallet

running = True

# ==============================
# Gérer client entrant
# ==============================
def handle_client(conn, wallet):
    try:
        data = conn.recv(4096).decode()
        req = json.loads(data)

        if req["action"] == "get_info":
            res = {
                "status": "success",
                "wallet": {
                    "address": wallet.address,
                    "owner": wallet.owner,
                    "balance": wallet.balance
                }
            }

        elif req["action"] == "receive":
            amount = req["amount"]
            from_addr = req["from_address"]

            tx_id = wallet._generate_tx_id()
            wallet.receive(amount, from_addr, tx_id)

            res = {
                "status": "success",
                "transaction_id": tx_id,
                "new_balance": wallet.balance
            }

        else:
            res = {"status": "error", "msg": "Action inconnue"}

        conn.send(json.dumps(res).encode())

    except Exception as e:
        conn.send(json.dumps({"status": "error", "msg": str(e)}).encode())

    finally:
        conn.close()

# Console serveur
def console(wallet, server):
    global running

    while running:
        print("\n MENU SERVEUR")
        print("1. Info")
        print("2. Historique")
        print("0. Quitter")

        choix = input("👉 Choix: ")

        if choix == "1":
            wallet.show_info()

        elif choix == "2":
            wallet.show_history()

        elif choix == "0":
            print("🛑 Arrêt serveur...")
            running = False
            server.close()
            break

        else:
            print("❌ Choix invalide")


def main():
    print("🌐 SERVEUR BKN")

    owner = input("Nom: ")
    balance = float(input("Solde: "))
    host = input("Host (Enter=localhost): ") or "localhost"
    port = int(input("Port (Enter=5555): ") or 5555)

    address = f"BKN-SERVER-{owner.upper()}-{str(uuid.uuid4())[:3]}"
    wallet = Wallet(address, owner, balance)

    server = socket.socket()
    server.bind((host, port))
    server.listen(5)

    print(f"\n🌐 Serveur lancé sur {host}:{port}")
    print("En attente de connexions...")

    threading.Thread(target=console, args=(wallet, server), daemon=True).start()

    while running:
        try:
            conn, _ = server.accept()
            threading.Thread(target=handle_client, args=(conn, wallet)).start()
        except:
            break


if __name__ == "__main__":
    main()