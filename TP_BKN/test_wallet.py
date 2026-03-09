from wallet import Wallet

wallet1 = Wallet("Alice", 1000)
wallet2 = Wallet("Bob", 500)

wallet1.send(100, wallet2.address)
wallet2.receive(100, wallet1.address)

print(wallet1.get_info())
print(wallet2.get_info())

wallet1.show_history()
wallet2.show_history()
