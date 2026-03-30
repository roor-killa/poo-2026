"""
network_client.py — Client de wallet BKN (Partie 2)

TODO : Complétez les sections marquées TODO.

Fonctionnalités attendues :
  1. Créer un wallet local
  2. Se connecter à un serveur distant
  3. Envoyer une requête JSON "get_info" pour récupérer les infos distantes
  4. Envoyer une requête JSON "receive" pour créditer le wallet distant
     et débiter le wallet local
  5. Gérer les erreurs réseau (timeout, connexion refusée)
"""

import socket
import json

from wallet import Wallet, InsufficientFundsError, InvalidAmountError

TIMEOUT = 10  # secondes


def send_request(host: str, port: int, payload: dict) -> dict:
    """
    Ouvre une connexion TCP vers (host, port), envoie `payload` en JSON
    et retourne la réponse JSON désérialisée.

    Raises
    ------
    ConnectionRefusedError
        Si le serveur n'est pas démarré.
    TimeoutError
        Si le serveur ne répond pas dans le délai imparti.
    json.JSONDecodeError
        Si la réponse n'est pas du JSON valide.

    TODO : Implémenter la fonction.
    """
    # TODO : Créer un socket TCP avec socket.socket(...)
    # TODO : Appliquer un timeout avec sock.settimeout(TIMEOUT)
    # TODO : Se connecter avec sock.connect((host, port))
    # TODO : Envoyer json.dumps(payload).encode("utf-8") avec sock.sendall()
    # TODO : Recevoir la réponse avec sock.recv(4096).decode("utf-8")
    # TODO : Désérialiser et retourner
    # TODO : Fermer le socket dans un bloc finally

    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(TIMEOUT)
        sock.connect((host,port))
        sock.sendall(json.dumps(payload).encode("utf-8"))
        data= sock.recv(4096).decode("utf-8")
        response=json.loads(data)
        return response
    finally:
        sock.close()



def action_get_info(host: str, port: int) -> None:
    """
    Récupère et affiche les informations du wallet distant.

    TODO : Appeler send_request avec {"action": "get_info"}
           et afficher le résultat.
    """
    print(f"\n🔍 Récupération des infos du wallet distant ({host}:{port})...")
    # TODO : Appeler send_request et afficher wallet["owner"], wallet["address"], wallet["balance"]
    try:
        response = send_request(host, port, {"action": "get_info"})
        if response.get("status") == "success":
            wallet = response["wallet"]
            print(f"\n Wallet")
            print(f"Nom : {wallet['owner']}")
            print(f"Adresse : {wallet['address']}")
            print(f"Solde : {wallet['balance']:.2f}BKN")
        else:
            print(f"Erreur:{response.get('message')}")
    except ConnectionRefusedError:
        print("Connexion refusée.")
    except Exception as e:
        print(f"Erreur: {e}")

def action_transfer(local_wallet: Wallet, host: str, port: int) -> None:
    """
    Demande un montant, débite le wallet local, et crédite le wallet distant.

    Étapes :
      1. Récupérer les infos du wallet distant (get_info) pour afficher l'adresse
      2. Demander le montant à l'utilisateur
      3. Vérifier que le solde local est suffisant
      4. Envoyer la requête "receive" au serveur
      5. Si succès → débiter le wallet local avec wallet.receive() en sens inverse
         (ou directement soustraire le solde — voir TODO ci-dessous)
      6. Afficher les nouveaux soldes

    TODO : Implémenter les étapes ci-dessus.
    """
    print(f"\n💸 Transfert de BKN vers un wallet distant")
    print(f"   Votre solde : {local_wallet.balance:.2f} BKN")

    host_input = input("Host du serveur destinataire (Entrée = localhost) : ").strip()
    if host_input:
        host = host_input

    try:
        port_input = input(f"Port (Entrée = {port}) : ").strip()
        if port_input:
            port = int(port_input)
    except ValueError:
        print("Port invalide, utilisation du port par défaut.")

    try:
        amount = float(input("Montant à transférer (BKN) : ").strip())
    except ValueError:
        print("❌ Montant invalide.")
        return

    # TODO : Étape 1 — get_info pour récupérer l'adresse distante
    # TODO : Étape 2 — Vérifier amount > 0 et amount <= local_wallet.balance
    # TODO : Étape 3 — send_request avec {"action": "receive", "amount": amount, "from_address": local_wallet.address}
    # TODO : Étape 4 — Si réponse "success", débiter local_wallet
    #                  (utiliser wallet.balance -= amount directement OU créer une méthode dédiée)
    # TODO : Afficher transaction_id et nouveaux soldes
    try:
        response = send_request(host, port, {"action": "get_info"})
        if response.get("status") == "success":
            walletdistant = response["wallet"]
            print(f"Adresse distante : {walletdistant['address']}")
        
        if amount > 0 and amount <= local_wallet.balance:
            réponsesendrec = send_request(host, port, {"action": "receive", "amount": amount, "from_address": local_wallet.address})
            if réponsesendrec["status"] == "success":
                local_wallet.balance -= amount
                local_wallet._record_transaction(
                    tx_id=réponsesendrec.get('tx_id', ''),
                    kind="DEBIT",
                    amount=amount,
                    counterpart=walletdistant['address']
                )
                
                print(f"Success! ID transaction: {réponsesendrec.get('tx_id')}")
                print(f"Votre nouveau solde est de: {local_wallet.balance:.2f} BKN")
            else:
                print(f"Erreur: {réponsesendrec.get('message')}")
        else:
            print("Montant invalide ou solde insuffisant.")
    except ConnectionRefusedError:
        print("Connexion refusée.")
    except Exception as e:
        print(f"Erreur: {e}")

def afficher_menu() -> None:
    print("\n💎 CLIENT WALLET BKN")
    print("1. Afficher mon wallet")
    print("2. Afficher l'historique")
    print("3. Obtenir infos d'un wallet distant")
    print("4. Transférer des BKN à un wallet distant")
    print("0. Quitter")


def main() -> None:
    print("🌐 CLIENT DE WALLET BKN")
    owner = input("Votre nom : ").strip() or "Bob"

    try:
        balance = float(input("Solde initial (BKN) : ").strip() or "500")
    except ValueError:
        print("Solde invalide, valeur par défaut : 500")
        balance = 500.0

    wallet = Wallet(owner=owner, initial_balance=balance, prefix="CLIENT")

    print(f"\n✅ Wallet créé !")
    print(f"   Adresse : {wallet.address}")
    print(f"   Solde   : {wallet.balance:.2f} BKN")

    # Hôte et port par défaut pour les connexions sortantes
    default_host = "localhost"
    default_port = 5555

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            wallet.display_info()

        elif choix == "2":
            wallet.display_history()

        elif choix == "3":
            # TODO : Demander host/port et appeler action_get_info()
            host=input("Entrez le host")
            port=int(input("Entrez le port:"))
            action_get_info(host,port)
        elif choix == "4":
            # TODO : Appeler action_transfer(wallet, default_host, default_port)
            action_transfer(wallet,default_host,default_port)

        elif choix == "0":
            print("\n👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
