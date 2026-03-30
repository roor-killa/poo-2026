from wallet import Wallet
import socket
import json
import random
import datetime


print("🌐 CLIENT DE WALLET BKN")

nom = input("Votre nom: ")
solde = float(input("Solde initial (BKN): "))

adresse = f"BKN-CLIENT-{nom}-{random.randint(100,999)}"
wallet = Wallet(adresse, nom, solde)

print("\n✅ Wallet créé!")
print(f"   Adresse: {wallet.adresse}")
print(f"   Solde: {wallet.solde:.2f} BKN")


while True:

    print("\n💎 CLIENT WALLET BKN")
    print("1. Afficher mon wallet")
    print("2. Afficher l'historique")
    print("3. Obtenir infos d'un wallet distant")
    print("4. Transférer des BKN à un wallet distant")
    print("0. Quitter")

    choix = input("\n👉 Votre choix: ")

    if choix == "1":

        print(f"\n🏦 WALLET - {wallet.nom_proprietaire}")
        print(f"Adresse: {wallet.adresse}")
        print(f"Solde: {wallet.solde:.2f} BKN")


    elif choix == "2":

        print("\n📜 Historique des transactions")

        if len(wallet.historique) == 0:
            print("Aucune transaction")

        for t in wallet.historique:
            print(t)


    elif choix == "4":

        print("\n💸 Transfert de BKN vers un wallet distant")
        print(f"Votre solde: {wallet.solde:.2f} BKN")

        host = input("Host du serveur destinataire (Enter = localhost): ")
        if host == "":
            host = "localhost"

        port_input = input("Port (Enter = 5555): ")
        if port_input == "":
            port = 5555
        else:
            port = int(port_input)

        montant = float(input("Montant à transférer (BKN): "))

        if montant <= 0:
            print("❌ Montant invalide")
            continue

        if montant > wallet.solde:
            print("❌ Solde insuffisant")
            continue


        print(f"\n💸 Transfert de {montant} BKN en cours...")
        print(f"🔗 Connexion à {host}:{port}...")

        try:

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))

            print("✅ Connecté!")

            transaction_id = f"TXN-BKN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100,999)}"

            requete = {
                "type": "transfer",
                "from": wallet.nom_proprietaire,
                "amount": montant,
                "transaction_id": transaction_id
            }

            client.send(json.dumps(requete).encode())

            wallet.solde -= montant
            wallet.historique.append(("envoyer", montant, host))

            print(f"✅ Débit local effectué ({montant} BKN)")

            reponse = client.recv(1024)
            data = json.loads(reponse.decode())

            if data["status"] == "success":

                print("✅ Crédit distant confirmé!")
                print(f"   Transaction ID: {transaction_id}")

                print(f"\n✅ Transfert de {montant} BKN réussi")

                print("\n📊 Nouveaux soldes:")
                print(f"   Votre wallet: {wallet.solde:.2f} BKN")

            client.close()

        except Exception as e:

            print("❌ Erreur de connexion :", e)


    elif choix == "0":

        print("Au revoir 👋")
        break