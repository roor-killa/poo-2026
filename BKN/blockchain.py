import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        last = self.get_last_block()
        block = Block(len(self.chain), transactions, last.hash)
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != prev.hash:
                return False

        return True