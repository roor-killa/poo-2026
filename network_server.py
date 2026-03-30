"""
network_server.py - Serveur BKN pour les transferts réseau (Partie 2)

Lance un serveur TCP qui accepte les connexions de clients BKN.
Gère les requêtes JSON : get_info et receive.
"""

import socket
import json
import threading
from datetime import datetime
from wallet import Wallet


# ──────────────────────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────────────────────

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5555
BUFFER_SIZE  = 4096
TIMEOUT_SECS = 30


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def send_json(conn: socket.socket, data: dict) -> None:
    """Sérialise et envoie un dictionnaire JSON au client."""
    payload = json.dumps(data, ensure_ascii=False) + "\n"
    conn.sendall(payload.encode("utf-8"))


def recv_json(conn: socket.socket) -> dict | None:
    """Reçoit et désérialise une requête JSON du client."""
    try:
        raw = b""
        while not raw.endswith(b"\n"):
            chunk = conn.recv(BUFFER_SIZE)
            if not chunk:
                return None
            raw += chunk
        return json.loads(raw.decode("utf-8").strip())
    except (json.JSONDecodeError, OSError):
        return None


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# ──────────────────────────────────────────────────────────────
# Traitement d'un client (thread)
# ──────────────────────────────────────────────────────────────

def handle_client(conn: socket.socket, addr: tuple, wallet: Wallet) -> None:
    """Traite toutes les requêtes d'une connexion cliente."""
    log(f"🔗 Nouveau client connecté : {addr[0]}:{addr[1]}")
    conn.settimeout(TIMEOUT_SECS)

    try:
        while True:
            request = recv_json(conn)
            if request is None:
                log(f"🔌 Client {addr[0]}:{addr[1]} déconnecté.")
                break

            action = request.get("action", "").lower()
            log(f"📨 Requête [{action}] de {addr[0]}:{addr[1]}")

            # ── get_info ────────────────────────────────────────
            if action == "get_info":
                send_json(conn, {
                    "status": "success",
                    "wallet": wallet.get_info(),
                })

            # ── receive ─────────────────────────────────────────
            elif action == "receive":
                try:
                    amount       = float(request.get("amount", 0))
                    from_address = str(request.get("from_address", "INCONNU"))
                    from_owner   = str(request.get("from_owner", ""))

                    tx_id = wallet.recevoir(amount, from_address, from_owner)
                    log(f"✅ Réception de {amount:.2f} BKN depuis {from_address}")
                    log(f"   Nouveau solde : {wallet.balance:.2f} BKN")

                    send_json(conn, {
                        "status": "success",
                        "message": f"Réception de {amount:.2f} BKN confirmée",
                        "transaction_id": tx_id,
                        "new_balance": wallet.balance,
                    })

                except (ValueError, TypeError) as e:
                    send_json(conn, {
                        "status": "error",
                        "message": str(e),
                    })

            # ── action inconnue ──────────────────────────────────
            else:
                send_json(conn, {
                    "status": "error",
                    "message": f"Action inconnue : '{action}'",
                })

    except socket.timeout:
        log(f"⏰ Timeout client {addr[0]}:{addr[1]}")
    except OSError as e:
        log(f"❌ Erreur réseau : {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────
# Thread d'écoute des commandes locales
# ──────────────────────────────────────────────────────────────

def local_command_loop(wallet: Wallet, stop_event: threading.Event) -> None:
    """Lit les commandes tapées directement dans le terminal serveur."""
    print("\n💡 Commandes disponibles : info | hist | quit\n")
    while not stop_event.is_set():
        try:
            cmd = input("[Serveur] > ").strip().lower()
        except EOFError:
            break

        if cmd == "info":
            print(f"\n{wallet}\n")

        elif cmd in ("hist", "history", "historique"):
            wallet.afficher_historique()

        elif cmd == "quit":
            print("\n👋 Arrêt du serveur...")
            stop_event.set()
            break

        elif cmd:
            print("⚠️  Commande inconnue. Tapez : info | hist | quit")


# ──────────────────────────────────────────────────────────────
# Initialisation
# ──────────────────────────────────────────────────────────────

def configurer_serveur() -> tuple[Wallet, str, int]:
    """Lit la configuration serveur depuis l'entrée standard."""
    print("\n" + "═" * 50)
    print("  🌐 SERVEUR DE WALLET BKN")
    print("═" * 50)

    nom = input("\nNom du propriétaire du wallet : ").strip() or "Alice"

    while True:
        try:
            solde = float(input(f"Solde initial de {nom} (BKN, Enter = 1000) : ").strip() or "1000")
            if solde < 0:
                print("   ⚠️  Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("   ⚠️  Valeur invalide, réessayez.")

    host = input(f"Host (Enter = {DEFAULT_HOST}) : ").strip() or DEFAULT_HOST

    while True:
        try:
            port = int(input(f"Port (Enter = {DEFAULT_PORT}) : ").strip() or DEFAULT_PORT)
            if not (1024 <= port <= 65535):
                print("   ⚠️  Le port doit être entre 1024 et 65535.")
                continue
            break
        except ValueError:
            print("   ⚠️  Valeur invalide, réessayez.")

    wallet = Wallet(nom, solde, prefix="BKN-SERVER")
    return wallet, host, port


# ──────────────────────────────────────────────────────────────
# Démarrage du serveur
# ──────────────────────────────────────────────────────────────

def demarrer_serveur(wallet: Wallet, host: str, port: int) -> None:
    """Démarre le serveur TCP et accepte les connexions en boucle."""
    stop_event = threading.Event()

    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(5)
        server_sock.settimeout(1.0)   # timeout pour vérifier stop_event

    except OSError as e:
        print(f"\n❌ Impossible de démarrer le serveur : {e}")
        if "already in use" in str(e).lower() or e.errno == 98 or e.errno == 48:
            print(f"   Le port {port} est déjà utilisé. Essayez un autre port.")
        return

    print(f"\n🌐 Serveur BKN démarré sur {host}:{port}")
    print(f"🏦 Wallet : {wallet.owner}")
    print(f"💰 Solde initial : {wallet.balance:.2f} BKN")
    print("En attente de connexions...\n")

    # Lancer le thread de commandes locales
    cmd_thread = threading.Thread(
        target=local_command_loop,
        args=(wallet, stop_event),
        daemon=True,
    )
    cmd_thread.start()

    # Boucle d'acceptation des clients
    while not stop_event.is_set():
        try:
            conn, addr = server_sock.accept()
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr, wallet),
                daemon=True,
            )
            t.start()
        except socket.timeout:
            continue   # vérifie stop_event et re-boucle
        except OSError:
            break

    server_sock.close()
    print("🔴 Serveur arrêté.")


# ──────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────

def main():
    try:
        wallet, host, port = configurer_serveur()
        demarrer_serveur(wallet, host, port)
    except KeyboardInterrupt:
        print("\n\n👋 Interruption clavier. Serveur arrêté.")


if __name__ == "__main__":
    main()
