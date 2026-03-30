"""
wallet.py — Classe Wallet pour le système BKN (BoKryptoNou)

Fichier FOURNI aux étudiants. Vous pouvez le lire et l'améliorer,
mais il est déjà fonctionnel pour démarrer les parties 1 et 2.
"""

import random
from datetime import datetime


class InsufficientFundsError(Exception):
    """Levée quand le solde est insuffisant pour un transfert."""
    pass


class InvalidAmountError(Exception):
    """Levée quand le montant est invalide (négatif ou nul)."""
    pass


class Wallet:
    """
    Portefeuille de crypto-monnaie BKN.

    Attributs
    ---------
    address : str
        Adresse unique du wallet (ex: BKN-CLIENT-Alice-742)
    owner : str
        Nom du propriétaire
    balance : float
        Solde courant en BKN
    transactions : list[dict]
        Historique des transactions
    """

    def __init__(self, owner: str, initial_balance: float = 0.0, prefix: str = "LOCAL"):
        if initial_balance < 0:
            raise InvalidAmountError("Le solde initial ne peut pas être négatif.")
        self.owner = owner
        self.balance = float(initial_balance)
        self.address = f"BKN-{prefix}-{owner.upper()}-{random.randint(100, 999)}"
        self.transactions: list[dict] = []

    # ------------------------------------------------------------------
    # Méthodes publiques
    # ------------------------------------------------------------------

    def send(self, amount: float, to_wallet: "Wallet") -> str:
        """
        Envoie `amount` BKN vers `to_wallet`.

        Returns
        -------
        str
            Identifiant de la transaction (TXN-BKN-...)

        Raises
        ------
        InvalidAmountError
            Si le montant est <= 0
        InsufficientFundsError
            Si le solde est insuffisant
        """
        self._validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Solde insuffisant : {self.balance:.2f} BKN disponibles, "
                f"{amount:.2f} BKN requis."
            )

        tx_id = self._generate_tx_id()
        self.balance -= amount
        to_wallet.receive(amount, from_address=self.address, tx_id=tx_id)

        self._record_transaction(
            tx_id=tx_id,
            kind="DEBIT",
            amount=amount,
            counterpart=to_wallet.address,
        )
        return tx_id

    def receive(self, amount: float, from_address: str = "UNKNOWN", tx_id: str = None) -> str:
        """
        Crédite `amount` BKN sur ce wallet.

        Returns
        -------
        str
            Identifiant de la transaction
        """
        self._validate_amount(amount)
        if tx_id is None:
            tx_id = self._generate_tx_id()
        self.balance += amount
        self._record_transaction(
            tx_id=tx_id,
            kind="CREDIT",
            amount=amount,
            counterpart=from_address,
        )
        return tx_id

    def get_history(self) -> list[dict]:
        """Retourne une copie de l'historique des transactions."""
        return list(self.transactions)

    def display_info(self) -> None:
        """Affiche les informations du wallet dans la console."""
        print(f"\n🏦 WALLET BKN - {self.owner}")
        print(f"   Adresse : {self.address}")
        print(f"   Solde   : {self.balance:.2f} BKN")

    def display_history(self) -> None:
        """Affiche l'historique des transactions dans la console."""
        print(f"\n📜 Historique des transactions — {self.owner}")
        if not self.transactions:
            print("   (aucune transaction)")
            return
        for tx in self.transactions:
            sign = "+" if tx["kind"] == "CREDIT" else "-"
            print(
                f"   [{tx['date']}] {sign}{tx['amount']:.2f} BKN "
                f"| {tx['kind']:6s} | {tx['counterpart']} "
                f"| {tx['tx_id']}"
            )

    def to_dict(self) -> dict:
        """Sérialise le wallet en dictionnaire (utile pour JSON réseau)."""
        return {
            "address": self.address,
            "owner": self.owner,
            "balance": self.balance,
        }

    # ------------------------------------------------------------------
    # Méthodes privées
    # ------------------------------------------------------------------

    def _validate_amount(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise InvalidAmountError("Le montant doit être un nombre.")
        if amount <= 0:
            raise InvalidAmountError("Le montant doit être strictement positif.")

    def _generate_tx_id(self) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        suffix = random.randint(100, 999)
        return f"TXN-BKN-{ts}-{suffix}"

    def _record_transaction(
        self, tx_id: str, kind: str, amount: float, counterpart: str
    ) -> None:
        self.transactions.append(
            {
                "tx_id": tx_id,
                "kind": kind,
                "amount": amount,
                "counterpart": counterpart,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def __repr__(self) -> str:
        return f"Wallet({self.owner!r}, balance={self.balance:.2f})"
