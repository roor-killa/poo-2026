🚌 Système de Suivi en Temps Réel des Bus - Martinique📝 1. Présentation du Projet
1.1 Contexte
Le réseau de transport en Martinique fait face à un défi majeur concernant l'information voyageur. L'absence de visibilité en temps réel sur la position des véhicules entraîne une incertitude pour les usagers. Ce projet modernise le service en offrant une solution technologique de pointe pour la géolocalisation fluide des bus.

1.2 Objectif Principal
Développer une solution capable de collecter, traiter et diffuser les données de géolocalisation de manière instantanée via des technologies de communication asynchrones.

⚙️ 2. Analyse et Besoins
2.1 Besoins Fonctionnels
Suivi GPS : Réception des coordonnées (lat/long) à intervalles réguliers.
Calcul des ETA : Estimation du temps d'arrivée aux arrêts.
Gestion des Incidents : Notification des retards ou déviations.

2.2 Dictionnaire des DonnéesEntitéAttributsDescriptionBusID_Bus, Plaque, ModèleIdentifiant unique du véhiculePositionLat, Long, TimestampDonnées télémétriques en temps réelLigneNuméro, Nom, ItinéraireDéfinition du parcours officielArrêtID_Arrêt, Nom, CoordonnéesPoints de passage obligatoires🛠️ 

3. Architecture & Stack Technique
3.1 Choix Technologiques 
Backend : Python (POO) avec FastAPI pour la performance asynchrone.
Base de Données : PostgreSQL (optimisé pour les requêtes géospatiales).
Communication : WebSockets pour le push de données temps réel. 
Conteneurisation : Docker & Docker-Compose pour un déploiement isolé.
Interface (IHM) : HTML5/JavaScript avec Leaflet.js pour la cartographie interactive.

🚀 4. Installation et Lancement (Docker)Pour lancer le projet (MVP) dans un environnement totalement configuré, utilisez Docker 

Lancer l'infrastructure :Bashdocker-compose up --build

Accéder à l'application :
Carte Temps Réel : http://localhost:8000Documentation
 API (Swagger) : http://localhost:8000/docs
 Vérification DB : http://localhost:8000/check-db
 🗺️ 5. Stratégie de Développement (MVP)
 Phase 1 : Développement du MVP sur une ligne pilote (ex: Ligne 1 - Fort-de-France).
 Phase 2 : Extension à l'ensemble du réseau Martiniquais (Mozaïk).
 Phase 3 : Intégration de l'extension PostGIS pour des calculs d'itinéraires avancés.

📦 6. Livrables
Source Code Backend (Python/FastAPI)
Base de données documentée (SQLAlchemy Models)
Documentation API interactive (OpenAPI/Swagger)
Interface de visualisation cartographique dynamique.