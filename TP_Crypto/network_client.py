import socket, json, datetime, uuid

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

    def debiter(self, montant):
        montant = float(montant)
        if montant <= 0:
            raise ValueError("Montant invalide.")
        if montant > self._solde:
            raise ValueError(f"Solde insuffisant : {self._solde:.2f} BKN disponibles.")
        self._solde -= montant
        self._enregistrer("ENVOI", -montant, "WALLET_DISTANT")

    def rembourser(self, montant):
        self._solde += montant
        self._enregistrer("REMBOURSEMENT", montant, "ECHEC_RESEAU")

    def _enregistrer(self, type_tx, montant, contrepartie):
        txn_id = "TXN-BKN-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:6].upper()
        self.historique.append({
            "txn_id": txn_id, "type": type_tx, "montant": montant,
            "contrepartie": contrepartie,
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "solde_apres": self._solde
        })

    def afficher(self):
        print(f"\n  👤 {self.nom} | Adresse: {self.adresse} | Solde: {self._solde:.2f} BKN")

    def afficher_historique(self):
        print(f"\n  📜 Historique de {self.nom} ({len(self.historique)} transaction(s))")
        for tx in self.historique:
            signe = "+" if tx["montant"] >= 0 else ""
            print(f"  [{tx['timestamp']}] {tx['type']} {signe}{tx['montant']:.2f} BKN | {tx['contrepartie']} | {tx['txn_id']}")


def envoyer_requete(host, port, requete):
    with socket.create_connection((host, port), timeout=10) as sock:
        sock.sendall(json.dumps(requete).encode())
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            try:
                json.loads(data.decode())
                break
            except:
                continue
    return json.loads(data.decode())


def main():
    print("\n" + "="*50)
    print("   🌐  CLIENT DE WALLET BKN")
    print("="*50)

    nom = input("\n  Votre nom: ").strip() or "Bob"
    solde = float(input("  Solde initial (BKN): ").strip() or "500")
    wallet = Wallet(nom, solde)

    print(f"\n  ✅ Wallet créé!\n     Adresse: {wallet.adresse}\n     Solde: {wallet.solde:.2f} BKN")

    while True:
        print("\n" + "="*50)
        print("  💎 CLIENT WALLET BKN")
        print("  1. Afficher mon wallet")
        print("  2. Afficher l'historique")
        print("  3. Obtenir infos d'un wallet distant")
        print("  4. Transférer des BKN à un wallet distant")
        print("  0. Quitter")
        print("="*50)

        choix = input("  👉 Votre choix: ").strip()

        if choix == "1":
            wallet.afficher()

        elif choix == "2":
            wallet.afficher_historique()

        elif choix == "3":
            host = input("  Host (Enter = localhost): ").strip() or "localhost"
            port = int(input("  Port (Enter = 5555): ").strip() or "5555")
            try:
                rep = envoyer_requete(host, port, {"action": "get_info"})
                if rep["status"] == "success":
                    w = rep["wallet"]
                    print(f"\n  🏦 Wallet distant: {w['owner']} | Adresse: {w['address']} | Solde: {w['balance']:.2f} BKN")
                else:
                    print(f"  ❌ {rep['message']}")
            except Exception as e:
                print(f"  ❌ Erreur réseau : {e}")

        elif choix == "4":
            print(f"\n  💸 Transfert de BKN vers un wallet distant")
            print(f"  Votre solde: {wallet.solde:.2f} BKN")
            host = input("  Host du serveur destinataire (Enter = localhost): ").strip() or "localhost"
            port = int(input("  Port (Enter = 5555): ").strip() or "5555")
            montant_str = input("  Montant à transférer (BKN): ").strip()

            try:
                montant = float(montant_str)
                print(f"\n  💸 Transfert de {montant:.2f} BKN en cours...")
                print(f"  🔗 Connexion à {host}:{port}...")

                rep_info = envoyer_requete(host, port, {"action": "get_info"})
                if rep_info["status"] != "success":
                    print(f"  ❌ {rep_info['message']}")
                    continue

                adresse_distante = rep_info["wallet"]["address"]
                print(f"  ✅ Connecté!\n  📍 Wallet distant: {adresse_distante}")

                wallet.debiter(montant)
                print(f"  ✅ Débit local effectué ({montant:.2f} BKN)")

                try:
                    rep = envoyer_requete(host, port, {"action": "receive", "amount": montant, "from_address": wallet.adresse})
                    if rep["status"] == "success":
                        print(f"  ✅ Crédit distant confirmé!")
                        print(f"     Transaction ID: {rep['transaction_id']}")
                        print(f"\n  ✅ Transfert de {montant:.2f} BKN réussi")
                        print(f"\n  📊 Nouveaux soldes:")
                        print(f"     Votre wallet: {wallet.solde:.2f} BKN")
                        print(f"     Wallet distant: {rep['new_balance']:.2f} BKN")
                    else:
                        wallet.rembourser(montant)
                        print(f"  ❌ {rep['message']} — Remboursement effectué.")
                except Exception as e:
                    wallet.rembourser(montant)
                    print(f"  ❌ Erreur réseau : {e} — Remboursement effectué.")

            except ValueError as e:
                print(f"  ❌ {e}")
            except Exception as e:
                print(f"  ❌ Erreur réseau : {e}")

        elif choix == "0":
            print("\n  👋 Au revoir ! 💎\n")
            break

        else:
            print("  ⚠️  Choix invalide.")

if __name__ == "__main__":
    main()
