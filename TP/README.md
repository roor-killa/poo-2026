# système de transfert bkn

## description



le but est de créer un système simple de wallets capable de

- créer des wallets
- envoyer des bkn
- recevoir des bkn
- consulter le solde
- consulter l historique
- faire des transferts en local
- faire des transferts en réseau


---

## objectifs du tp

le sujet demande

- une classe `wallet`
- un programme `local_transfer.py`
- un programme `network_server.py`
- un programme `network_client.py`
- un `README.md`

le tp repose sur la poo les sockets json et la gestion des erreurs

---

## structure du projet

```text
TP
├── wallet.py
├── local_transfer.py
├── network_server.py
├── network_client.py
└── README.md

---

## ▶comment lancer le projet (état actuel)

### 1 se placer dans le dossier du projet(...OBJET\depot\poo-2026\TP) et taper

```bash
python local_transfer.py



puis utiliser le menu

exemples

1 → afficher les wallets
2 → transfert wallet1 vers wallet2
3 → transfert wallet2 vers wallet1
4 → historique wallet1
5 → historique wallet2
0 → quitter




test du serveur réseau
ouvrir un terminal

python network_server.py


