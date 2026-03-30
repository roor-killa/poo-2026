from wallet import Wallet
import threading
import random
import socket
import json


print("🌐 SERVEUR DE WALLET BKN")
nom = input("Nom du propriétaire du wallet: ")
solde = float(input("Solde initial (BKN): "))
host = input("Host (Enter = localhost): ")
if host == "":
    host = "localhost"
port = input("Port (Enter = 5555): ")
while port != "" and not port.isdigit():
    print("Veuillez entrer un numéro de port valide.")
    port = input("Port (Enter = 5555): ")
if port == "":
    port = 5555
adresse = f"BKN-SERVER-{nom}-{random.randint(100, 999)}"
wallet = Wallet(adresse, nom, solde)

print(f"🌐 Serveur BKN démarré sur {host}:{port}")
print(f"🏦 Wallet: {nom}")
print(f"💰 Solde initial: {solde:.2f} BKN")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("En attente de connexions...")

def handle_client(client_socket, adresse_client):

    try:
        data = client_socket.recv(1024)

        if not data:
            return

        message = data.decode()
        requete = json.loads(message)

        if requete["type"] == "transfer":

            montant = requete["amount"]
            expediteur = requete["from"]

            wallet.solde += montant
            wallet.historique.append(("recevoir", montant, expediteur))

            print(f"\n💸 Réception de {montant} BKN de {expediteur}")
            print(f"Nouveau solde: {wallet.solde:.2f} BKN")

            reponse = {
                "status": "success",
                "message": "Transaction reçue"
            }
        
        elif requete["type"] == "info":
            reponse = {
                "adresse": wallet.adresse,
                "nom": wallet.nom_proprietaire,
                "solde": wallet.solde
                }
        client_socket.send(json.dumps(reponse).encode())      

    except Exception as e:
        print("Erreur :", e)

    finally:
        client_socket.close()


def start_server():

    while True:

        client_socket, adresse_client = server.accept()
        print(f"\nConnexion reçue de {adresse_client}")

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, adresse_client)
        )

        client_thread.start()

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

while True:
    cmd = input("[Serveur] > ")

    if cmd == "info":
        print(f"🏦 WALLET BKN - {nom}")
        print(f"Adresse: {adresse}")
        print(f"Solde: {wallet.solde:.2f} BKN")
    
    elif cmd == "hist":
        for transaction in wallet.historique:
            print(transaction)
    
    elif cmd == "quit":
        print("Arrêt du serveur...")
        break