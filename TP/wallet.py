import uuid
from datetime import datetime


class Wallet:
    def __init__(self, owner: str, balance: float = 0.0, prefix: str = "USER"):
        # stocke le nom du propriétaire
        self.owner = owner

        # stocke le solde actuel
        self.balance = float(balance)

        # crée une adresse unique pour le wallet
        self.address = self.generate_address(prefix)

        # stocke lhistorique des transactions
        self.history = []

    def generate_address(self, prefix: str) -> str:
        # crée une adresse unique de wallet
        short_id = str(uuid.uuid4().int)[:3]
        owner_part = self.owner.upper().replace(" ", "-")
        return f"BKN-{prefix}-{owner_part}-{short_id}"

    def generate_transaction_id(self) -> str:
        # crée un identifiant unique de transaction
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        short_id = str(uuid.uuid4().int)[:3]
        return f"TXN-BKN-{now}-{short_id}"

    def send(self, amount: float, to_address: str):
        # vérifie que le montant est valide
        if amount <= 0:
            raise ValueError("le montant doit être supérieur à zéro")

        # vérifie que le solde est suffisant
        if amount > self.balance:
            raise ValueError("solde insuffisant")

        # débite le wallet
        self.balance -= amount

        # crée la transaction
        transaction_id = self.generate_transaction_id()

        # ajoute la transaction à lhistorique
        self.history.append({
            "transaction_id": transaction_id,
            "type": "send",
            "amount": amount,
            "from": self.address,
            "to": to_address,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return transaction_id

    def receive(self, amount: float, from_address: str):
        # vérifie que le montant est valide
        if amount <= 0:
            raise ValueError("le montant doit être supérieur à zéro")

        # crédite le wallet
        self.balance += amount

        # crée la transaction
        transaction_id = self.generate_transaction_id()

        # ajoute la transaction à lhistorique
        self.history.append({
            "transaction_id": transaction_id,
            "type": "receive",
            "amount": amount,
            "from": from_address,
            "to": self.address,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return transaction_id

    def get_info(self) -> dict:
        # retourne les informations principales du wallet
        return {
            "address": self.address,
            "owner": self.owner,
            "balance": self.balance
        }

    def get_history(self) -> list:
        # retourne lhistorique complet
        return self.history

    def show_info(self):
        # affiche les informations du wallet
        print(f"🏦 WALLET BKN - {self.owner}")
        print(f"Adresse: {self.address}")
        print(f"Solde: {self.balance:.2f} BKN")

    def show_history(self):
        # affiche lhistorique des transactions
        print(f"\n📜 HISTORIQUE DE {self.owner}")

        if not self.history:
            print("aucune transaction")
            return

        for transaction in self.history:
            print("-" * 40)
            print(f"ID: {transaction['transaction_id']}")
            print(f"Type: {transaction['type']}")
            print(f"Montant: {transaction['amount']:.2f} BKN")
            print(f"De: {transaction['from']}")
            print(f"Vers: {transaction['to']}")
            print(f"Date: {transaction['date']}")


from wallet import Wallet

w1 = Wallet("Alice", 1000, "SERVER")
w2 = Wallet("Bob", 500, "CLIENT")

tx1 = w1.send(100, w2.address)
tx2 = w2.receive(100, w1.address)

w1.show_info()
w2.show_info()
w1.show_history()
w2.show_history()