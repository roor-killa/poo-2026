import datetime
import uuid

def is_valid_address(address):
    return address.startswith("BKN-")

class Wallet:
    def __init__(self, owner, balance, prefix="BKN"):
        self.owner = owner
        self.balance = float(balance)
        self.address = f"{prefix}-{owner.upper()}-{str(uuid.uuid4())[:6]}"
        self.history = []

    def send(self, amount, receiver):
        if amount <= 0:
            raise ValueError("Montant invalide")

        if self.balance < amount:
            raise ValueError("Solde insuffisant")

        if not is_valid_address(receiver.address):
            raise ValueError("Adresse invalide")

        self.balance -= amount
        receiver.receive(amount, self.address)

        txn_id = self._generate_txn()
        self._add_history("SEND", amount, receiver.address, txn_id)

        return txn_id

    def receive(self, amount, sender_address):
        self.balance += amount

        txn_id = self._generate_txn()
        self._add_history("RECEIVE", amount, sender_address, txn_id)

        return txn_id

    def _generate_txn(self):
        return f"TXN-BKN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:3]}"

    def _add_history(self, type_txn, amount, other, txn_id):
        self.history.append({
            "type": type_txn,
            "amount": amount,
            "other": other,
            "id": txn_id
        })

    def show_info(self):
        print(f"\n🏦 WALLET BKN - {self.owner}")
        print(f"Adresse: {self.address}")
        print(f"Solde: {self.balance:.2f} BKN")

    def show_history(self):
        print(f"\n📜 Historique de {self.owner}")
        if not self.history:
            print("Aucune transaction.")
            return
        for h in self.history:
            print(h)