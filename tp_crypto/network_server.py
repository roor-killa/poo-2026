import socket
import json
import threading
from wallet import Wallet

# Variable globale pour notre wallet serveur (pour que le réseau y ait accès)
mon_wallet = None

def ecouter_reseau(host, port):
    """Cette fonction tourne en arrière-plan (Thread) pour écouter les clients."""
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permet de réutiliser le port directement si on relance le script
    serveur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    serveur_socket.bind((host, port))
    serveur_socket.listen(5)
    
    print(f"\n🌐 Serveur BKN démarré sur {host}:{port}")
    print("En attente de connexions...")

    while True:
        # On attend qu'un client frappe à la porte
        client_socket, addr = serveur_socket.accept()
        print(f"\n🔗 [Réseau] Client connecté depuis {addr}")
        
        # TODO plus tard : Lire le message JSON du client
        
        client_socket.close()

def main():
    global mon_wallet
    print("🌐 SERVEUR DE WALLET BKN")
    nom = input("Nom du propriétaire du wallet: ")
    solde_str = input("Solde initial (BKN): ")
    solde = float(solde_str) if solde_str else 1000.0

    # On crée le wallet du serveur avec le préfixe SERVER
    mon_wallet = Wallet(nom, solde, prefix="SERVER")
    
    host = input("Host (Enter = localhost): ") or "127.0.0.1"
    port_str = input("Port (Enter = 5555): ") or "5555"
    port = int(port_str)

    # 1. On lance l'écoute réseau dans un "Thread" (en arrière-plan)
    # daemon=True permet au thread de s'arrêter quand on quitte le programme principal
    thread_serveur = threading.Thread(target=ecouter_reseau, args=(host, port), daemon=True)
    thread_serveur.start()

    # 2. Boucle du menu local (au premier plan)
    while True:
        commande = input("\n[Serveur] > ").strip().lower()
        
        if commande == "info":
            # TODO : Utilise la méthode de la Partie 1 pour afficher les infos de mon_wallet
            pass
            
        elif commande == "hist":
            # TODO : Utilise la méthode de la Partie 1 pour afficher l'historique de mon_wallet
            pass
            
        elif commande == "quitter":
            print("Fermeture du serveur... 👋")
            break
            
        elif commande == "":
            pass # Si l'utilisateur appuie juste sur Entrée, on ne fait rien
            
        else:
            print("Commandes dispo: info, hist, quitter")

if __name__ == "__main__":
    main()
    