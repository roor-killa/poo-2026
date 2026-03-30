import socket
import json
import threading
from wallet import Wallet

def start_client_server(wallet):
    server = socket.socket()
    server.bind(("localhost", 6000))
    server.listen()

    print("📡 Client prêt à recevoir sur localhost:6000")

    def handle():
        while True:
            conn, _ = server.accept()
            data = json.loads(conn.recv(1024).decode())

            if data["action"] == "receive":
                amount = data["amount"]
                sender = data["from_address"]

                wallet.receive(amount, sender)

                print(f"\n💸 BKN reçus !")
                print(f"Montant: {amount}")
                print(f"Nouveau solde: {wallet.balance:.2f} BKN")

                conn.send(json.dumps({"status": "success"}).encode())

            conn.close()

    threading.Thread(target=handle, daemon=True).start()


def connect(host, port, data):
    s = socket.socket()

    print(f"🔗 Connexion à {host}:{port}...")
    s.connect((host, port))
    print("✅ Connecté!")

    s.send(json.dumps(data).encode())
    res = json.loads(s.recv(1024).decode())

    s.close()
    return res


def main():
    print("🌐 CLIENT DE WALLET BKN")

    owner = input("Votre nom: ")
    balance = float(input("Solde initial (BKN): "))

    wallet = Wallet(owner, balance, "BKN-CLIENT")

    start_client_server(wallet)

    print("\n✅ Wallet créé!")
    print(f"   Adresse: {wallet.address}")
    print(f"   Solde: {wallet.balance:.2f} BKN")

    while True:
        print("\n💎 CLIENT WALLET BKN")
        print("1. Afficher mon wallet")
        print("2. Afficher l'historique")
        print("3. Obtenir infos d'un wallet distant")
        print("4. Transférer des BKN à un wallet distant")
        print("0. Quitter")

        choice = input("\n👉 Votre choix: ")

        try:
            if choice == "1":
                wallet.show_info()

            elif choice == "2":
                wallet.show_history()

            elif choice == "3":
                res = connect("localhost", 5555, {"action": "get_info"})
                print(res)

            elif choice == "4":
                amount = float(input("Montant: "))
                confirm = input("Confirmer (o/n): ")

                if confirm != "o":
                    continue

                if wallet.balance < amount:
                    print("❌ Solde insuffisant")
                    continue

                res = connect("localhost", 5555, {
                    "action": "receive",
                    "amount": amount,
                    "from_address": wallet.address
                })

                wallet.balance -= amount

                print("✅ Transfert réussi")

            elif choice == "0":
                break

        except Exception as e:
            print("❌ Erreur:", e)


if __name__ == "__main__":
    main()