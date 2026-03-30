
PROJET Crypto-monnaie


Sujet : Creer un système de transfert de crypto-monnaie

Structure:
    BKN
    |- local_transfer.py Gestion des transfert local
    |- network_client.py Gestion du transfert client/server (partie client)
    |- network_server.py Gestion du transfert client/server (partie server)
    |- wallet.py : Gestion du wallet


Pour lancer le projet partie Transfert Local:
    - Aller au rout du projet
    - Lancer le script : python.exe ./local_transfer.py
    - Puis amusez vous!

Pour lancer le projet partie Transfert Local:
    - Aller au rout du projet
    - Ouvrir un terminal
    - Lancer le script : python.exe ./network_server.py
    - Ouvrir un autre terminal
    - Lancer le script : python.exe ./network_client.py
    - Puis amusez vous!


Choix de conceptions :

Transfert Local
Pour effectuer les transferts, on manipule directement les objects/wallets concerner grace a la fonction effectuer_transfert() (qui appelle recieve())


Transfert Client -> Server
Pour effectuer les transferts, on fait le server exposer un port de connection via websockets pour qu'un client puisse s'y connecter et faire le transfert d'argent en modifiant l'attribut solde avec la methode recieve() 

Transfert Server -> Client
Pour effectuer les transferts, on fait le server exposer un port de connection via websockets pour qu'un client puisse s'y connecter. Puis on creer un espace de stockage ou quand le server envoie de l'argent, la requete est stocker dans cet espace pour qu'au prochain connection du Client, il clique l'option 5, entre le port et host et reçoit l'argent.

DONC le client uniquement reçoit l'argent quand il se connecte au server




Les difficultés rencontrées:
    - Creation du server et gerer les connections websockets
    - Trouver une maniere de faire le transfert server -> client



Les améliorations possibles:
    - Ajouter des mots de passe
    - Separer le server du client 
    - Ajouter des signature pour les transactions
    - Creer un blocs chaines
    - Hash les transactions
    - Stocker les transactions dans une base de donnée (avec docker)
    - Creer une interface 