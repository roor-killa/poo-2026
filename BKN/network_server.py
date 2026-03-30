import socket
import json
import threading
from wallet import Wallet

wallet = None

def handle_client(conn):
    global wallet
    try:
        data = json.loads(conn.recv(1024).decode())

        if data["action"] == "get_info":
            response = {
                "status": "success",
                "wallet": {
                    "address": wallet.address,
                    "owner": wallet.owner,
                    "balance": wallet.balance
                }
            }

        elif data["action"] == "receive":
            amount = data["amount"]
            sender = data["from_address"]

            txn = wallet.receive(amount, sender)

            print(f"\n💸 Réception de {amount} BKN depuis {sender}")

            response = {
                "status": "success",
                "transaction_id": txn,
                "new_balance": wallet.balance
            }

        conn.send(json.dumps(response).encode())

    except Exception as e:
        conn.send(json.dumps({"status": "error", "message": str(e)}).encode())

    finally:
        conn.close()


def console():
    global wallet
    while True:
        cmd = input("\n[Serveur] > ")

        if cmd == "info":
            wallet.show_info()

        elif cmd == "hist":
            wallet.show_history()

        elif cmd == "send":
            host = input("Host client (Enter = localhost): ") or "localhost"
            port = int(input("Port client (Enter = 6000): ") or 6000)

            amount = float(input("Montant: "))
            confirm = input("Confirmer (o/n): ")

            if confirm != "o":
                continue

            try:
                s = socket.socket()
                s.connect((host, port))

                s.send(json.dumps({
                    "action": "receive",
                    "amount": amount,
                    "from_address": wallet.address
                }).encode())

                res = json.loads(s.recv(1024).decode())
                s.close()

                if res["status"] == "success":
                    wallet.balance -= amount
                    print("✅ Transfert serveur → client réussi")

            except Exception as e:
                print("❌ Erreur:", e)


def main():
    global wallet

    print("🌐 SERVEUR DE WALLET BKN")

    owner = input("Nom du propriétaire du wallet: ")
    balance = float(input("Solde initial (BKN): "))

    host = input("Host (Enter = localhost): ") or "localhost"
    port = int(input("Port (Enter = 5555): ") or 5555)

    wallet = Wallet(owner, balance, "BKN-SERVER")

    server = socket.socket()
    server.bind((host, port))
    server.listen()

    print(f"\n🌐 Serveur BKN démarré sur {host}:{port}")
    print(f"🏦 Wallet: {wallet.owner}")
    print(f"💰 Solde initial: {wallet.balance:.2f} BKN")
    print("En attente de connexions...")

    threading.Thread(target=console, daemon=True).start()

    while True:
        conn, addr = server.accept()
        print(f"\n🔗 Connexion de {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    main()