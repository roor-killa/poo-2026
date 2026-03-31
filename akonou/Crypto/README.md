# Systeme de Transfert de Crypto-monnaie BKN

Projet POO  avec deux modes:
- Partie 1: transferts locaux entre deux wallets
- Partie 2: transferts reseau client/serveur via sockets TCP + JSON

## 1) Structure du dossier

- wallet.py: classe Wallet, exceptions metier, historique, validation des montants
- transfer_strategies.py: interface polymorphe TransferStrategy et strategies Local/Network
- local_transfer.py: menu local, transferts Wallet1 <-> Wallet2
- network_server.py: serveur TCP, traitement des actions JSON get_info / receive
- network_client.py: client TCP, consultation distante et transfert vers serveur

## 2) Prerequis

- Python 3.10+ (teste dans un environnement virtuel local)

Optionnel (Windows PowerShell):

1. Activer l environnement virtuel:

   .\.venv\Scripts\Activate.ps1

2. Se placer dans le dossier Crypto:

   cd .\Crypto

## 3) Lancement

### Partie 1 - Mode local

Commande:

python local_transfer.py

Fonctions disponibles:
- Afficher les deux wallets
- Transferer Wallet1 -> Wallet2
- Transferer Wallet2 -> Wallet1
- Afficher les historiques

### Partie 2 - Mode reseau

Ouvrir deux terminaux.

Terminal 1 (serveur):

python network_server.py

Terminal 2 (client):

python network_client.py

Flux principal:
- Le client peut demander les infos du wallet distant (action get_info)
- Le client peut transferer des BKN vers le serveur (action receive)
- Si le serveur confirme, le client debite son wallet local

## 4) Protocole JSON

### Demande d informations

Client -> Serveur:

{
  "action": "get_info"
}

Serveur -> Client:

{
  "status": "success",
  "wallet": {
    "address": "BKN-SERVER-...",
    "owner": "Alice",
    "balance": 1000.0
  }
}

### Reception de BKN cote serveur

Client -> Serveur:

{
  "action": "receive",
  "amount": 100.0,
  "from_address": "BKN-CLIENT-..."
}

Serveur -> Client:

{
  "status": "success",
  "message": "Reception de 100.0 BKN confirmee",
  "transaction_id": "TXN-BKN-...",
  "new_balance": 1100.0
}

## 5) Choix de conception

- Encapsulation:
  - La logique metier du solde est concentree dans Wallet (send, receive, _validate_amount).
- Abstraction:
  - Les scripts local et reseau consomment la meme interface Wallet (send, receive, display_info, display_history).
- Composition:
  - Le client et le serveur composent un objet Wallet avec des composants reseau (socket + JSON).
- Concurrence:
  - Le serveur accepte plusieurs clients grace a un thread daemon par connexion.
- Robustesse:
  - Erreurs metier capturees (InvalidAmountError, InsufficientFundsError).
  - Erreurs reseau capturees (timeout, connexion refusee).
  - Gestion JSON invalide cote serveur et client.

## 6) Verification des objectifs

Objectifs fonctionnels couverts:
- Creation de wallets: OK
- Transferts locaux: OK
- Transferts reseau Client -> Serveur: OK
- Historique des transactions: OK
- Verification et mise a jour des soldes: OK

Competences techniques couvertes:
- Sockets Python TCP: OK
- JSON (serialisation/deserialisation): OK
- Gestion d etat transactionnel: OK
- Threads cote serveur: OK
- Gestion des erreurs et cas limites: OK

Remarque POO (polymorphisme):
- Le projet utilise une interface commune TransferStrategy avec deux implementations:
  - LocalTransferStrategy pour les transferts locaux Wallet -> Wallet.
  - NetworkTransferStrategy pour les transferts client -> serveur via JSON.
- Le code client local et reseau manipule ces objets via la meme methode transfer(...), ce qui materialise le polymorphisme.

## 7) Difficultes rencontrees

- Conserver la coherence des soldes entre client et serveur en cas d erreur reseau.
- Decider du moment du debit local: ici, debit local uniquement apres confirmation distante.
- Gestions des saisies utilisateur (montant/port invalides).

## 8) Ameliorations possibles

- Validation stricte du format d adresse wallet.
- Confirmation utilisateur avant transfert.
- Journalisation fichier (logs) des transactions reseau.
- Authentification simple par mot de passe.
- Signature des transactions.

## 9) Plan de tests conseille

Partie 1:
- Transfert avec solde suffisant
- Transfert avec solde insuffisant
- Montant negatif
- Montant nul
- Verification des historiques apres plusieurs operations

Partie 2:
- Connexion au serveur
- get_info
- Transfert avec solde suffisant
- Transfert avec solde insuffisant
- Serveur non demarre (connexion refusee)
- Delai depasse (timeout)
- Port deja utilise au demarrage serveur

## 10) Commandes rapides (Windows)

Depuis le dossier Crypto:

python local_transfer.py
python network_server.py
python network_client.py
