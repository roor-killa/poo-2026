# Cahier des Charges - Transport Martinique (Suivi Bus Temps Reel)

## 1. Contexte et problematique

En Martinique, les usagers des transports en commun rencontrent une difficulte recurrente: il est difficile de savoir si le bus est deja passe ou s'il est encore en approche. Cette incertitude genere:

- des temps d'attente inutiles
- une perte de confiance dans le service
- des retards pour les etudiants, salaries et usagers quotidiens

Le projet **Transport Martinique** vise a fournir une information fiable, lisible et en temps reel sur la position des bus et leur heure d'arrivee estimee.

## 2. Objectifs du projet

### 2.1 Objectif general

Concevoir une application permettant a un usager de savoir instantanement:

- ou se trouve un bus sur sa ligne
- si le bus est deja passe a son arret
- dans combien de temps le prochain bus arrive

### 2.2 Objectifs specifiques

- collecter la position GPS des bus en quasi temps reel
- calculer une ETA (heure d'arrivee estimee) par arret
- afficher les informations sur une interface simple mobile/web
- reduire l'incertitude et le temps d'attente percu

## 3. Analyse des besoins

### 3.1 Acteurs

- **Usager**: consulte les lignes, arrets, ETA, statut du bus.
- **Conducteur (ou device embarque)**: partage automatiquement sa position GPS.
- **Administrateur reseau**: gere lignes, arrets, bus et supervision.

### 3.2 Besoins fonctionnels

- Visualiser les bus actifs sur une carte.
- Rechercher un arret et voir les prochains passages.
- Afficher un statut clair:
	- "Arrive dans X min"
	- "A l'approche"
	- "Deja passe"
	- "Donnee indisponible"
- Consulter les details d'une ligne (trajet, arrets, direction).
- Recevoir des alertes de perturbation (option MVP+).

### 3.3 Besoins non fonctionnels

- Disponibilite cible: 99% sur plage de service.
- Latence d'actualisation: 5 a 15 secondes.
- Precision de geolocalisation: < 30 m en zone couverte.
- Securite: authentification des devices bus, chiffrement HTTPS.
- Scalabilite: support de plusieurs lignes simultanees.

### 3.4 Contraintes

- Couverture reseau mobile parfois instable selon zones.
- Heterogeneite du parc de bus (equipements differents).
- Budget limite (contexte projet etudiant / pilote local).

## 4. Conception fonctionnelle

### 4.1 Cas d'usage principaux

1. En tant qu'usager, je veux choisir ma ligne pour voir les bus en circulation.
2. En tant qu'usager, je veux selectionner mon arret pour savoir si le bus est deja passe.
3. En tant qu'usager, je veux voir l'ETA pour organiser mon depart.
4. En tant qu'admin, je veux gerer les lignes/arrets/bus.
5. En tant que systeme, je veux traiter les positions GPS et recalculer les ETA.

### 4.2 Regles metier essentielles

- Un bus en service envoie sa position periodiquement.
- Un bus est rattache a une ligne et un sens (aller/retour).
- Le statut "deja passe" est determine par la position du bus sur le trajet par rapport a l'arret cible.
- Si aucune position recente (> 90 sec), le statut devient "donnee indisponible".

## 5. IHM choisie

### 5.1 Cibles

- **PWA responsive**: acces et utilisation confortables sur mobile, tablette et PC.
- **Interface cartographique**: la vue principale est une carte interactive avec des popups au clic sur un arret de bus.

### 5.2 MVP express vise

- consultation d'un arret ou d'une ligne via une barre de recherche en haut de la carte
- recherche des arrets de bus et des lignes, avec prise en compte du sens/direction
- affichage de popups sur la carte pour voir les informations d'un arret, d'une ligne ou des prochains passages
- ecran adapte mobile et desktop, avec navigation fluide sur PC et smartphone
- mode hors ligne de base grace au cache PWA
- installation sur l'ecran d'accueil

### 5.3 Ecrans principaux

- Ecran principal: carte interactive, barre de recherche, popups d'arrets.
- Ecran arret: details de l'arret, ETA simplifie, statut de passage, prochains bus.
- Ecran ligne: affiche le trajet, les arrets et la direction selectionnee.

### 5.4 Principes UX

- Information lisible en moins de 3 secondes.
- Code couleur simple (vert = approche, orange = retard, gris = indisponible).
- Priorite au texte explicite pour eviter les ambiguities.
- Carte lisible, mobile first, avec interactions rapides sur les arrets et les lignes.

## 6. Storyboard (parcours utilisateur)

### Scenario principal: "Mon bus est-il deja passe ?"

1. L'usager ouvre l'application.
2. Il saisit ou selectionne son arret favori.
3. L'application affiche les bus de la ligne concernes.
4. Pour chaque bus, l'app calcule et montre:
	 - distance restante
	 - ETA
	 - statut (approche / deja passe)
5. L'usager prend sa decision (attendre, changer d'arret, itineraire alternatif).

### Scenario secondaire: "Suivi sur carte"

1. L'usager choisit une ligne.
2. Une vue carte peut etre ajoutee plus tard, hors MVP.
3. Les positions se rafraichissent automatiquement dans une version future.

## 7. Modele de donnees (proposition)

### 7.1 Entites principales

- **Bus**: id, immatriculation, capacite, statut, ligne_id
- **Ligne**: id, code, nom, sens, actif
- **Arret**: id, nom, latitude, longitude
- **LigneArret**: ligne_id, arret_id, ordre, distance_cumulee
- **PositionBus**: id, bus_id, latitude, longitude, vitesse, timestamp
- **PassageEstime**: id, bus_id, arret_id, eta_minutes, statut, calcule_a
- **Utilisateur**: id, nom, email, role

### 7.2 Relations

- Une ligne possede plusieurs arrets ordonnes.
- Un bus appartient a une ligne active a un instant donne.
- Un bus emet plusieurs positions dans le temps.
- Les ETA sont calculees par couple (bus, arret).

## 8. Architecture technique

### 8.1 Vue d'ensemble

- **Frontend PWA**: interface Next.js responsive, optimisee pour PC et mobile.
- **Backend FastAPI**: API REST pour servir lignes, arrets, sens, et ETA mockes.
- **Carte interactive**: composant principal cote frontend pour afficher les arrets et leurs popups.
- **Recherche globale**: barre de recherche en tete de carte pour trouver rapidement arrets et lignes par direction.
- **Cache offline**: service worker pour navigation de base sans reseau.
- **Containerisation complete**: tout le projet doit tourner dans Docker, avec Docker Compose pour lancer frontend + backend.
- **Execution locale hors Docker**: hors scope du MVP, le fonctionnement cible est 100% containerise.

### 8.2 Flux de donnees

1. L'utilisateur ouvre la PWA sur mobile ou PC.
2. La PWA appelle l'API FastAPI du MVP.
3. L'utilisateur cherche un arret ou une ligne, puis precise la direction si besoin.
4. La carte centre le resultat et affiche un popup avec les details du point selectionne.
5. L'interface affiche le prochain passage estime et le statut via les donnees API.
6. Le cache PWA garde l'application utilisable hors ligne de facon basique.

## 9. Stack technique recommandee

### Stack minimale MVP

- Frontend: Next.js + React
- UI: design responsive desktop/mobile
- Carte: bibliotheque cartographique au choix selon le besoin final
- Backend: FastAPI + Uvicorn
- PWA: manifest + service worker
- Donnees: mocks en memoire ou JSON servis par FastAPI
- Conteneurisation: Docker Compose obligatoire, avec tous les services executes dans Docker

### Hors perimetre MVP

- backend temps reel
- base de donnees PostgreSQL
- auth JWT
- geolocalisation en direct du bus
- notifications push

## 10. Plan de realisation

### Sprint express 2h30

#### 0h00 - 0h20

- creer le projet Vite React
- creer le backend FastAPI minimal
- definir les donnees mock API

#### 0h20 - 0h55

- construire l'ecran principal mobile first
- ajouter la recherche arret/ligne
- connecter la PWA aux endpoints FastAPI

#### 0h55 - 1h25

- mettre le manifest et le service worker
- tester l'installation PWA
- ajouter le cache offline de base

#### 1h25 - 2h00

- ecrire les Dockerfile frontend/backend
- preparer docker-compose
- corriger les erreurs d'affichage

#### 2h00 - 2h30

- nettoyer le README
- faire une demo rapide sur mobile
- noter les evolutions possibles

## 11. Ressources et moyens

### 11.1 Ressources humaines (minimum)

- 1 developpeur frontend avec assistance IA
- 1 developpeur backend FastAPI (peut etre la meme personne)
- 1 testeur ou utilisateur beta pour verifier le rendu mobile

### 11.2 Ressources materiels

- Un ordinateur avec Node.js, Python 3.11+ et Docker
- Un smartphone pour tester l'installation PWA
- Un navigateur moderne pour la validation mobile

### 11.3 Budget indicatif (MVP)

- Equipement GPS pilote: faible a moyen
- Hebergement cloud: faible a moyen
- Cout principal: temps de developpement

### 11.4 Sources de donnees publiques Martinique

Les arrets, lignes et parcours peuvent etre derives des feeds GTFS publics suivants:

- GTFS du transport scolaire en Martinique:
	- Page data.gouv: https://www.data.gouv.fr/datasets/gtfs-du-transport-scolaire-en-martinique
	- API dataset: https://www.data.gouv.fr/api/1/datasets/66ec3c0c709063a99cb03d00/
	- Fichier GTFS direct: https://www.data.gouv.fr/api/1/datasets/r/c14a1893-58a1-4e7b-830e-bd1f9daa863d
- GTFS du reseau maritime de Martinique:
	- Page data.gouv: https://www.data.gouv.fr/datasets/gtfs-du-reseau-maritime-de-martinique
	- API dataset: https://www.data.gouv.fr/api/1/datasets/66c5292d8731e820140565b7/
	- Fichier GTFS direct: https://www.data.gouv.fr/api/1/datasets/r/39fc07d6-65b5-49f0-a5f2-d56757a8dd42

Ces fichiers GTFS contiennent les donnees utiles pour les arrets, les lignes, les sens et les passages via les tables `stops.txt`, `routes.txt`, `trips.txt` et `stop_times.txt`.

## 12. Risques et mitigations

- **Risque**: GPS instable en zones denses.  
	**Mitigation**: filtrage et lissage des positions, fallback derniere position fiable.
- **Risque**: reseau mobile coupe.  
	**Mitigation**: buffer local puis envoi differe.
- **Risque**: ETA peu precise au debut.  
	**Mitigation**: recalibrage par historique reel des trajets.

## 13. Livrables attendus

- Cahier des charges valide
- Maquettes IHM
- API documentee (OpenAPI/Swagger)
- Application usager MVP (web/mobile)
- Rapport de test de precision ETA

## 14. Critere de reussite

- L'usager sait en moins de 5 secondes si son bus arrive ou est deja passe.
- Precision ETA moyenne inferieure a +/- 2-3 minutes sur ligne pilote.
- Application stable pendant les heures de pointe.

---

## Resume

Ce projet apporte une reponse concrete au probleme de visibilite des bus en Martinique via geolocalisation, calcul ETA et affichage temps reel. Le MVP doit prioriser la fiabilite de l'information usager avant l'ajout de fonctionnalites avancees.



