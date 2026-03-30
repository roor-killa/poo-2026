## 🚀 Comment lancer le projet

### Partie 1 : Mode Local
Pour tester les transferts sur un seul terminal :
1. Ouvrir un terminal dans le dossier du projet.
2. Exécutez la commande suivante :
   ```bash
   "python local_transfer.py"  OU "py local_transfer.py"

### Partie 2 : Mode Reseau
Pour tester le transfert entre deux portefeuilles via le réseau :

Lancer le Serveur (Le destinataire) :
Exécutez : "python network_server.py"
Suivez les instructions (Nom : Alice, Solde : 1000). Le serveur passera en mode "Écoute".

Lancer le Client (L'expéditeur) :
Ouvrez un deuxième terminal (sans fermer le premier).
Exécutez : "python network_client.py"
Suivez les instructions (Nom : Bob).
Choisissez l'option 2 pour envoyer un montant au  serveur.

Vérification :
Une fois le message de réussite affiché sur le client, retournez sur le terminal du Serveur.
Tapez info pour voir que le solde a bien augmenté grâce au message JSON reçu.
