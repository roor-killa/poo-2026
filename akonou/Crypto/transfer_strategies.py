"""
transfer_strategies.py — Strategies de transfert pour illustrer le polymorphisme.
"""

from abc import ABC, abstractmethod
from typing import Callable

from wallet import Wallet, InvalidAmountError, InsufficientFundsError


class TransferStrategy(ABC):
    """Interface commune des strategies de transfert."""

    @abstractmethod
    def transfer(self, sender: Wallet, amount: float, **kwargs) -> dict:
        """Execute un transfert et retourne un resultat structure."""


class LocalTransferStrategy(TransferStrategy):
    """Transfert local entre deux instances Wallet."""

    def transfer(self, sender: Wallet, amount: float, **kwargs) -> dict:
        recipient = kwargs.get("recipient")
        if not isinstance(recipient, Wallet):
            raise ValueError("Le destinataire local est invalide.")

        tx_id = sender.send(amount, recipient)
        return {
            "status": "success",
            "transaction_id": tx_id,
            "sender_balance": sender.balance,
            "recipient_balance": recipient.balance,
            "recipient_address": recipient.address,
        }


class NetworkTransferStrategy(TransferStrategy):
    """Transfert vers un wallet distant via requetes JSON."""

    def __init__(self, request_sender: Callable[[str, int, dict], dict]):
        self.request_sender = request_sender

    def transfer(self, sender: Wallet, amount: float, **kwargs) -> dict:
        host = kwargs.get("host")
        port = kwargs.get("port")
        if not host or not isinstance(port, int):
            raise ValueError("Host/port invalides pour un transfert reseau.")

        if amount <= 0:
            raise InvalidAmountError("Le montant doit etre strictement positif.")
        if amount > sender.balance:
            raise InsufficientFundsError(
                f"Solde insuffisant : {sender.balance:.2f} BKN disponibles, {amount:.2f} BKN requis."
            )

        remote_info_resp = self.request_sender(host, port, {"action": "get_info"})
        if remote_info_resp.get("status") != "success":
            raise RuntimeError(remote_info_resp.get("message", "Erreur get_info distante."))

        remote_wallet = remote_info_resp.get("wallet", {})
        remote_address = remote_wallet.get("address", "N/A")

        response = self.request_sender(
            host,
            port,
            {
                "action": "receive",
                "amount": amount,
                "from_address": sender.address,
            },
        )

        if response.get("status") != "success":
            raise RuntimeError(response.get("message", "Transfert refuse par le serveur."))

        sender.balance -= amount
        return {
            "status": "success",
            "transaction_id": response.get("transaction_id", "N/A"),
            "remote_address": remote_address,
            "sender_balance": sender.balance,
            "remote_balance": response.get("new_balance", 0.0),
        }
