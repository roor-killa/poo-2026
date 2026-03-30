"""
network_client.py - Client BKN pour les transferts réseau (Partie 2)

Se connecte à un serveur BKN distant, récupère ses infos
et effectue des transferts JSON via TCP.
"""

import socket
import json
from wallet import Wallet


# ──────────────────────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────────────────────

DEFAULT_HOST    = "localhost"
DEFAULT_PORT    = 5555
TIMEOUT_CONNECT = 5   # secondes
TIMEOUT_RECV    = 10  # secondes
BUFFER_SIZE     = 4096


# ──────────────────────────────────────────────────────────────
# Couche réseau bas niveau
# ──────────────────────────────────────────────────────────────

def ouvrir_connexion(host: str, port: int) -> socket.socket:
    """
    Crée et retourne un socket connecté au serveur.

    Raises:
        ConnectionRefusedError si le serveur n'écoute pas.
        TimeoutError si le délai est dépassé.
        OSError pour toute autre erreur réseau.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT_CONNECT)
    sock.connect((host, port))
    sock.settimeout(TIMEOUT_RECV)
    return sock


def send_json(sock: socket.socket, data: dict) -> None:
    """Sérialise et envoie un dictionnaire JSON."""
    payload = json.dumps(data, ensure_ascii=False) + "\n"
    sock.sendall(payload.encode("utf-8"))


def recv_json(sock: socket.socket) -> dict:
    """
    Reçoit et désérialise la réponse JSON du serveur.

    Raises:
        ConnectionError si la connexion est fermée inopinément.
        json.JSONDecodeError si la réponse n'est pas du JSON valide.
    """
    raw = b""
    while not raw.endswith(b"\n"):
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            raise ConnectionError("Le serveur a fermé la connexion.")
        raw += chunk
    return json.loads(raw.decode("utf-8").strip())


# ──────────────────────────────────────────────────────────────
# Actions réseau de haut niveau
# ──────────────────────────────────────────────────────────────

def get_info_distant(host: str, port: int) -> dict | None:
    """
    Récupère les informations d'un wallet distant.

    Returns:
        dict avec les clés address, owner, balance ; ou None si échec.
    """
    print(f"\n🔗 Connexion à {host}:{port}...")
    try:
        with ouvrir_connexion(host, port) as sock:
            print("✅ Connecté !")
            send_json(sock, {"action": "get_info"})
            reponse = recv_json(sock)

        if reponse.get("status") == "success":
            return reponse.get("wallet")
        else:
            print(f"❌ Erreur serveur : {reponse.get('message', 'Inconnue')}")
            return None

    except (ConnectionRefusedError, socket.timeout, TimeoutError):
        print(f"❌ Impossible de joindre {host}:{port}.")
        print("   Vérifiez que le serveur est bien démarré.")
        return None
    except OSError as e:
        print(f"❌ Erreur réseau : {e}")
        return None


def transferer_vers_distant(
    wallet_local: Wallet,
    host: str,
    port: int,
    montant: float,
) -> bool:
    """
    Transfère des BKN du wallet local vers un wallet distant.

    Étapes :
      1. Connexion au serveur.
      2. Récupération de l'adresse distante (get_info).
      3. Débit local.
      4. Crédit distant (receive).
      5. Rollback local si le crédit échoue.

    Returns:
        True si le transfert est réussi, False sinon.
    """
    print(f"\n💸 Transfert de {montant:.2f} BKN en cours...")
    print(f"🔗 Connexion à {host}:{port}...")

    try:
        sock = ouvrir_connexion(host, port)
        print("✅ Connecté !")
    except (ConnectionRefusedError, socket.timeout, TimeoutError):
        print(f"❌ Connexion refusée à {host}:{port}.")
        print("   Vérifiez que le serveur est bien démarré.")
        return False
    except OSError as e:
        print(f"❌ Erreur réseau : {e}")
        return False

    try:
        # 1. Récupérer l'adresse distante
        send_json(sock, {"action": "get_info"})
        info_resp = recv_json(sock)

        if info_resp.get("status") != "success":
            print(f"❌ Impossible de récupérer les infos distantes.")
            return False

        wallet_info = info_resp["wallet"]
        distant_address = wallet_info["address"]
        distant_owner   = wallet_info["owner"]
        print(f"📍 Wallet distant : {distant_address} ({distant_owner})")

        # 2. Débit local
        try:
            wallet_local._valider_montant(montant)
            if montant > wallet_local.balance:
                raise ValueError(
                    f"Solde insuffisant. Disponible : {wallet_local.balance:.2f} BKN."
                )
            wallet_local.balance -= montant
            from wallet import Transaction
            tx_local = Transaction("ENVOI", montant, distant_address,
                                   f"Vers {distant_owner}")
            wallet_local.history.append(tx_local)
            print(f"✅ Débit local effectué ({montant:.2f} BKN)")

        except ValueError as e:
            print(f"❌ Débit impossible : {e}")
            return False

        # 3. Crédit distant
        send_json(sock, {
            "action":       "receive",
            "amount":       montant,
            "from_address": wallet_local.address,
            "from_owner":   wallet_local.owner,
        })
        credit_resp = recv_json(sock)

        if credit_resp.get("status") == "success":
            tx_id        = credit_resp.get("transaction_id", "N/A")
            new_balance  = credit_resp.get("new_balance", "?")
            print(f"✅ Crédit distant confirmé !")
            print(f"   Transaction ID : {tx_id}")
            print(f"\n✅ Transfert de {montant:.2f} BKN réussi")
            print(f"\n📊 Nouveaux soldes :")
            print(f"   Votre wallet   : {wallet_local.balance:.2f} BKN")
            print(f"   Wallet distant : {new_balance} BKN")
            return True

        else:
            # Rollback
            wallet_local.balance += montant
            wallet_local.history.pop()
            msg = credit_resp.get("message", "Inconnue")
            print(f"❌ Crédit distant échoué : {msg}")
            print("   🔄 Débit local annulé (rollback).")
            return False

    except (ConnectionError, socket.timeout, TimeoutError) as e:
        # Rollback si le débit avait déjà eu lieu
        print(f"❌ Connexion perdue durant le transfert : {e}")
        print("   Vérifiez manuellement l'état des deux wallets.")
        return False
    except json.JSONDecodeError:
        print("❌ Réponse serveur invalide (JSON malformé).")
        return False
    finally:
        sock.close()


# ──────────────────────────────────────────────────────────────
# Saisie utilitaire
# ──────────────────────────────────────────────────────────────

def saisir_host_port() -> tuple[str, int]:
    host = input(f"   Host du serveur (Enter = {DEFAULT_HOST}) : ").strip() or DEFAULT_HOST
    while True:
        try:
            port = int(input(f"   Port (Enter = {DEFAULT_PORT}) : ").strip() or DEFAULT_PORT)
            if not (1 <= port <= 65535):
                print("   ⚠️  Port invalide (1-65535).")
                continue
            return host, port
        except ValueError:
            print("   ⚠️  Valeur invalide.")


def saisir_montant(disponible: float) -> float | None:
    """Retourne le montant saisi ou None si annulé/invalide."""
    raw = input(f"   Montant à transférer (BKN) : ").strip()
    try:
        m = float(raw)
        if m <= 0:
            print("   ❌ Le montant doit être strictement positif.")
            return None
        return m
    except ValueError:
        print(f"   ❌ '{raw}' n'est pas un montant valide.")
        return None


# ──────────────────────────────────────────────────────────────
# Actions du menu
# ──────────────────────────────────────────────────────────────

def action_afficher(wallet: Wallet) -> None:
    print(f"\n{wallet}")


def action_historique(wallet: Wallet) -> None:
    wallet.afficher_historique()


def action_get_info() -> None:
    host, port = saisir_host_port()
    infos = get_info_distant(host, port)
    if infos:
        print(f"\n🏦 Wallet distant :")
        print(f"   Adresse      : {infos.get('address')}")
        print(f"   Propriétaire : {infos.get('owner')}")
        print(f"   Solde        : {infos.get('balance', 0):.2f} BKN")


def action_transferer(wallet: Wallet) -> None:
    print(f"\n💸 Transfert de BKN vers un wallet distant")
    print(f"   Votre solde : {wallet.balance:.2f} BKN")
    host, port = saisir_host_port()
    montant = saisir_montant(wallet.balance)
    if montant is not None:
        transferer_vers_distant(wallet, host, port, montant)


# ──────────────────────────────────────────────────────────────
# Menus
# ──────────────────────────────────────────────────────────────

def print_header() -> None:
    print("\n" + "═" * 50)
    print("  🌐 CLIENT DE WALLET BKN")
    print("═" * 50)


def print_menu() -> None:
    print("\n┌─────────────────────────────────────────┐")
    print("│         💎 CLIENT WALLET BKN            │")
    print("├─────────────────────────────────────────┤")
    print("│  1. Afficher mon wallet                 │")
    print("│  2. Afficher l'historique               │")
    print("│  3. Obtenir infos d'un wallet distant   │")
    print("│  4. Transférer des BKN (→ distant)      │")
    print("│  0. Quitter                             │")
    print("└─────────────────────────────────────────┘")


def creer_wallet_client() -> Wallet:
    print_header()
    nom = input("\nVotre nom : ").strip() or "Bob"
    while True:
        try:
            solde = float(input(f"Solde initial (BKN, Enter = 500) : ").strip() or "500")
            if solde < 0:
                print("   ⚠️  Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("   ⚠️  Valeur invalide.")

    wallet = Wallet(nom, solde, prefix="BKN-CLIENT")
    print(f"\n✅ Wallet créé !")
    print(f"   Adresse : {wallet.address}")
    print(f"   Solde   : {wallet.balance:.2f} BKN")
    return wallet


# ──────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────

def main():
    try:
        wallet = creer_wallet_client()

        while True:
            print_menu()
            choix = input("\n👉 Votre choix : ").strip()

            if choix == "1":
                action_afficher(wallet)
            elif choix == "2":
                action_historique(wallet)
            elif choix == "3":
                action_get_info()
            elif choix == "4":
                action_transferer(wallet)
            elif choix == "0":
                print("\n👋 Au revoir ! 💎\n")
                break
            else:
                print("\n⚠️  Choix invalide. Entrez un chiffre entre 0 et 4.")

    except KeyboardInterrupt:
        print("\n\n👋 Interruption clavier. À bientôt !")


if __name__ == "__main__":
    main()
