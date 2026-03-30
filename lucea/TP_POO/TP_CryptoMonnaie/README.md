# Système de Transfert de Crypto-monnaie BKN (BoKryptoNou)

Ce projet implémente un système de transfert de crypto-monnaie BKN avec mode local et mode réseau (client/serveur) en Python.
Il permet de créer des wallets, effectuer des transferts, consulter l’historique et gérer des transactions sur un terminal local ou via TCP.

# Contenu du projet
- wallet.py : Classe Wallet gérant les soldes et l’historique des transactions
- local_transfer.py : Application locale pour tester les transferts entre deux wallets
- network_server.py : Serveur TCP qui gère un wallet et reçoit des transferts distants
- network_client.py : Client TCP permettant d’envoyer des BKN à un wallet distant

# Comment lancer chaque partie

1️⃣ Transfert local

1. Ouvrir un terminal dans le dossier contenant local_transfer.py
2. Lancer le programme (python local_transfer.py)
3. Suivre le menu pour :
   - Afficher les wallets (1)
   - Transférer BKN Wallet1 → Wallet2 (2)
   - Transférer BKN Wallet2 → Wallet1 (3)
   - Consulter l’historique du Wallet1 (4)
   - Consulter l’historique du Wallet2 (5)
   - Quitter (0)

2️⃣ Serveur réseau

1. Ouvrir un terminal
2. Placer le terminal dans le dossier contenant network_server.py
3. Lancer :
   - python network_server.py
4. Entrer le nom du wallet, le solde initial, le host (Enter = localhost) et le port (Enter = 5555)
5. Le serveur reste actif et accepte les connexions clients.
Les commandes locales du serveur :
- info → afficher l’état du wallet
- hist → afficher l’historique des transactions
- quit → arrêter le serveur

3️⃣ Client réseau

1. Ouvrir un autre terminal
2. Placer le terminal dans le dossier contenant network_client.py
3. Lancer :
   - python network_client.py
4. Entrer le nom du wallet et le solde initial
Suivre le menu pour :
- Afficher son wallet (1)
- Afficher l’historique (2)
- Obtenir infos d’un wallet distant (3)
- Transférer des BKN à un wallet distant (4)
- Quitter (0)

Pour un transfert, entrer le host (Enter = localhost), le port (Enter = 5555) et le montant.
Le client débitera le wallet local et le serveur créditera le wallet distant, avec confirmation de la transaction.

# Choix de conception

- POO (Programmation orientée objet) : Une seule classe Wallet pour gérer solde et historique.
- Abstraction des transactions : méthodes envoyer() et recevoir() pour encapsuler la logique.
- Transferts locaux et distants : le code est séparé pour tester les fonctionnalités réseau sans impacter le local.
- Sockets TCP + JSON : communication client/serveur simple et structurée.
- Threading serveur : permet d’accepter plusieurs clients sans bloquer l’interface serveur.
- IDs de transaction uniques générés avec timestamp + nombre aléatoire.

# Difficultés rencontrées

- Gestion du threading pour le serveur afin de ne pas bloquer l’interface console.
- Conversion du port en int et validation des entrées utilisateur.
- Synchronisation des transactions locales et distantes pour éviter les incohérences.
- Gestion des exceptions réseau (client ou serveur qui se déconnecte brutalement).
- Génération de transaction ID unique et lisible.

# Améliorations possibles

- Interface graphique pour rendre l’expérience plus intuitive (Tkinter, PyQt).
- Transferts bidirectionnels multi-clients avec enregistrement de l’historique serveur.
- Validation serveur du montant reçu pour éviter la fraude côté client.
- Sérialisation JSON plus riche pour inclure l’adresse du destinataire et le timestamp exact.
- Logs persistants pour garder l’historique des transactions même après fermeture du serveur.
- Cryptographie (signature des transactions) pour sécuriser les transferts.
- Tests unitaires pour vérifier les méthodes envoyer() et recevoir().