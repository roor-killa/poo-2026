import uuid
import datetime


class Wallet:
    """Représente un portefeuille de crypto-monnaie BKN."""

    def __init__(self, proprietaire: str, solde_initial: float = 0.0, prefix: str = "BKN"):
        # Génération d'une adresse unique basée sur un identifiant aléatoire court
        self.adresse = f"{prefix}-{proprietaire.upper()}-{str(uuid.uuid4())[:3].upper()}"
        self.proprietaire = proprietaire
        self.solde = solde_initial
        self.historique = []  # Liste des transactions effectuées

    def envoyer(self, destinataire: "Wallet", montant: float) -> str:
        """Envoie des BKN vers un autre wallet. Retourne l'ID de transaction."""
        # Vérifications avant transfert
        if montant <= 0:
            raise ValueError("Le montant doit être supérieur à 0.")
        if montant > self.solde:
            raise ValueError(f"Solde insuffisant. Disponible : {self.solde:.2f} BKN")

        # Débit de l'expéditeur
        self.solde -= montant

        # Crédit du destinataire
        destinataire.recevoir(montant, self.adresse)

        # Création de la transaction
        tx_id = self._generer_tx_id()
        self.historique.append({
            "type": "ENVOI",
            "montant": montant,
            "vers": destinataire.adresse,
            "tx_id": tx_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return tx_id

    def recevoir(self, montant: float, depuis_adresse: str) -> None:
        """Crédite le wallet d'un montant reçu."""
        self.solde += montant
        self.historique.append({
            "type": "RECEPTION",
            "montant": montant,
            "de": depuis_adresse,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def afficher_historique(self) -> None:
        """Affiche toutes les transactions du wallet."""
        print(f"\n📜 Historique de {self.proprietaire} ({self.adresse})")
        if not self.historique:
            print("   Aucune transaction pour le moment.")
            return
        for tx in self.historique:
            if tx["type"] == "ENVOI":
                print(f"  ↗ ENVOI    {tx['montant']:.2f} BKN → {tx['vers']}  [{tx['date']}]")
            else:
                print(f"  ↙ REÇU    {tx['montant']:.2f} BKN ← {tx['de']}  [{tx['date']}]")

    def afficher_info(self) -> None:
        """Affiche les informations du wallet."""
        print(f"\n🏦 WALLET BKN - {self.proprietaire}")
        print(f"   Adresse : {self.adresse}")
        print(f"   Solde   : {self.solde:.2f} BKN")

    def _generer_tx_id(self) -> str:
        """Génère un identifiant unique pour une transaction."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        suffix = str(uuid.uuid4().int)[:3]
        return f"TXN-BKN-{timestamp}-{suffix}"
