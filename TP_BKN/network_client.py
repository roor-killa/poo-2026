import socket
import json
from wallet import Wallet


def connecter_serveur(host, port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    return client


def obtenir_info_wallet(host, port):

    try:
        client = connecter_serveur(host, port)

        request = {
            "action": "get_info"
        }

        client.send(json.dumps(request).encode())

        response = client.recv(4096).decode()
        data = json.loads(response)

        client.close()

        return data

    except Exception as e:
        print("❌ Erreur connexion:", e)
        return None


def transferer(wallet):

    try:

        print("\n💸 Transfert de BKN vers un wallet distant")

        print(f"Votre solde: {wallet.balance:.2f} BKN")

        host = input("Host du serveur destinataire (Enter = localhost): ") or "localhost"
        port_input = input("Port (Enter = 5555): ")
        port = int(port_input) if port_input else 5555

        montant = float(input("Montant à transférer (BKN): "))

        print(f"\n🔗 Connexion à {host}:{port}...")

        client = connecter_serveur(host, port)

        print("✅ Connecté!")

        request = {
            "action": "get_info"
        }

        client.send(json.dumps(request).encode())

        response = client.recv(4096).decode()
        data = json.loads(response)

        wallet_distant = data["wallet"]

        print(f"📍 Wallet distant: {wallet_distant['address']}")

        # débit local
        txn_local = wallet.send(montant, wallet_distant["address"])

        print(f"✅ Débit local effectué ({montant} BKN)")

        request = {
            "action": "receive",
            "amount": montant,
            "from_address": wallet.address
        }

        client.send(json.dumps(request).encode())

        response = client.recv(4096).decode()
        result = json.loads(response)

        if result["status"] == "success":

            print("✅ Crédit distant confirmé!")
            print(f"Transaction ID: {result['transaction_id']}")

            wallet.receive(0, "confirmation")

        else:

            print("❌ Erreur:", result["message"])

        client.close()

    except Exception as e:

        print("❌ Erreur:", e)


def afficher_wallet(wallet):

    print("\n🏦 MON WALLET")
    print("------------------")
    print(f"Propriétaire: {wallet.owner}")
    print(f"Adresse: {wallet.address}")
    print(f"Solde: {wallet.balance:.2f} BKN")


def afficher_historique(wallet):

    print("\n📜 Historique")

    if not wallet.history:
        print("Aucune transaction")

    else:
        for txn in wallet.history:
            print(txn)


def menu():

    print("\n🌐 CLIENT DE WALLET BKN")

    owner = input("Votre nom: ")
    balance = float(input("Solde initial (BKN): "))

    wallet = Wallet(owner, balance, "BKN-CLIENT")

    print("\n✅ Wallet créé!")
    print(f"Adresse: {wallet.address}")
    print(f"Solde: {wallet.balance:.2f} BKN")

    while True:

        print("\n💎 CLIENT WALLET BKN")
        print("1. Afficher mon wallet")
        print("2. Afficher l'historique")
        print("3. Obtenir infos d'un wallet distant")
        print("4. Transférer des BKN à un wallet distant")
        print("0. Quitter")

        choix = input("\n👉 Votre choix: ")

        if choix == "1":

            afficher_wallet(wallet)

        elif choix == "2":

            afficher_historique(wallet)

        elif choix == "3":

            host = input("Host (Enter = localhost): ") or "localhost"
            port_input = input("Port (Enter = 5555): ")
            port = int(port_input) if port_input else 5555

            data = obtenir_info_wallet(host, port)

            if data and data["status"] == "success":

                w = data["wallet"]

                print("\n🏦 WALLET DISTANT")
                print("-------------------")
                print(f"Owner: {w['owner']}")
                print(f"Address: {w['address']}")
                print(f"Balance: {w['balance']} BKN")

        elif choix == "4":

            transferer(wallet)

        elif choix == "0":

            print("\n👋 Fermeture du client")
            break

        else:

            print("❌ Choix invalide")


if __name__ == "__main__":
    menu()
