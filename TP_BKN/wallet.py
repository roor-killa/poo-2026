import datetime
import random


class Wallet:

    def __init__(self, owner, balance=0, prefix="BKN"):
        self.owner = owner
        self.balance = float(balance)

        # generation d'une adresse unique
        random_id = random.randint(100, 999)
        self.address = f"{prefix}-{owner.upper()}-{random_id}"

        # historique des transactions
        self.history = []

    # afficher les informations du wallet
    def get_info(self):
        return {
            "address": self.address,
            "owner": self.owner,
            "balance": self.balance
        }

    # recevoir de la crypto
    def receive(self, amount, from_address="UNKNOWN"):

        if amount <= 0:
            raise ValueError("Le montant doit etre positif")

        self.balance += amount

        txn_id = self.generate_transaction_id()

        transaction = {
            "id": txn_id,
            "type": "receive",
            "amount": amount,
            "from": from_address,
            "to": self.address,
            "date": str(datetime.datetime.now())
        }

        self.history.append(transaction)

        return txn_id

    # envoyer de la crypto
    def send(self, amount, to_address):

        if amount <= 0:
            raise ValueError("Le montant doit etre positif")

        if amount > self.balance:
            raise ValueError("Solde insuffisant")

        self.balance -= amount

        txn_id = self.generate_transaction_id()

        transaction = {
            "id": txn_id,
            "type": "send",
            "amount": amount,
            "from": self.address,
            "to": to_address,
            "date": str(datetime.datetime.now())
        }

        self.history.append(transaction)

        return txn_id

    # generer un ID de transaction
    def generate_transaction_id(self):

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        rand = random.randint(100, 999)

        return f"TXN-BKN-{timestamp}-{rand}"

    # afficher l'historique
    def show_history(self):

        if not self.history:
            print("Aucune transaction.")

        for txn in self.history:
            print(txn)
