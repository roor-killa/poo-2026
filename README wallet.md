# TP Crypto-monnaie BKN

## Présentation

Pour ce TP on devait créer un système de transfert de crypto-monnaie en Python en appliquant les concepts de la programmation orientée objet vus en cours (polymorphisme, encapsulation, abstraction).

Le système s'appelle **BKN (BoKryptoNou)**, la crypto de la Martinique 🇫🇷

---

## Fichiers du projet

- `wallet.py` : la classe Wallet qui représente un portefeuille
- `local_transfer.py` : partie 1, les transferts entre deux wallets sur le même terminal
- `network_server.py` : partie 2, le serveur qui attend les connexions
- `network_client.py` : partie 2, le client qui se connecte au serveur

---

## Comment lancer le projet

### Partie 1 — transferts locaux

```bash
python local_transfer.py
```

Deux wallets sont créés automatiquement (Alice avec 1000 BKN et Bob avec 500 BKN). Un menu s'affiche pour faire des transferts dans les deux sens et voir l'historique.

### Partie 2 — transferts réseau

Il faut ouvrir deux terminaux.

**Terminal 1 (le serveur) :**
```bash
python network_server.py
```
On rentre le nom du propriétaire, le solde de départ, et le port (par défaut 5555). Une fois lancé on peut taper des commandes :
- `info` pour voir le solde
- `hist` pour voir l'historique
- `send` pour envoyer des BKN au client connecté (bonus)
- `quit` pour arrêter

**Terminal 2 (le client) :**
```bash
python network_client.py
```
On rentre son nom, son solde, et le port d'écoute (par défaut 5556). Ensuite un menu permet de voir son wallet, son historique, ou d'envoyer des BKN au serveur.

---

## Bonus niveau 1 — transfert bidirectionnel

En bonus j'ai implémenté le transfert dans les deux sens, donc pas seulement client → serveur mais aussi serveur → client.

Pour ça j'ai rajouté un thread côté client qui tourne en arrière-plan et qui écoute sur un deuxième port (5556). Quand le serveur tape `send`, il se connecte sur ce port et envoie une requête JSON pour créditer le wallet du client.

Dans les deux sens, si quelque chose se passe mal côté réseau, le débit est annulé automatiquement pour ne pas perdre de BKN.

---

## Choix de conception

Le principal choix qu'on a fait c'est de séparer complètement la classe `Wallet` du code réseau. La classe Wallet ne sait pas du tout qu'il y a des sockets, elle gère juste les soldes et les transactions. C'est les fichiers server et client qui s'occupent du réseau et qui utilisent Wallet.

Pour la communication réseau on utilise du JSON sur TCP, avec trois types de messages : `get_info` pour récupérer les infos d'un wallet distant, `receive` pour recevoir des BKN depuis le client, et `receive_from_server` pour le sens inverse.

---

## Difficultés rencontrées

La partie la plus compliquée c'était de gérer le cas où la connexion tombe entre le moment où on débite le wallet local et le moment où l'autre wallet est crédité. Si on ne gère pas ce cas on peut perdre des BKN sans que personne ne les reçoive. J'ai réglé ça avec un système de rollback qui rembourse le débit si le crédit distant échoue.

Pour le bonus c'était compliqué de faire tourner le thread d'écoute en arrière-plan sans qu'il bloque le menu principal du client. J'ai utilisé `daemon=True` pour que le thread s'arrête automatiquement quand le programme principal se termine.

---

## Améliorations possibles

- Ajouter une authentification par mot de passe (bonus niveau 2)
- Faire une vraie mini blockchain avec hash des transactions (bonus niveau 3)
- Sauvegarder les wallets dans une base de données pour ne pas tout perdre quand on ferme le programme
- Ajouter une interface graphique
