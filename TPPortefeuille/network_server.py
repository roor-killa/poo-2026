import socket
import threading
import json
import datetime
from wallet import Wallet


# Stocke la connexion active pour permettre au serveur d'envoyer des BKN
connexion_active = None
lock_connexion = threading.Lock()


def traiter_requete(donnees: dict, wallet: Wallet) -> dict:
    """Analyse la requête JSON reçue et retourne une réponse appropriée."""
    action = donnees.get("action")

    if action == "get_info":
        # Retourne les informations du wallet serveur
        return {
            "status": "success",
            "wallet": {
                "address": wallet.adresse,
                "owner": wallet.proprietaire,
                "balance": wallet.solde
            }
        }

    elif action == "receive":
        # Le serveur reçoit des BKN envoyés par le client
        montant = donnees.get("amount", 0)
        depuis = donnees.get("from_address", "inconnu")

        if montant <= 0:
            return {"status": "error", "message": "Montant invalide."}

        wallet.recevoir(montant, depuis)
        tx_id = wallet._generer_tx_id()

        print(f"\n💰 Réception de {montant:.2f} BKN depuis {depuis}")
        print(f"   Nouveau solde : {wallet.solde:.2f} BKN")

        return {
            "status": "success",
            "message": f"Réception de {montant:.2f} BKN confirmée",
            "transaction_id": tx_id,
            "new_balance": wallet.solde
        }

    elif action == "debit_confirm":
        # Le client confirme qu'il a bien reçu les BKN envoyés par le serveur
        montant = donnees.get("amount", 0)
        nouveau_solde_client = donnees.get("new_balance", 0)
        tx_id = donnees.get("transaction_id", "?")

        print(f"\n✅ Client a confirmé la réception de {montant:.2f} BKN")
        print(f"   Nouveau solde client : {nouveau_solde_client:.2f} BKN")
        print(f"   Transaction ID       : {tx_id}")

        return {"status": "success", "message": "Confirmation reçue."}

    else:
        return {"status": "error", "message": f"Action inconnue : {action}"}


def gerer_client(conn: socket.socket, adresse_client: tuple, wallet: Wallet):
    """Gère la communication avec un client connecté."""
    global connexion_active

    print(f"\n🔗 Client connecté : {adresse_client}")

    # Mémorisation de la connexion pour le transfert serveur → client
    with lock_connexion:
        connexion_active = conn

    try:
        with conn:
            while True:
                donnees_brutes = conn.recv(4096)
                if not donnees_brutes:
                    break

                requete = json.loads(donnees_brutes.decode("utf-8"))
                print(f"   📩 Requête reçue : {requete.get('action')}")

                reponse = traiter_requete(requete, wallet)
                conn.sendall(json.dumps(reponse).encode("utf-8"))

    except json.JSONDecodeError:
        print("❌ Erreur : données reçues invalides.")
    except ConnectionResetError:
        print(f"⚠️  Client {adresse_client} déconnecté de façon inattendue.")
    finally:
        with lock_connexion:
            connexion_active = None
        print(f"🔌 Client {adresse_client} déconnecté.")


def transferer_vers_client(wallet: Wallet):
    """BONUS N1 — Envoie des BKN au client connecté (serveur → client)."""
    with lock_connexion:
        conn = connexion_active

    if conn is None:
        print("❌ Aucun client connecté pour le moment.")
        return

    print(f"\n💸 Transfert vers le client connecté")
    print(f"   Votre solde : {wallet.solde:.2f} BKN")

    try:
        saisie = input("   Montant à envoyer (BKN) : ").strip()
        montant = float(saisie)

        if montant <= 0:
            print("❌ Le montant doit être supérieur à 0.")
            return
        if montant > wallet.solde:
            print(f"❌ Solde insuffisant. Disponible : {wallet.solde:.2f} BKN")
            return

        # Étape 1 : débiter le wallet serveur
        wallet.solde -= montant
        wallet.historique.append({
            "type": "ENVOI",
            "montant": montant,
            "vers": "client connecté",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"   ✅ Débit local effectué ({montant:.2f} BKN)")

        # Étape 2 : demander au client de créditer son wallet
        requete = {
            "action": "receive_from_server",
            "amount": montant,
            "from_address": wallet.adresse
        }

        with lock_connexion:
            conn = connexion_active
            if conn is None:
                raise ConnectionError("Le client s'est déconnecté entre-temps.")
            conn.sendall(json.dumps(requete).encode("utf-8"))
            reponse_brute = conn.recv(4096)

        reponse = json.loads(reponse_brute.decode("utf-8"))

        if reponse.get("status") == "success":
            print(f"\n✅ Transfert de {montant:.2f} BKN vers le client réussi !")
            print(f"   Votre nouveau solde : {wallet.solde:.2f} BKN")
        else:
            # Remboursement en cas d'échec côté client
            print(f"❌ Erreur côté client : {reponse.get('message')}")
            print("↩️  Remboursement du débit...")
            wallet.solde += montant
            wallet.historique.pop()

    except ValueError:
        print("❌ Montant invalide.")
    except (ConnectionError, OSError) as e:
        print(f"❌ Erreur réseau : {e}")
        print("↩️  Remboursement du débit...")
        wallet.solde += montant


def commandes_locales(wallet: Wallet, serveur: socket.socket):
    """Gère les commandes tapées localement par l'opérateur du serveur."""
    print("\n💡 Commandes : info | hist | send | quit")
    while True:
        cmd = input("[Serveur] > ").strip().lower()

        if cmd == "info":
            wallet.afficher_info()

        elif cmd == "hist":
            wallet.afficher_historique()

        elif cmd == "send":
            # Bonus niveau 1 : envoi de BKN depuis le serveur vers le client
            transferer_vers_client(wallet)

        elif cmd == "quit":
            print("\n👋 Arrêt du serveur...")
            serveur.close()
            break

        else:
            print("❌ Commande inconnue. Utilisez : info | hist | send | quit")


def main():
    print("\n🌐 SERVEUR DE WALLET BKN")

    nom = input("Nom du propriétaire du wallet : ").strip()
    solde = float(input("Solde initial (BKN) : ").strip())
    host = input("Host (Entrée = localhost) : ").strip() or "localhost"
    port = input("Port (Entrée = 5555) : ").strip()
    port = int(port) if port else 5555

    wallet = Wallet(nom, solde_initial=solde, prefix="BKN-SERVER")

    print(f"\n🌐 Serveur BKN démarré sur {host}:{port}")
    wallet.afficher_info()
    print("En attente de connexions...\n")

    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        serveur.bind((host, port))
        serveur.listen(5)

        thread_cmd = threading.Thread(
            target=commandes_locales, args=(wallet, serveur), daemon=True
        )
        thread_cmd.start()

        while True:
            try:
                conn, adresse_client = serveur.accept()
                thread_client = threading.Thread(
                    target=gerer_client, args=(conn, adresse_client, wallet), daemon=True
                )
                thread_client.start()
            except OSError:
                break

    except OSError as e:
        print(f"❌ Impossible de démarrer le serveur : {e}")
    finally:
        serveur.close()


if __name__ == "__main__":
    main()
