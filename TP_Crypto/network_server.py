import socket, json, threading, datetime, uuid

class Wallet:
    def __init__(self, nom, solde_initial=0.0):
        self.adresse = "BKN-" + uuid.uuid4().hex[:16].upper()
        self.nom = nom
        self._solde = solde_initial
        self.historique = []
        if solde_initial > 0:
            self._enregistrer("DEPOT", solde_initial, "GENESIS")

    @property
    def solde(self):
        return self._solde

    def recevoir(self, montant, from_address):
        montant = float(montant)
        if montant <= 0:
            raise ValueError("Montant invalide.")
        txn_id = "TXN-BKN-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:6].upper()
        self._solde += montant
        self._enregistrer("RECEPTION", montant, from_address, txn_id)
        return txn_id

    def _enregistrer(self, type_tx, montant, contrepartie, txn_id=None):
        if not txn_id:
            txn_id = "TXN-BKN-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:6].upper()
        self.historique.append({
            "txn_id": txn_id, "type": type_tx, "montant": montant,
            "contrepartie": contrepartie,
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "solde_apres": self._solde
        })

    def afficher(self):
        print(f"\n  🏦 {self.nom} | Adresse: {self.adresse} | Solde: {self._solde:.2f} BKN")

    def afficher_historique(self):
        print(f"\n  📜 Historique de {self.nom} ({len(self.historique)} transaction(s))")
        for tx in self.historique:
            signe = "+" if tx["montant"] >= 0 else ""
            print(f"  [{tx['timestamp']}] {tx['type']} {signe}{tx['montant']:.2f} BKN | {tx['contrepartie']} | {tx['txn_id']}")


def gerer_client(conn, wallet, lock):
    try:
        data = b""
        conn.settimeout(10)
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            try:
                json.loads(data.decode())
                break
            except:
                continue

        req = json.loads(data.decode())
        action = req.get("action")

        if action == "get_info":
            rep = {"status": "success", "wallet": {"address": wallet.adresse, "owner": wallet.nom, "balance": wallet.solde}}

        elif action == "receive":
            montant = req.get("amount")
            from_addr = req.get("from_address", "INCONNU")
            with lock:
                txn_id = wallet.recevoir(montant, from_addr)
                nouveau_solde = wallet.solde
            print(f"\n  📥 Reçu {float(montant):.2f} BKN de {from_addr} | {txn_id}")
            rep = {"status": "success", "message": f"Réception de {float(montant):.2f} BKN confirmée", "transaction_id": txn_id, "new_balance": nouveau_solde}

        else:
            rep = {"status": "error", "message": "Action inconnue."}

    except Exception as e:
        rep = {"status": "error", "message": str(e)}
    finally:
        conn.sendall(json.dumps(rep).encode())
        conn.close()


def main():
    print("\n" + "="*50)
    print("   🌐  SERVEUR DE WALLET BKN")
    print("="*50)

    nom = input("\n  Nom du propriétaire du wallet: ").strip() or "Alice"
    solde = float(input("  Solde initial (BKN): ").strip() or "1000")
    host = input("  Host (Enter = localhost): ").strip() or "localhost"
    port = int(input("  Port (Enter = 5555): ").strip() or "5555")

    wallet = Wallet(nom, solde)
    lock = threading.Lock()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)

    print(f"\n  🌐 Serveur BKN démarré sur {host}:{port}")
    print(f"  🏦 Wallet: {nom} | 💰 Solde: {solde:.2f} BKN")
    print("  En attente de connexions...\n")
    print("  Commandes: info | hist | quitter")

    def accepter():
        while True:
            try:
                srv.settimeout(1)
                conn, addr = srv.accept()
                print(f"\n  🔗 Connexion de {addr[0]}:{addr[1]}")
                threading.Thread(target=gerer_client, args=(conn, wallet, lock), daemon=True).start()
            except socket.timeout:
                continue
            except:
                break

    threading.Thread(target=accepter, daemon=True).start()

    while True:
        cmd = input("\n  [Serveur] > ").strip().lower()
        if cmd == "info":
            wallet.afficher()
        elif cmd == "hist":
            wallet.afficher_historique()
        elif cmd == "quitter":
            print("\n  👋 Arrêt du serveur.")
            srv.close()
            break

if __name__ == "__main__":
    main()
