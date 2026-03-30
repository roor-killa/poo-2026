import socket
import json
import threading
import datetime
from wallet import Wallet


TIMEOUT_CONNEXION = 5  # Secondes avant abandon de la tentative de connexion


def envoyer_requete(host: str, port: int, requete: dict) -> dict:
    """Envoie une requête JSON au serveur et retourne la réponse."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT_CONNEXION)

        print(f"   🔗 Connexion à {host}:{port}...")
        sock.connect((host, port))
        print("   ✅ Connecté !")

        sock.sendall(json.dumps(requete).encode("utf-8"))
        reponse_brute = sock.recv(4096)
        return json.loads(reponse_brute.decode("utf-8"))


def obtenir_infos_distant(host: str, port: int) -> dict | None:
    """Récupère les informations du wallet distant."""
    try:
        reponse = envoyer_requete(host, port, {"action": "get_info"})

        if reponse.get("status") == "success":
            info = reponse["wallet"]
            print(f"\n📋 Infos du wallet distant :")
            print(f"   Propriétaire : {info['owner']}")
            print(f"   Adresse      : {info['address']}")
            print(f"   Solde        : {info['balance']:.2f} BKN")
            return info
        else:
            print(f"❌ Erreur serveur : {reponse.get('message')}")
            return None

    except socket.timeout:
        print("❌ Erreur : délai de connexion dépassé (timeout).")
    except ConnectionRefusedError:
        print(f"❌ Erreur : connexion refusée sur {host}:{port}.")
    except Exception as e:
        print(f"❌ Erreur réseau : {e}")
    return None


def transferer_vers_distant(wallet_local: Wallet, host: str, port: int):
    """Effectue un transfert de BKN du wallet local vers le wallet distant."""
    print(f"\n💸 Transfert de BKN vers un wallet distant")
    print(f"   Votre solde : {wallet_local.solde:.2f} BKN")

    try:
        saisie = input("   Montant à transférer (BKN) : ").strip()
        montant = float(saisie)

        if montant <= 0:
            print("❌ Le montant doit être supérieur à 0.")
            return
        if montant > wallet_local.solde:
            print(f"❌ Solde insuffisant. Disponible : {wallet_local.solde:.2f} BKN")
            return

        print(f"\n💸 Transfert de {montant:.2f} BKN en cours...")

        # Étape 1 : récupérer l'adresse du wallet distant
        info_distant = obtenir_infos_distant(host, port)
        if info_distant is None:
            return

        # Étape 2 : débiter le wallet local
        wallet_local.solde -= montant
        wallet_local.historique.append({
            "type": "ENVOI",
            "montant": montant,
            "vers": info_distant["address"],
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"   ✅ Débit local effectué ({montant:.2f} BKN)")

        # Étape 3 : demander au serveur de créditer son wallet
        reponse = envoyer_requete(host, port, {
            "action": "receive",
            "amount": montant,
            "from_address": wallet_local.adresse
        })

        if reponse.get("status") == "success":
            print(f"   ✅ Crédit distant confirmé !")
            print(f"      Transaction ID : {reponse.get('transaction_id')}")
            print(f"\n✅ Transfert de {montant:.2f} BKN réussi !")
            print(f"\n📊 Nouveaux soldes :")
            print(f"   Votre wallet   : {wallet_local.solde:.2f} BKN")
            print(f"   Wallet distant : {reponse.get('new_balance'):.2f} BKN")
        else:
            # Le crédit a échoué : on rembourse le wallet local
            print(f"❌ Erreur côté serveur : {reponse.get('message')}")
            print("↩️  Remboursement du débit local...")
            wallet_local.solde += montant
            wallet_local.historique.pop()

    except ValueError:
        print("❌ Montant invalide. Veuillez entrer un nombre.")
    except socket.timeout:
        print("❌ Erreur : délai de connexion dépassé (timeout).")
        wallet_local.solde += montant
    except ConnectionRefusedError:
        print(f"❌ Connexion refusée. Le serveur est-il en ligne ?")
    except Exception as e:
        print(f"❌ Erreur réseau inattendue : {e}")


# ──────────────────────────────────────────────────────────────────────────────
# BONUS NIVEAU 1 : écoute persistante pour recevoir des BKN depuis le serveur
# ──────────────────────────────────────────────────────────────────────────────

def ecouter_serveur(wallet_local: Wallet, host: str, port_ecoute: int):
    """
    Ouvre un socket d'écoute dédié pour recevoir des transferts initiés
    par le serveur (connexion entrante serveur → client).
    Tourne dans un thread daemon en arrière-plan.
    """
    sock_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock_ecoute.bind((host, port_ecoute))
        sock_ecoute.listen(3)
        print(f"\n👂 En écoute des transferts entrants sur le port {port_ecoute}...")

        while True:
            try:
                conn, addr = sock_ecoute.accept()
                with conn:
                    donnees_brutes = conn.recv(4096)
                    if not donnees_brutes:
                        continue

                    requete = json.loads(donnees_brutes.decode("utf-8"))
                    action = requete.get("action")

                    if action == "receive_from_server":
                        # Le serveur veut envoyer des BKN au client
                        montant = requete.get("amount", 0)
                        depuis = requete.get("from_address", "serveur")

                        if montant <= 0:
                            conn.sendall(json.dumps({
                                "status": "error", "message": "Montant invalide."
                            }).encode("utf-8"))
                            continue

                        wallet_local.recevoir(montant, depuis)
                        tx_id = wallet_local._generer_tx_id()

                        print(f"\n\n💰 Le serveur vous a envoyé {montant:.2f} BKN !")
                        print(f"   Nouveau solde : {wallet_local.solde:.2f} BKN")
                        print(f"   Transaction   : {tx_id}")

                        conn.sendall(json.dumps({
                            "status": "success",
                            "transaction_id": tx_id,
                            "new_balance": wallet_local.solde
                        }).encode("utf-8"))

                    else:
                        conn.sendall(json.dumps({
                            "status": "error", "message": "Action inconnue."
                        }).encode("utf-8"))

            except OSError:
                break

    except OSError as e:
        print(f"⚠️  Impossible d'ouvrir le port d'écoute {port_ecoute} : {e}")
    finally:
        sock_ecoute.close()


def afficher_menu():
    """Affiche le menu principal du client."""
    print("\n💎 CLIENT WALLET BKN")
    print("1. Afficher mon wallet")
    print("2. Afficher l'historique")
    print("3. Obtenir infos d'un wallet distant")
    print("4. Transférer des BKN à un wallet distant")
    print("0. Quitter")


def saisir_connexion() -> tuple[str, int]:
    """Demande à l'utilisateur l'host et le port du serveur."""
    host = input("   Host du serveur (Entrée = localhost) : ").strip() or "localhost"
    port = input("   Port (Entrée = 5555) : ").strip()
    port = int(port) if port else 5555
    return host, port


def main():
    print("\n🌐 CLIENT DE WALLET BKN")

    nom = input("Votre nom : ").strip()
    solde = float(input("Solde initial (BKN) : ").strip())

    # Port d'écoute du client pour les transferts entrants (serveur → client)
    port_ecoute_str = input("Port d'écoute entrant (Entrée = 5556) : ").strip()
    port_ecoute = int(port_ecoute_str) if port_ecoute_str else 5556

    wallet = Wallet(nom, solde_initial=solde, prefix="BKN-CLIENT")

    print(f"\n✅ Wallet créé !")
    wallet.afficher_info()

    # Lancement du thread d'écoute en arrière-plan (bonus niveau 1)
    thread_ecoute = threading.Thread(
        target=ecouter_serveur,
        args=(wallet, "localhost", port_ecoute),
        daemon=True
    )
    thread_ecoute.start()

    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix : ").strip()

        if choix == "1":
            wallet.afficher_info()

        elif choix == "2":
            wallet.afficher_historique()

        elif choix == "3":
            host, port = saisir_connexion()
            obtenir_infos_distant(host, port)

        elif choix == "4":
            host, port = saisir_connexion()
            transferer_vers_distant(wallet, host, port)

        elif choix == "0":
            print("\n👋 Au revoir ! Vos BKN sont en sécurité.")
            break

        else:
            print("❌ Choix invalide. Entrez un numéro entre 0 et 4.")


if __name__ == "__main__":
    main()
