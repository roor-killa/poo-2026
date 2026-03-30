# TP : Système de Transfert de Crypto-monnaie BKN (BoKryptoNou)
## Programmation Orientée Objet - Application du Polymorphisme

---

## 📋 Objectifs Pédagogiques

### Concepts POO
1. **Polymorphisme** : Manipuler différents types d'objets via une interface commune
2. **Abstraction** : Créer des interfaces claires et réutilisables
3. **Encapsulation** : Gérer l'état interne des objets de manière sécurisée
4. **Composition** : Assembler des objets pour créer des systèmes complexes

### Compétences Techniques
1. Programmation réseau avec les sockets Python
2. Sérialisation/désérialisation JSON
3. Gestion des transactions et de l'état
4. Programmation concurrente (threads)
5. Gestion des erreurs et cas limites

---

## 🎯 Contexte du Projet

Vous allez créer un système de transfert de crypto-monnaie **BKN (BoKryptoNou) ou (BitKoinNou)**, 
la nouvelle crypto de la Martinique ! 🇫🇷

Le système permettra de :
- Créer des wallets (portefeuilles électroniques)
- Effectuer des transferts locaux (sur un seul terminal)
- Effectuer des transferts réseau (entre deux terminaux distants)
- Consulter l'historique des transactions
- Vérifier les soldes

---

## 📦 Partie 1 : Transferts Locaux (1h)

### Objectif
Créer un système de transfert de BKN entre deux wallets **sur le même terminal**.

### Fonctionnalités Requises

1. **Classe Wallet** ✅ (Fournie)
   - Attributs : adresse, nom du propriétaire, solde
   - Méthodes : envoyer, recevoir, consulter historique

2. **Programme local_transfer.py**
   - Menu interactif
   - Affichage des informations des wallets
   - Transfert bidirectionnel entre Wallet1 ↔ Wallet2
   - Affichage de l'historique des transactions

### Critères d'Évaluation (10 points)

| Critère | Points |
|---------|--------|
| Les wallets sont créés correctement avec soldes initiaux | 2 |
| Le menu est fonctionnel et clair | 2 |
| Les transferts Wallet1 → Wallet2 fonctionnent | 2 |
| Les transferts Wallet2 → Wallet1 fonctionnent | 2 |
| Gestion des erreurs (solde insuffisant, montant invalide) | 1 |
| Affichage de l'historique des transactions | 1 |

### Exemple d'Utilisation

```bash
$ python local_transfer.py

💎 SYSTÈME DE TRANSFERT BKN - MODE LOCAL
1. Afficher les wallets
2. Transférer BKN (Wallet1 → Wallet2)
3. Transférer BKN (Wallet2 → Wallet1)
4. Historique Wallet1
5. Historique Wallet2
0. Quitter

👉 Votre choix: 2

💸 Transfert: Alice → Bob
Solde disponible: 1000.00 BKN
Montant à transférer: 150

✅ Transfert de 150.0 BKN réussi
   Transaction: TXN-BKN-20250202143052-123

📊 Nouveaux soldes:
   Alice: 850.00 BKN
   Bob: 650.00 BKN
```

---

## 🌐 Partie 2 : Transferts Réseau (2h)

### Objectif
Créer un système de transfert de BKN entre deux wallets **sur deux terminaux distants**.

### Architecture

```
Terminal 1 (Serveur)          Terminal 2 (Client)
┌──────────────────┐         ┌──────────────────┐
│  Wallet Serveur  │  ←───→  │  Wallet Client   │
│  Balance: 1000   │         │  Balance: 500    │
│  Port: 5555      │         │  Se connecte au  │
│                  │         │  serveur         │
└──────────────────┘         └──────────────────┘
```

### Protocole de Communication

#### 1. Demande d'Information
```json
// Client → Serveur
{
    "action": "get_info"
}

// Serveur → Client
{
    "status": "success",
    "wallet": {
        "address": "BKN-SERVER-ALICE-001",
        "owner": "Alice",
        "balance": 1000.0
    }
}
```

#### 2. Transfert de BKN
```json
// Client → Serveur (pour recevoir des BKN)
{
    "action": "receive",
    "amount": 100.0,
    "from_address": "BKN-CLIENT-BOB-002"
}

// Serveur → Client
{
    "status": "success",
    "message": "Réception de 100.0 BKN confirmée",
    "transaction_id": "TXN-BKN-20250202-123",
    "new_balance": 1100.0
}
```

### Fonctionnalités Requises

1. **network_server.py** ✅ (Fourni comme base)
   - Créer un serveur socket TCP
   - Gérer les connexions clients
   - Traiter les requêtes JSON
   - Créditer le wallet lors de réception de BKN
   - Afficher les commandes locales (info, hist, quit)

2. **network_client.py** ✅ (Fourni comme base)
   - Se connecter au serveur
   - Envoyer des requêtes JSON
   - Débiter le wallet local
   - Confirmer la réception distante

### Critères d'Évaluation (10 points)

| Critère | Points |
|---------|--------|
| Le serveur démarre correctement et écoute sur un port | 2 |
| Le client peut se connecter au serveur | 2 |
| La requête "get_info" fonctionne | 1 |
| Le transfert Client → Serveur fonctionne | 3 |
| Les soldes sont mis à jour correctement (local et distant) | 1 |
| Gestion des erreurs réseau (timeout, connexion refusée) | 1 |

### Scénario de Test

#### Terminal 1 (Serveur)
```bash
$ python network_server.py

🌐 SERVEUR DE WALLET BKN
Nom du propriétaire du wallet: Alice
Solde initial (BKN): 1000
Host (Enter = localhost): 
Port (Enter = 5555): 

🌐 Serveur BKN démarré sur localhost:5555
🏦 Wallet: Alice
💰 Solde initial: 1000.00 BKN
En attente de connexions...

[Serveur] > info
🏦 WALLET BKN - Alice
Adresse: BKN-SERVER-ALICE-743
Solde: 1000.00 BKN
```

#### Terminal 2 (Client)
```bash
$ python network_client.py

🌐 CLIENT DE WALLET BKN
Votre nom: Bob
Solde initial (BKN): 500

✅ Wallet créé!
   Adresse: BKN-CLIENT-BOB-284
   Solde: 500.00 BKN

💎 CLIENT WALLET BKN
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

👉 Votre choix: 4

💸 Transfert de BKN vers un wallet distant
Votre solde: 500.00 BKN
Host du serveur destinataire (Enter = localhost): 
Port (Enter = 5555): 
Montant à transférer (BKN): 100

💸 Transfert de 100.0 BKN en cours...
🔗 Connexion à localhost:5555...
✅ Connecté!
📍 Wallet distant: BKN-SERVER-ALICE-743
✅ Débit local effectué (100.0 BKN)
✅ Crédit distant confirmé!
   Transaction ID: TXN-BKN-20250202143052-743

✅ Transfert de 100.0 BKN réussi

📊 Nouveaux soldes:
   Votre wallet: 400.00 BKN
   Wallet distant: 1100.0 BKN
```

---

## 🚀 Extensions Possibles (Bonus)

### Niveau 1 : Fonctionnalités Supplémentaires (+2 points)
- Transfert bidirectionnel réseau (Serveur → Client aussi)
- Validation de l'adresse du wallet avant transfert
- Confirmation avant chaque transfert

### Niveau 2 : Sécurité (+3 points)
- Authentification par mot de passe pour chaque wallet
- Signature des transactions
- Liste des wallets autorisés

### Niveau 3 : Blockchain Simplifiée (+5 points)
- Créer un système de blocs chaînés
- Hash de chaque transaction
- Vérification de l'intégrité de la chaîne

---

## 📝 Livrables

1. **Code Source**
   - `wallet.py` (peut être modifié/amélioré)
   - `local_transfer.py` (complété)
   - `network_server.py` (complété)
   - `network_client.py` (complété)

2. **Documentation**
   - README.md expliquant :
     - Comment lancer chaque partie
     - Les choix de conception
     - Les difficultés rencontrées
     - Les améliorations possibles

3. **Vidéo de Démonstration** (optionnel)
   - Partie 1 : Transferts locaux (2-3 min)
   - Partie 2 : Transferts réseau (3-5 min)

---

## 🧪 Tests à Effectuer

### Partie 1
- [ ] Transfert avec solde suffisant
- [ ] Transfert avec solde insuffisant
- [ ] Transfert d'un montant négatif
- [ ] Transfert de 0 BKN
- [ ] Affichage de l'historique après plusieurs transferts

### Partie 2
- [ ] Connexion au serveur
- [ ] Récupération des infos du wallet distant
- [ ] Transfert avec solde suffisant
- [ ] Transfert avec solde insuffisant
- [ ] Gestion de la déconnexion du serveur
- [ ] Timeout de connexion
- [ ] Port déjà utilisé

---

## 💡 Conseils

1. **Testez progressivement** : Commencez par la Partie 1, puis passez à la Partie 2
2. **Gérez les erreurs** : Anticipez tous les cas d'erreur possibles
3. **Lisez les messages** : Les prints vous guident dans le déroulement
4. **Utilisez le debugger** : Placez des breakpoints pour comprendre le flux
5. **Travaillez en binôme** : Une personne = un terminal pour la Partie 2

---

## 📚 Ressources

- Documentation Python sockets: https://docs.python.org/3/library/socket.html
- JSON en Python: https://docs.python.org/3/library/json.html
- Threading: https://docs.python.org/3/library/threading.html

---

## ⏰ Planning Suggéré

| Temps | Activité |
|-------|----------|
| 0h00 - 0h15 | Lecture de l'énoncé et compréhension du code fourni |
| 0h15 - 1h15 | Partie 1 : Transferts locaux |
| 1h15 - 1h30 | Pause |
| 1h30 - 3h30 | Partie 2 : Transferts réseau |
| 3h30 - 4h00 | Tests et rédaction du README |

---

**Bon courage et amusez-vous bien avec BKN ! 🚀💎**
