import socket
import json
import uuid
from wallet import Wallet

def request(host, port, payload):
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((host, port))

        s.send(json.dumps(payload).encode())
        res = json.loads(s.recv(4096).decode())

        s.close()
        return res

    except Exception as e:
        return {"status": "error", "msg": str(e)}

def main():
    print("🌐 CLIENT BKN")

    owner = input("Nom: ")
    balance = float(input("Solde: "))

    address = f"BKN-CLIENT-{owner.upper()}-{str(uuid.uuid4())[:3]}"
    wallet = Wallet(address, owner, balance)

    while True:
        print("\n1. Info")
        print("2. Historique")
        print("3. Info distante")
        print("4. Envoyer BKN")
        print("0. Quitter")

        c = input("👉 ")

        if c == "1":
            wallet.show_info()

        elif c == "2":
            wallet.show_history()

        elif c == "3":
            host = input("Host: ") or "localhost"
            port = int(input("Port: ") or 5555)

            print(request(host, port, {"action": "get_info"}))

        elif c == "4":
            try:
                host = input("Host: ") or "localhost"
                port = int(input("Port: ") or 5555)
                amount = float(input("Montant: "))

                wallet.debit(amount)

                res = request(host, port, {
                    "action": "receive",
                    "amount": amount,
                    "from_address": wallet.address
                })

                if res["status"] == "success":
                    print("✅ Transfert OK")
                    print(res)
                else:
                    raise Exception("Erreur serveur")

            except Exception as e:
                print("❌", e)

        elif c == "0":
            break

if __name__ == "__main__":
    main()