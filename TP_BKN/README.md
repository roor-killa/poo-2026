# TP : Système de Transfert de Crypto-monnaie BKN (BoKryptoNou)

## 📌 Description du projet

Ce projet consiste à développer un système simple de transfert de crypto-monnaie appelé **BKN (BoKryptoNou)** en utilisant les principes de la **Programmation Orientée Objet (POO)** en Python.

L’application permet de créer des **wallets (portefeuilles numériques)** et d’effectuer des **transactions de BKN** soit localement (sur un seul terminal), soit à distance via un **réseau client/serveur utilisant les sockets Python**.

Ce projet met en pratique plusieurs concepts importants comme le **polymorphisme, l’encapsulation, la gestion des transactions et la communication réseau**.

---

# 🎯 Objectifs du TP

Les objectifs principaux de ce projet sont :

* Comprendre et appliquer les concepts de la **Programmation Orientée Objet**
* Implémenter un système simple de **gestion de wallet**
* Réaliser des **transactions de crypto-monnaie**
* Mettre en place une **communication réseau avec les sockets**
* Manipuler des données en **format JSON**
* Gérer les **erreurs et les cas limites**

---

# 🧱 Structure du projet

Le projet est composé de plusieurs fichiers :

```
TP_BKN
│
├── wallet.py
├── local_transfer.py
├── network_server.py
├── network_client.py
└── README.md
```

### wallet.py

Ce fichier contient la classe **Wallet** qui représente un portefeuille de crypto-monnaie.

Fonctionnalités principales :

* création d'un wallet
* génération d'une adresse unique
* gestion du solde
* envoi de BKN
* réception de BKN
* stockage de l'historique des transactions

---

### local_transfer.py

Ce programme permet d'effectuer des **transferts de BKN entre deux wallets sur le même terminal**.

Fonctionnalités :

* affichage des wallets
* transfert Alice → Bob
* transfert Bob → Alice
* affichage de l'historique des transactions

---

### network_server.py

Ce fichier implémente le **serveur du système BKN**.

Fonctionnalités :

* création d'un wallet serveur
* écoute des connexions réseau
* traitement des requêtes JSON
* réception de BKN depuis un client
* envoi des informations du wallet

---

### network_client.py

Ce programme représente le **client du système**.

Fonctionnalités :

* création d'un wallet client
* connexion au serveur
* récupération des informations du wallet distant
* envoi de BKN vers un wallet distant
* affichage de l'historique

---

# ⚙️ Technologies utilisées

Ce projet utilise :

* **Python**
* **Programmation Orientée Objet**
* **Sockets TCP**
* **JSON**
* **Programmation réseau**

---

# 🚀 Comment lancer le projet

## 1️⃣ Partie 1 : Transfert local

Dans le terminal :

```
python local_transfer.py
```

Le programme affichera un menu permettant de :

* voir les wallets
* effectuer des transferts
* consulter l'historique

---

## 2️⃣ Partie 2 : Transfert réseau

### Lancer le serveur

Dans un premier terminal :

```
python network_server.py
```

Entrer :

* le nom du propriétaire
* le solde initial
* le port

---

### Lancer le client

Dans un second terminal :

```
python network_client.py
```

Le client pourra :

* afficher son wallet
* consulter l'historique
* obtenir les informations du wallet distant
* transférer des BKN au serveur

---

# 🧪 Tests réalisés

Les tests suivants ont été réalisés :

* transfert avec solde suffisant
* transfert avec solde insuffisant
* transfert d'un montant négatif
* affichage de l'historique des transactions
* connexion client / serveur
* récupération des informations d'un wallet distant
* transfert réseau entre deux wallets

---

# ⚠️ Difficultés rencontrées

Lors du développement de ce projet, plusieurs difficultés ont été rencontrées :

* compréhension du fonctionnement des **sockets réseau**
* gestion de la communication **client / serveur**
* sérialisation et désérialisation des données **JSON**
* gestion des erreurs lors des transactions

Ces difficultés ont été résolues en utilisant la documentation officielle de Python et en testant progressivement chaque fonctionnalité.

---

# 🔮 Améliorations possibles

Plusieurs améliorations peuvent être ajoutées au projet :

* authentification des wallets avec mot de passe
* validation des adresses de wallet
* création d'une **blockchain simplifiée**
* ajout d'une interface graphique
* transfert bidirectionnel serveur → client

---

# 👨‍💻 Auteur

Projet réalisé par :

**Mohand**

Étudiant en L2 informatique
