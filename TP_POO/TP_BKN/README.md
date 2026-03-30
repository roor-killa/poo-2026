Projet BKN - Système de Wallet (Local & Réseau)

Ce projet implémente un système de transfert de tokens BKN :
- Mode local (2 wallets sur un même terminal)
- Mode réseau (client ↔ serveur via sockets TCP)


Lancement :

1. Mode local
python local_transfert.py

2. Mode Réseau
Terminal 1 (Serveur)
python network_server.py

Terminal 2 (Client)
python network_client.py