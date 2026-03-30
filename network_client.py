import socket
import json
from wallet import Wallet

def main():
    print("💻 CLIENT DE TRANSFERT BKN")
    nom = input("Votre nom (ex: Bob): ")
    
    # Création du wallet client
    mon_wallet = Wallet(nom, 500.0, prefix="CLIENT")
    
    host = "127.0.0.1"
    port = 5555
    
    while True:
        print("\n--- MENU CLIENT ---")
        print("1. Afficher mon solde")
        print("2. Envoyer des BKN au Serveur")
        print("0. Quitter")
        
        choix = input("\n👉 Choix: ")
        
        if choix == "1":
            mon_wallet.display_info()
            
        elif choix == "2":
            montant_str = input("Montant à envoyer (BKN): ")
            try:
                montant = float(montant_str)
                
                # 1. Préparation du JSON
                transaction = {"sender": mon_wallet.owner, "amount": montant}
                donnees_json = json.dumps(transaction)
                
                # 2. Connexion et Envoi
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                client_socket.send(donnees_json.encode('utf-8'))
                
                # Optionnel : Lecture de la réponse du serveur
                # reponse = client_socket.recv(1024).decode('utf-8')
                # print(f"📩 Serveur : {reponse}")
                
                client_socket.close()
                
                # 3. Mise à jour locale
                mon_wallet.balance -= montant
                mon_wallet.transactions.append(f"Transfert réseau : -{montant:.2f} BKN")
                
                print(f"✅ Transaction de {montant} BKN envoyée !")
                
            except Exception as e:
                print(f"❌ Erreur : {e}")
                
        elif choix == "0":
            break

if __name__ == "__main__":
    main()