# BKN Project

## Lancement
Partie 1 : Transferts locaux

Dans le terminal :

python local_transfer.py

Fonctionnalités :

Affichage des wallets
Transfert entre deux wallets (wallet 1 ↔ wallet 2)
Historique des transactions
Gestion des erreurs (solde insuffisant, montant invalide)

Partie 2 : Transferts réseau

Étape 1 : Lancer le serveur dans un premier terminal :

python network_server.py

Entrées demandées :

Nom du propriétaire
Solde initial
Host (laisser vide pour localhost)
Port (laisser vide pour 5555)

Étape 2 : Lancer le client dans un deuxième terminal :

python network_client.py

Fonctionnalités :

Consulter son wallet
Voir l’historique
Obtenir les informations d’un wallet distant
Envoyer des BKN vers le serveur

### Local
python local_transfer.py

### Réseau
Terminal 1:
python network_server.py

Terminal 2:
python network_client.py