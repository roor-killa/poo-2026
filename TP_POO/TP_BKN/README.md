Projet BKN - Système de Wallet (Local & Réseau)

Ce projet implémente un système de transfert de tokens BKN :
- Mode local (2 wallets sur un même terminal)
- Mode réseau (client ↔ serveur via sockets TCP)


Lancement du code :
1. Mode local avec      python local_transfert.py     directement dans la console

2. Mode Réseau
- Terminal 1 (Serveur)      python network_server.py    dans la console.
- Terminal 2 (Client)       python network_client.py    dans la console (certaines fonctionnalités ne fonctionneront pas si le serveur n'est pas lancé au préalable).