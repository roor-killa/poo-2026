# 💎 Système de Transfert BKN (BoKryptoNou)

La nouvelle crypto-monnaie de la Martinique ! 🇫🇷

---

## 📁 Structure du projet

```
bkn/
├── wallet.py            # Classe Wallet (Transaction + Wallet)
├── local_transfer.py    # Partie 1 : transferts locaux
├── network_server.py    # Partie 2 : serveur TCP
├── network_client.py    # Partie 2 : client TCP
└── README.md
```

---

## 🚀 Lancement

### Partie 1 — Transferts locaux

```bash
python local_transfer.py
```

Deux wallets sont créés interactivement, puis un menu permet d'effectuer des transferts dans les deux sens et de consulter l'historique.

### Partie 2 — Transferts réseau

**Terminal 1 (Serveur)**

```bash
python network_server.py
```

Renseigner le nom, le solde, le host et le port. Le serveur écoute les connexions et accepte les commandes locales : `info`, `hist`, `quit`.

**Terminal 2 (Client)**

```bash
python network_client.py
```

Renseigner le nom et le solde. Le menu propose d'afficher son wallet, son historique, de consulter un wallet distant, ou d'effectuer un transfert.

---

## ⚙️ Prérequis

- Python 3.10+ (utilisation des union types `X | Y`)
- Aucune dépendance externe (bibliothèques standard uniquement)

---

## 🏗️ Choix de conception

### Polymorphisme et abstraction

La méthode `envoyer()` de `Wallet` appelle `recevoir()` sur n'importe quel objet `Wallet`, ce qui illustre le polymorphisme : le code expéditeur ne connaît pas la nature concrète du destinataire.

### Séparation réseau / logique métier

`wallet.py` ne contient aucun code réseau. Le serveur et le client importent `Wallet` et gèrent eux-mêmes la sérialisation JSON et les sockets. Cela respecte le principe de responsabilité unique.

### Rollback sur échec réseau

Dans `network_client.py`, si le débit local a réussi mais que le crédit distant échoue, le solde local est restauré et la transaction est retirée de l'historique. Cela évite de perdre des BKN sans confirmation.

### Protocole JSON sur TCP avec délimiteur `\n`

Chaque message se termine par `\n`. La lecture boucle jusqu'à trouver ce délimiteur, ce qui permet de gérer correctement les messages fragmentés par TCP.

### Thread par client (serveur)

Chaque connexion est traitée dans un thread dédié (`daemon=True`). Le thread principal reste libre pour écouter de nouvelles connexions. Un `threading.Event` permet l'arrêt propre via la commande `quit`.

---

## 🧪 Tests effectués

| Scénario | Résultat |
|---|---|
| Transfert avec solde suffisant | ✅ |
| Transfert avec solde insuffisant | ✅ Erreur explicite |
| Montant négatif | ✅ Rejeté |
| Montant = 0 | ✅ Rejeté |
| Historique après plusieurs transferts | ✅ |
| Connexion au serveur | ✅ |
| get_info wallet distant | ✅ |
| Transfert client → serveur | ✅ |
| Serveur non démarré (connexion refusée) | ✅ Message clair |
| Timeout de connexion | ✅ Géré |
| Port déjà utilisé | ✅ Message explicite |

---

## 💡 Difficultés rencontrées

- **Rollback atomique** : garantir la cohérence des deux wallets quand la connexion tombe entre le débit local et le crédit distant est le cas le plus délicat. La solution retenue (rollback immédiat avec message d'avertissement) est un compromis acceptable pour un prototype.
- **Fragmentation TCP** : les petits messages JSON arrivent rarement fragmentés en pratique, mais la boucle de lecture sur `\n` assure la robustesse.
- **Arrêt propre du serveur** : `socket.settimeout(1.0)` sur l'`accept()` permet de vérifier périodiquement le `stop_event` sans bloquer indéfiniment.

---

## 🔮 Améliorations possibles

1. **Transfert bidirectionnel réseau** : ajouter une action `send` côté serveur (bonus niveau 1).
2. **Authentification** : mot de passe hashé (SHA-256) échangé à la connexion (bonus niveau 2).
3. **Blockchain simplifiée** : chaîner les transactions avec leur hash SHA-256 et vérifier l'intégrité à la demande (bonus niveau 3).
4. **Persistance** : sauvegarder les wallets en JSON ou SQLite pour survivre aux redémarrages.
5. **Interface graphique** : Tkinter ou une petite API Flask + React.
