LISTE DE TESTS:

PS C:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TP BKN> python network_server.py
🌐 SERVEUR DE WALLET BKN
Nom du propriétaire du wallet : Alice
Solde initial (BKN) : 1000
Host (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Commandes locales : info | hist | quit
[Serveur] > 🌐 Serveur BKN démarré sur localhost:5555
🏦 Wallet : Alice
💰 Solde initial : 1000.00 BKN
En attente de connexions...

info

🏦 WALLET BKN - Alice
   Adresse : BKN-SERVER-ALICE-881
   Solde   : 1000.00 BKN
[Serveur] >


TEST CLIENT:

PS C:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TP BKN> python network_client.py
🌐 CLIENT DE WALLET BKN
Votre nom : Bob 
Solde initial (BKN) : 500

✅ Wallet créé !
   Adresse : BKN-CLIENT-BOB-770
   Solde   : 500.00 BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 500.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 100
Adresse distante : BKN-SERVER-ALICE-881
Success! ID transaction: TXN-BKN-20260330163338-714
Votre nouveau solde est de: 400.00 BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 3
Entrez le hostlocalhost
Entrez le port:5555

🔍 Récupération des infos du wallet distant (localhost:5555)...

 Wallet
Nom : Alice
Adresse : BKN-SERVER-ALICE-881
Solde : 1100.00BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 1

🏦 WALLET BKN - Bob
   Adresse : BKN-CLIENT-BOB-770
   Solde   : 400.00 BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 2

📜 Historique des transactions — Bob
   (aucune transaction)

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix :


CONFIRMATION SERVERSIDE du credit envoiyée par BOB:

PS C:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TP BKN> python network_server.py
🌐 SERVEUR DE WALLET BKN
Nom du propriétaire du wallet : Alice
Solde initial (BKN) : 1000
Host (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Commandes locales : info | hist | quit
[Serveur] > 🌐 Serveur BKN démarré sur localhost:5555
🏦 Wallet : Alice
💰 Solde initial : 1000.00 BKN
En attente de connexions...

info

🏦 WALLET BKN - Alice
   Adresse : BKN-SERVER-ALICE-881
   Solde   : 1000.00 BKN
[Serveur] >
🔗 Connexion de ('127.0.0.1', 49171)

🔗 Connexion de ('127.0.0.1', 49172)

🔗 Connexion de ('127.0.0.1', 62594)
hist

📜 Historique des transactions — Alice
   [2026-03-30 16:33:38] +100.00 BKN | CREDIT | BKN-CLIENT-BOB-770 | TXN-BKN-20260330163338-714
[Serveur] > info

🏦 WALLET BKN - Alice
   Adresse : BKN-SERVER-ALICE-881
   Solde   : 1100.00 BKN
[Serveur] >



### Partie 1
- [ ] Transfert avec solde suffisant
💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 500.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 100
Adresse distante : BKN-SERVER-ALICE-881
Success! ID transaction: TXN-BKN-20260330163338-714
Votre nouveau solde est de: 400.00 BKN


- [ ] Transfert avec solde insuffisant
 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 400.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 5000
Adresse distante : BKN-SERVER-ALICE-881
Montant invalide ou solde insuffisant.


- [ ] Transfert d'un montant négatif

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 400.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : -300
Adresse distante : BKN-SERVER-ALICE-881
Montant invalide ou solde insuffisant.

- [ ] Transfert de 0 BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 400.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 0
Adresse distante : BKN-SERVER-ALICE-881
Montant invalide ou solde insuffisant.


- [ ] Affichage de l'historique après plusieurs transferts

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 2

📜 Historique des transactions — Bob
   [2026-03-30 16:53:10] -299.00 BKN | DEBIT  | BKN-SERVER-ALICE-653 | TXN-BKN-20260330165310-131
   [2026-03-30 16:53:29] -23.00 BKN | DEBIT  | BKN-SERVER-ALICE-653 | TXN-BKN-20260330165329-307



### Partie 2
- [ ] Connexion au serveur

PS C:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TP BKN> & C:/Users/steph/AppData/Local/Python/pythoncore-3.14-64/python.exe "c:/Users/steph/OneDrive/Desktop/POOCours/poo-2026/TP BKN/network_server.py"
🌐 SERVEUR DE WALLET BKN
Nom du propriétaire du wallet : Alice
Solde initial (BKN) : 1000
Host (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Commandes locales : info | hist | quit
[Serveur] > 🌐 Serveur BKN démarré sur localhost:5555
🏦 Wallet : Alice
💰 Solde initial : 1000.00 BKN
En attente de connexions...

cd "c:/Users/steph/OneDrive/Desktop/POOCours/poo-2026/TP BKN"
Commandes disponibles : info | hist | quit
[Serveur] > & C:/Users/steph/AppData/Local/Python/pythoncore-3.14-64/python.exe "c:/Users/steph/OneDrive/Desktop/POOCours/poo-2026/TP BKN/network_client.py"
Commandes disponibles : info | hist | quit
[Serveur] >
🔗 Connexion de ('127.0.0.1', 52093)

🔗 Connexion de ('127.0.0.1', 52094)

🔗 Connexion de ('127.0.0.1', 52095)

🔗 Connexion de ('127.0.0.1', 52096)

### Partie 1
- [ ] Transfert avec solde suffisant
- [ ] Transfert avec solde insuffisant
- [ ] Transfert d'un montant négatif
- [ ] Transfert de 0 BKN
- [ ] Affichage de l'historique après plusieurs transferts

### Partie 2
- [ ] Connexion au serveur

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 3
Entrez le hostlocalhost
Entrez le port:5555

🔍 Récupération des infos du wallet distant (localhost:5555)...

 Wallet
Nom : Alice
Adresse : BKN-SERVER-ALICE-108
Solde : 2000.00BKN
------------------------------------------------Server------------------------------------------------------
PS C:\Users\steph\OneDrive\Desktop\POOCours\poo-2026\TP BKN> & C:/Users/steph/AppData/Local/Python/pythoncore-3.14-64/python.exe "c:/Users/steph/OneDrive/Desktop/POOCours/poo-2026/TP BKN/network_server.py"
🌐 SERVEUR DE WALLET BKN
Nom du propriétaire du wallet : Alice
Solde initial (BKN) : 2000
Host (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Commandes locales : info | hist | quit
[Serveur] > 🌐 Serveur BKN démarré sur localhost:5555
🏦 Wallet : Alice
💰 Solde initial : 2000.00 BKN
En attente de connexions...


🔗 Connexion de ('127.0.0.1', 52274)

- [ ] Récupération des infos du wallet distant

 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 3
Entrez le hostlocalhost
Entrez le port:5555

🔍 Récupération des infos du wallet distant (localhost:5555)...

 Wallet
Nom : Alice
Adresse : BKN-SERVER-ALICE-653
Solde : 1322.00BKN


- [ ] Transfert avec solde suffisant
💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 1000.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 100
Adresse distante : BKN-SERVER-ALICE-108
Success! ID transaction: TXN-BKN-20260330172430-899
Votre nouveau solde est de: 900.00 BKN
-------------------------------Server-------------------------------------------
🏦 WALLET BKN - Alice
   Adresse : BKN-SERVER-ALICE-108
   Solde   : 2100.00 BKN
[Serveur] > hist

📜 Historique des transactions — Alice
   [2026-03-30 17:24:30] +100.00 BKN | CREDIT | BKN-CLIENT-BOB-527 | TXN-BKN-20260330172430-899
[Serveur] >

- [ ] Transfert avec solde insuffisant
 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix : 4

💸 Transfert de BKN vers un wallet distant
   Votre solde : 900.00 BKN
Host du serveur destinataire (Entrée = localhost) : localhost
Port (Entrée = 5555) : 5555
Montant à transférer (BKN) : 10000
Adresse distante : BKN-SERVER-ALICE-108
Montant invalide ou solde insuffisant.

- [ ] Gestion de la déconnexion du serveur
[Serveur] > quit
🛑 Arrêt du serveur.
- [ ] Timeout de connexion
- [ ] Port déjà utilisé
