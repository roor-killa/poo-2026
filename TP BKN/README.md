# TP BKN - Système de Crypto-monnaie BKN (BoKryptoNou)

Système de portefeuilles de crypto-monnaie permettant des transferts locaux et réseau.

## Fichiers

### `wallet.py`
**Description :** Classe `Wallet` représentant un portefeuille BKN. Gère le solde, les transactions et l'historique.

**Usage :** Module importé par les autres fichiers (pas à exécuter directement).

---

### `local_transfer.py`
**Description :** Application de transferts locaux entre deux wallets (Alice et Bob). Menu interactif pour transférer des BKN et consulter l'historique.

**Lancement :**
```bash
python local_transfer.py
```

**Options du menu :**
1. Afficher les wallets
2. Transférer (Alice → Bob)
3. Transférer (Bob → Alice)
4. Historique Alice
5. Historique Bob
0. Quitter

---

### `network_server.py`
**Description :** Serveur TCP qui expose un wallet sur le réseau. Accepte les requêtes JSON pour consulter les infos ou recevoir des BKN.

**Lancement :**
```bash
python network_server.py
```

**Configuration :** Le programme demande le nom du propriétaire, le solde initial, l'hôte et le port (défaut: localhost:5555).

**Commandes locales :** `info`, `hist`, `quit`

---

### `network_client.py`
**Description :** Client TCP pour interagir avec un serveur BKN distant. Permet de consulter un wallet distant et d'envoyer des BKN.

**Lancement :**
```bash
python network_client.py
```

**Options du menu :**
1. Afficher mon wallet
2. Afficher l'historique
3. Obtenir infos d'un wallet distant
4. Transférer des BKN à un wallet distant
0. Quitter

---

## Utilisation Réseau

1. **Démarrer le serveur** dans un terminal :
   ```bash
   python network_server.py
   ```

2. **Démarrer le client** dans un autre terminal :
   ```bash
   python network_client.py
   ```

3. Utiliser l'option 4 du client pour transférer des BKN vers le serveur.
