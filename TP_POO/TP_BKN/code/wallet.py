import datetime
import uuid

class Wallet:
    #initialisation
    def __init__(self, address, owner, balance=0):
        self.address = address
        self.owner = owner
        self.balance = balance
        self.history = []

    # methodes
    def send(self, amount, to_wallet):   #envoyer une somme
        if amount <= 0:
            raise ValueError("Montant invalide")
        if amount > self.balance:
            raise ValueError("Solde insuffisant")

        self.balance -= amount
        tx_id = self._generate_tx_id()

        tx = {
            "id": tx_id,
            "type": "send",
            "amount": amount,
            "to": to_wallet.address,
            "date": str(datetime.datetime.now())
        }

        self.history.append(tx)
        to_wallet.receive(amount, self.address, tx_id)

        return tx_id

    def receive(self, amount, from_address, tx_id=None):    #reçevoir une somme
        self.balance += amount

        tx = {
            "id": tx_id or self._generate_tx_id(),
            "type": "receive",
            "amount": amount,
            "from": from_address,
            "date": str(datetime.datetime.now())
        }

        self.history.append(tx)

    def _generate_tx_id(self):  #code de transaction
        return f"TXN-BKN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:4]}"

    def show_info(self):
        print(f"\n {self.owner}")
        print(f"Adresse: {self.address}")
        print(f"Solde: {self.balance:.2f} BKN")

    def show_history(self):
        print("\n Historique:")
        if not self.history:
            print("Aucune transaction.")
        for tx in self.history:
            print(tx)