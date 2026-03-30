"""
wallet.py - Classe Wallet pour le système de transfert BKN (BoKryptoNou)
"""

import time
import random
import string
from datetime import datetime


def generate_address(prefix: str) -> str:
    """Génère une adresse unique pour un wallet."""
    suffix = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}-{suffix}"


class Transaction:
    """Représente une transaction BKN."""

    def __init__(self, tx_type: str, amount: float, address: str, description: str = ""):
        self.tx_id = self._generate_tx_id()
        self.tx_type = tx_type          # "ENVOI" ou "RECEPTION"
        self.amount = amount
        self.address = address          # adresse source ou destination
        self.description = description
        self.timestamp = datetime.now()

    def _generate_tx_id(self) -> str:
        suffix = ''.join(random.choices(string.digits, k=3))
        return f"TXN-BKN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{suffix}"

    def __str__(self) -> str:
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        sign = "-" if self.tx_type == "ENVOI" else "+"
        desc = f" ({self.description})" if self.description else ""
        return (f"[{ts}] {self.tx_id}\n"
                f"   {self.tx_type}: {sign}{self.amount:.2f} BKN | "
                f"Adresse: {self.address}{desc}")


class Wallet:
    """
    Portefeuille électronique BKN.

    Attributs:
        address  (str)   : adresse unique du wallet (ex: BKN-SERVER-ALICE-001)
        owner    (str)   : nom du propriétaire
        balance  (float) : solde actuel en BKN
        history  (list)  : liste des transactions
    """

    def __init__(self, owner: str, initial_balance: float = 0.0, prefix: str = "BKN-LOCAL"):
        if initial_balance < 0:
            raise ValueError("Le solde initial ne peut pas être négatif.")
        self.owner = owner
        self.balance = float(initial_balance)
        self.address = generate_address(f"{prefix}-{owner.upper()}")
        self.history: list[Transaction] = []

    # ------------------------------------------------------------------
    # Méthodes principales
    # ------------------------------------------------------------------

    def envoyer(self, montant: float, destinataire: "Wallet") -> str:
        """
        Envoie des BKN vers un autre wallet local.

        Returns:
            transaction_id (str)

        Raises:
            ValueError si montant invalide ou solde insuffisant.
        """
        self._valider_montant(montant)
        if montant > self.balance:
            raise ValueError(
                f"Solde insuffisant. Disponible: {self.balance:.2f} BKN, "
                f"demandé: {montant:.2f} BKN."
            )

        self.balance -= montant
        tx = Transaction("ENVOI", montant, destinataire.address,
                         f"Vers {destinataire.owner}")
        self.history.append(tx)

        destinataire.recevoir(montant, self.address, self.owner)
        return tx.tx_id

    def recevoir(self, montant: float, from_address: str, from_owner: str = "") -> str:
        """
        Crédite le wallet d'un montant reçu.

        Returns:
            transaction_id (str)
        """
        self._valider_montant(montant)
        self.balance += montant
        desc = f"De {from_owner}" if from_owner else ""
        tx = Transaction("RECEPTION", montant, from_address, desc)
        self.history.append(tx)
        return tx.tx_id

    def consulter_historique(self) -> list[Transaction]:
        """Retourne la liste complète des transactions."""
        return list(self.history)

    def afficher_historique(self) -> None:
        """Affiche l'historique formaté dans le terminal."""
        print(f"\n📜 Historique de {self.owner} ({self.address})")
        print("─" * 65)
        if not self.history:
            print("   Aucune transaction.")
        else:
            for tx in self.history:
                print(tx)
        print("─" * 65)
        print(f"   Solde actuel : {self.balance:.2f} BKN\n")

    def get_info(self) -> dict:
        """Retourne un dictionnaire avec les informations du wallet (pour JSON)."""
        return {
            "address": self.address,
            "owner": self.owner,
            "balance": self.balance,
        }

    def __str__(self) -> str:
        return (f"🏦 Wallet BKN\n"
                f"   Propriétaire : {self.owner}\n"
                f"   Adresse      : {self.address}\n"
                f"   Solde        : {self.balance:.2f} BKN")

    # ------------------------------------------------------------------
    # Méthode privée utilitaire
    # ------------------------------------------------------------------

    @staticmethod
    def _valider_montant(montant: float) -> None:
        """Lève une ValueError si le montant est invalide."""
        if not isinstance(montant, (int, float)):
            raise ValueError("Le montant doit être un nombre.")
        if montant <= 0:
            raise ValueError("Le montant doit être strictement positif.")
