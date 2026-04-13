# Cahier des Charges — BusTrack MQ

**Application de suivi en temps réel des bus en Martinique**

---

| Champ | Détail |
|---|---|
| **Auteur** | Ibrahim Ousseini GUINDO |
| **Formation** | L2 Informatique — Université des Antilles |
| **Cours** | Projet Backend — POO Python / FastAPI |
| **Date** | Avril 2026 |
| **Version** | 2.0 |

---

## Sommaire

1. [Présentation du projet](#1-présentation-du-projet)
2. [Analyse](#2-analyse)
3. [Conception](#3-conception)
4. [Stack technique](#4-stack-technique)
5. [Architecture technique](#5-architecture-technique)
6. [Plan, ressources et moyens](#6-plan-ressources-et-moyens)
7. [MVP — Développement de l'application](#7-mvp--développement-de-lapplication)
8. [Déploiement en production — CI/CD](#8-déploiement-en-production--cicd)
9. [Application mobile Flutter](#9-application-mobile-flutter)
10. [Notifications push](#10-notifications-push)
11. [Analyse des risques](#11-analyse-des-risques)
12. [Conclusion](#12-conclusion)

---

## 1. Présentation du projet

### 1.1 Contexte général

La Martinique est un territoire insulaire dont les transports en commun constituent un enjeu majeur de mobilité pour la population. Les usagers souffrent aujourd'hui d'un manque de visibilité en temps réel sur la position des bus, entraînant des attentes incertaines et une faible confiance dans l'offre de transport public.

Le projet **BusTrack MQ** vise à concevoir et développer une solution complète permettant de simuler et d'afficher en temps réel la position des bus sur le réseau martiniquais. Cette solution repose sur un backend Python orienté objet (POO) avec FastAPI, un frontend web Next.js, une application mobile Flutter et un pipeline CI/CD automatisé.

### 1.2 Objectifs

- Simuler la position GPS des bus sur des lignes prédéfinies de Martinique.
- Exposer ces données via une API REST et un flux WebSocket temps réel.
- Afficher la position des bus sur une carte interactive (web et mobile).
- Permettre la consultation des lignes, arrêts et détails des bus.
- Envoyer des notifications push aux usagers abonnés (Web Push + FCM).
- Déployer l'application en production avec un pipeline CI/CD automatisé.

### 1.3 Périmètre

Le projet couvre uniquement la simulation GPS — aucune intégration d'une API GTFS réelle n'est prévue dans cette version. Les données de lignes et arrêts sont définies manuellement pour les principales lignes de Martinique :

- **Ligne 1** — Fort-de-France ↔ Le Lamentin
- **Ligne 2** — Fort-de-France ↔ Schoelcher
- **Ligne 3** — Fort-de-France ↔ Le François

---

## 2. Analyse

### 2.1 Problématique

Comment fournir aux usagers du réseau de bus martiniquais une information en temps réel sur la position des véhicules, en simulant des données GPS fiables, tout en assurant une disponibilité continue sur web et mobile grâce à un pipeline CI/CD ?

### 2.2 Analyse des besoins

#### Besoins fonctionnels

- Simulation du déplacement des bus le long de leurs lignes (interpolation GPS, inversion de direction en bout de ligne).
- Mise à jour en temps réel de la position via WebSocket (toutes les 4 secondes).
- Consultation de la liste des lignes et des arrêts.
- Affichage cartographique interactif (Leaflet.js sur web, carte native sur Flutter).
- API REST documentée (Swagger/OpenAPI).
- Notifications push lors d'événements (bus proche d'un arrêt, perturbation).
- Application mobile Flutter (iOS/Android).

#### Besoins non fonctionnels

- **Performances** : réponse API < 200 ms, mise à jour position toutes les 4 secondes.
- **Disponibilité** : déploiement continu en production (uptime > 99 %).
- **Maintenabilité** : code POO structuré, tests unitaires (couverture > 70 %), documentation.
- **Sécurité** : validation des entrées, gestion des erreurs HTTP, CORS configuré.
- **Compatibilité mobile** : Flutter supporte iOS et Android depuis une base de code unique.

### 2.3 Analyse de l'existant

Aucune solution open source gratuite ne couvre le temps réel des bus en Martinique. Le réseau CFTU/Mozaïk ne propose pas d'API publique de géolocalisation. Ce projet comble ce vide en proposant une simulation réaliste et une stack moderne déployable en production.

---

## 3. Conception

### 3.1 Architecture générale

L'application suit une architecture multi-tiers découplée :

```
┌─────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│  Frontend Web   │    │   Backend FastAPI     │    │  App Mobile      │
│  Next.js 14     │◄──►│   Python POO          │◄──►│  Flutter         │
│  Vercel         │    │   PostgreSQL          │    │  iOS / Android   │
└─────────────────┘    │   Railway             │    └──────────────────┘
                       │                      │
                       │  ┌────────────────┐  │
                       │  │ Simulateur GPS │  │
                       │  │ BackgroundTask │  │
                       │  └────────────────┘  │
                       └──────────────────────┘
```

- **Frontend web** : Next.js 14 + Tailwind CSS + Leaflet.js (déployé sur Vercel).
- **Backend** : API FastAPI exposant les endpoints REST et WebSocket.
- **Simulation** : moteur GPS tournant en BackgroundTask, diffusant via WebSocket.
- **Mobile** : application Flutter consommant la même API REST + WebSocket.
- **Base de données** : PostgreSQL (SQLAlchemy async + Alembic).

### 3.2 Modèle de données

#### Entités principales

| Entité | Attributs clés | Description |
|---|---|---|
| `Ligne` | id, nom, couleur, description, actif | Ligne de bus (ex : Ligne 1 Fort-de-France → Lamentin) |
| `Arrêt` | id, nom, latitude, longitude, ordre, ligne_id | Point d'arrêt géolocalisé sur une ligne |
| `Bus` | id, nom, latitude, longitude, vitesse, statut, arret_courant_idx, direction, ligne_id | Véhicule simulé avec position GPS courante |
| `PositionHistorique` | id, bus_id, latitude, longitude, timestamp | Enregistrement de position à un instant t |
| `PushSubscription` | id, endpoint, p256dh, auth | Abonnement Web Push d'un navigateur |

#### Modèle POO (classes Python)

```
Bus ──────────────► Ligne ──────────────► Arrêt[]
 │  avancer()        │  get_arret(idx)
 │  _haversine()     │  nombre_arrets()
 │  to_dict()        │
 └─ direction: ±1    └─ couleur, arrets[]
```

### 3.3 IHM — Interfaces principales

#### Web (Next.js)

**Page `/` — Carte principale**
- Carte Leaflet.js centrée sur la Martinique.
- Marqueurs bus animés colorés par ligne.
- Sidebar gauche : filtre par ligne + liste des bus actifs.
- Panneau détail bus au clic (position GPS, vitesse, prochain arrêt).
- Indicateur de connexion WebSocket (vert/rouge) dans la navbar.
- Toggle dark mode / light mode persistant.

**Page `/lignes` — Liste des lignes**
- Grille de cartes par ligne avec couleur, nom, nombre d'arrêts.

**Page `/lignes/[id]` — Détail d'une ligne**
- Tracé des arrêts en timeline verticale.
- Liste des bus actifs sur la ligne avec statut.

**Page `/bus/[id]` — Détail d'un bus**
- Position GPS, vitesse, arrêt courant, prochain arrêt.
- Lien vers la ligne associée.

#### Mobile (Flutter)
- Écran carte avec marqueurs bus temps réel.
- Écran liste des lignes.
- Écran détail ligne / bus.
- Notifications push via FCM.

### 3.4 Storyboard

Le parcours utilisateur principal (web) :

1. L'utilisateur ouvre l'application → la carte s'affiche centrée sur Fort-de-France.
2. Il voit les 6 bus actifs représentés par des marqueurs colorés animés.
3. Il clique sur une ligne dans le panneau → seuls les bus de cette ligne restent visibles.
4. Il clique sur un bus → un panneau affiche : ligne, prochain arrêt, vitesse, GPS.
5. Les positions se rafraîchissent automatiquement toutes les 4 secondes via WebSocket.
6. Il navigue vers `/lignes` pour voir toutes les lignes disponibles.

---

## 4. Stack technique

| Couche | Technologie | Rôle |
|---|---|---|
| **Backend** | Python 3.11 + FastAPI 0.111 | API REST + WebSocket + simulation GPS |
| **POO** | Classes Python (Bus, Ligne, Arrêt, SimulateurGPS) | Logique métier, interpolation GPS Haversine |
| **Base de données** | PostgreSQL 16 | Stockage lignes, arrêts, historique positions, abonnements push |
| **ORM** | SQLAlchemy 2.0 async + Alembic | Modèles relationnels et migrations |
| **Validation** | Pydantic V2 + pydantic-settings | Schémas API et configuration |
| **Frontend web** | Next.js 14 + Tailwind CSS | Interface web responsive, dark/light mode |
| **Carte web** | Leaflet.js + react-leaflet | Carte interactive, marqueurs bus animés |
| **Application mobile** | Flutter (Dart) | iOS + Android depuis une base de code unique |
| **Notifications push (web)** | Web Push API + VAPID (pywebpush) | Notifications navigateur sans serveur tiers |
| **Notifications push (mobile)** | Firebase Cloud Messaging (FCM) | Notifications iOS et Android via Flutter |
| **Conteneurisation** | Docker + Docker Compose | Environnement reproductible dev/prod |
| **CI/CD** | GitHub Actions | Tests automatisés + déploiement continu |
| **Déploiement backend** | Railway | Hébergement API + PostgreSQL en production |
| **Déploiement frontend** | Vercel | Hébergement Next.js avec CDN global |
| **Documentation API** | Swagger UI (intégré FastAPI) | Documentation interactive auto-générée |
| **Tests** | pytest + pytest-asyncio + pytest-cov | Tests unitaires (16 tests, couverture > 70 %) |

---

## 5. Architecture technique

### 5.1 Structure du projet

#### Backend (`bustrack_mq/`)

```
bustrack_mq/
├── models/
│   ├── arret.py          # Dataclass Arrêt
│   ├── ligne.py          # Dataclass Ligne (get_arret, nombre_arrets)
│   └── bus.py            # Classe Bus (avancer, _haversine, to_dict)
├── simulation/
│   └── engine.py         # SimulateurGPS — BackgroundTask + broadcast WS
├── api/
│   ├── schemas.py        # Schémas Pydantic V2
│   └── routes/
│       ├── lignes.py     # GET /api/lignes, /api/lignes/{id}
│       ├── bus.py        # GET /api/bus, /api/bus/{id}
│       ├── websocket.py  # WS /ws/positions
│       └── notifications.py  # POST /api/notifications/subscribe
├── db/
│   ├── database.py       # Engine async, session, init_db()
│   └── models.py         # Modèles SQLAlchemy (LigneDB, BusDB, etc.)
├── core/
│   └── config.py         # Settings pydantic-settings
├── tests/
│   └── test_models.py    # 16 tests unitaires (16/16 ✅)
├── main.py               # Point d'entrée FastAPI + lifespan
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci-cd.yml
```

#### Frontend (`bustrack_mq_frontend/`)

```
bustrack_mq_frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Carte temps réel + sidebar
│   │   ├── layout.tsx            # Layout global + Navbar
│   │   ├── lignes/page.tsx       # Liste des lignes
│   │   ├── lignes/[id]/page.tsx  # Détail ligne
│   │   ├── bus/[id]/page.tsx     # Détail bus
│   │   └── not-found.tsx         # Page 404
│   ├── components/
│   │   ├── map/BusMap.tsx        # Carte Leaflet (dynamic, no SSR)
│   │   ├── map/Sidebar.tsx       # Panneau filtres + liste bus
│   │   ├── ui/Navbar.tsx         # Nav + dark mode + indicateur WS
│   │   └── ui/BadgeStatut.tsx    # Badge statut bus
│   ├── hooks/
│   │   ├── useBusPositions.ts    # WebSocket + reconnexion auto
│   │   └── useDarkMode.ts        # Toggle dark/light persistant
│   ├── lib/api.ts                # Client API centralisé
│   └── types/index.ts            # Types TypeScript partagés
└── vercel.json
```

### 5.2 Endpoints API

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/lignes` | Liste de toutes les lignes |
| `GET` | `/api/lignes/{id}` | Détail d'une ligne (arrêts + bus) |
| `GET` | `/api/bus` | Position actuelle de tous les bus actifs |
| `GET` | `/api/bus/{id}` | Détail d'un bus |
| `WS` | `/ws/positions` | Flux WebSocket — positions toutes les 4 s |
| `GET` | `/api/notifications/vapid-public-key` | Clé publique VAPID |
| `POST` | `/api/notifications/subscribe` | Enregistrement abonnement push |
| `DELETE` | `/api/notifications/unsubscribe` | Suppression abonnement push |
| `GET` | `/health` | Santé de l'API (CI/CD + monitoring) |

---

## 6. Plan, ressources et moyens

### 6.1 Planning prévisionnel

| Phase | Tâches | Livrables | Durée |
|---|---|---|---|
| 1 | Rédaction CDC + conception | CDC v2.0, diagrammes de classes | 1 semaine |
| 2 | Modèles POO + moteur simulation GPS | Classes Bus/Ligne/Arrêt + SimulateurGPS | 1,5 semaine |
| 3 | API FastAPI (REST + WebSocket) | Endpoints + Swagger + 16 tests ✅ | 1,5 semaine |
| 4 | Frontend Next.js (carte + pages) | Interface web fonctionnelle (MVP) | 1 semaine |
| 5 | Application mobile Flutter | App iOS/Android fonctionnelle | 1,5 semaine |
| 6 | Notifications push (Web Push + FCM) | Abonnements + envoi notifications | 0,5 semaine |
| 7 | Tests + Docker | Suite pytest + docker-compose | 0,5 semaine |
| 8 | CI/CD + déploiement production | Pipeline GitHub Actions + URL prod | 0,5 semaine |

### 6.2 Ressources humaines

- **Développeur solo** : Ibrahim (conception, développement, tests, déploiement).
- **Encadrement** : enseignant responsable du cours Backend (suivi hebdomadaire).

### 6.3 Ressources techniques

- **Machine de développement** : macOS, VS Code, Docker Desktop.
- **Hébergement backend** : Railway (gratuit pour projets étudiants).
- **Hébergement frontend** : Vercel (gratuit, CDN global).
- **Versioning** : GitHub (dépôt privé, branches `main` / `develop`).
- **IA assistante** : Claude Code (génération de code, revue, documentation).

---

## 7. MVP — Développement de l'application

### 7.1 Définition du MVP

Le Produit Minimum Viable comprend :

- Simulation de 3 lignes de bus avec 2 bus chacune (6 bus total).
- API REST retournant les positions en JSON.
- WebSocket diffusant les positions toutes les 4 secondes.
- Frontend web Next.js affichant la carte avec les bus animés.
- Application Flutter affichant la carte avec les bus en temps réel.
- Endpoint `/health` opérationnel pour le monitoring CI/CD.

### 7.2 Fonctionnalités post-MVP (V2)

- Authentification JWT pour un panneau d'administration.
- Historique persistant des positions en base de données.
- Intégration données GTFS réelles si disponibles.
- Calcul d'itinéraires et temps d'attente estimés.
- Mode hors ligne dans l'app Flutter.

### 7.3 Critères d'acceptation du MVP

| Critère | Indicateur de succès |
|---|---|
| Simulation GPS fonctionnelle | Bus se déplacent d'arrêt en arrêt en continu, inversion en bout de ligne |
| API REST opérationnelle | Tous les endpoints répondent < 200 ms |
| WebSocket temps réel | Mise à jour position toutes les 4 s côté client |
| Interface carte web | Bus visibles et animés sur Leaflet.js |
| Interface mobile Flutter | Bus visibles sur carte native iOS/Android |
| Tests | 16/16 tests unitaires passent (pytest) |
| Application déployée | URL publique accessible sans erreur 5xx |

---

## 8. Déploiement en production — CI/CD

### 8.1 Stratégie CI/CD

Le pipeline garantit que chaque modification du code est automatiquement testée et déployée en production sans intervention manuelle.

### 8.2 Pipeline GitHub Actions

**Étape 1 — Intégration Continue (CI)**

Déclencheur : push sur `main` ou `develop`, ouverture d'une Pull Request.

1. Checkout du code source.
2. Installation de Python 3.11 et des dépendances.
3. Lint avec `ruff`.
4. Exécution des tests avec `pytest --cov` (couverture > 70 % requise).
5. Build de l'image Docker et vérification d'intégrité.

**Étape 2 — Déploiement Continu (CD)**

Déclencheur : push sur `main` uniquement (après validation CI).

1. Push de l'image Docker vers GitHub Container Registry (`ghcr.io`).
2. Déploiement automatique sur Railway via Railway CLI.
3. Vérification de santé post-déploiement via `/health` (HTTP 200 attendu).
4. Rollback automatique en cas d'échec.

### 8.3 Environnements

| Environnement | Branche | Description |
|---|---|---|
| Développement | `develop` | Docker Compose local, SQLite possible |
| Staging | `develop → PR` | Tests CI automatiques, pas de déploiement |
| Production | `main` | Railway (backend) + Vercel (frontend), PostgreSQL, HTTPS |

### 8.4 Variables d'environnement

| Variable | Rôle |
|---|---|
| `DATABASE_URL` | URL de connexion PostgreSQL |
| `SECRET_KEY` | Clé secrète de l'API |
| `CORS_ORIGINS` | Domaines autorisés (frontend Vercel) |
| `RAILWAY_TOKEN` | Token d'authentification Railway (secret GitHub) |
| `RAILWAY_API_URL` | URL publique de l'API (health check post-déploiement) |
| `VAPID_PRIVATE_KEY` | Clé privée VAPID pour Web Push |
| `VAPID_PUBLIC_KEY` | Clé publique VAPID exposée au frontend |
| `SIMULATION_INTERVAL` | Intervalle de simulation GPS en secondes (défaut : 4) |

### 8.5 Schéma du pipeline

```
git push → GitHub
       ↓
GitHub Actions CI : ruff → pytest (16/16) → docker build
       ↓  (branche main uniquement)
GitHub Actions CD : docker push ghcr.io → railway deploy
       ↓
Vérification GET /health → HTTP 200
       ↓
Production en ligne ✓  (Railway + Vercel)
```

---

## 9. Application mobile Flutter

### 9.1 Description

L'application mobile BusTrack MQ est développée avec Flutter (Dart), permettant un déploiement simultané sur iOS et Android depuis une base de code unique. Elle consomme la même API FastAPI que le frontend web.

### 9.2 Écrans principaux

| Écran | Description |
|---|---|
| Carte principale | Carte native avec marqueurs bus animés temps réel (WebSocket) |
| Liste des lignes | Liste scrollable des lignes avec couleur et nombre d'arrêts |
| Détail d'une ligne | Timeline des arrêts + bus actifs sur la ligne |
| Détail d'un bus | Position GPS, vitesse, statut, prochain arrêt |
| Paramètres | Gestion des notifications push, thème |

### 9.3 Dépendances Flutter clés

- `flutter_map` — carte interactive (OpenStreetMap).
- `web_socket_channel` — connexion WebSocket temps réel.
- `http` — appels API REST.
- `firebase_messaging` — notifications push FCM.
- `provider` / `riverpod` — gestion d'état.

### 9.4 Notifications push mobile (FCM)

Les notifications push sur mobile utilisent **Firebase Cloud Messaging (FCM)**, intégré via le package `firebase_messaging`. Le backend FastAPI envoie les notifications FCM via l'API Firebase Admin SDK lorsqu'un événement le déclenche (bus proche d'un arrêt, perturbation de service).

---

## 10. Notifications push

### 10.1 Web Push (navigateurs)

- Protocole **Web Push API + VAPID** (Voluntary Application Server Identification).
- Bibliothèque backend : `pywebpush`.
- Clés générées avec `py-vapid` (`vapid --gen`).
- Les abonnements sont stockés en base (`PushSubscriptionDB`).
- Les abonnements expirés (404/410) sont automatiquement supprimés.

### 10.2 Mobile (FCM)

- **Firebase Cloud Messaging** via `firebase_messaging` (Flutter).
- Le token FCM de chaque appareil est envoyé au backend lors de l'inscription.
- Le backend stocke les tokens et les utilise pour cibler les notifications.

---

## 11. Analyse des risques

| Risque | Probabilité | Impact | Mesure de mitigation |
|---|---|---|---|
| Complexité simulation GPS temps réel | Moyenne | Élevé | Prototyper le moteur en priorité (Phase 2) ✅ fait |
| Latence WebSocket en production | Faible | Moyen | Tests de charge + polling en fallback |
| Dépassement du délai projet | Moyenne | Élevé | Scope MVP strict, features V2 différées |
| Incompatibilités dépendances Python | Faible | Moyen | Docker pour l'isolation des environnements ✅ fait |
| Quota gratuit Railway dépassé | Faible | Faible | Monitoring + Render en backup |
| Complexité Flutter WebSocket mobile | Faible | Moyen | `web_socket_channel` éprouvé, même logique que web |
| Clés VAPID mal configurées | Faible | Moyen | Script de génération documenté dans le README |

---

## 12. Conclusion

Le projet BusTrack MQ répond à une problématique concrète et locale : améliorer l'accès à l'information de transport en Martinique. En simulant des données GPS réalistes et en les exposant via une API FastAPI moderne, ce projet mobilise l'ensemble des compétences du cours de backend : conception POO, API REST, temps réel WebSocket, tests unitaires, containerisation Docker et déploiement CI/CD.

La solution couvre trois surfaces : un **frontend web** Next.js (Vercel), une **API backend** FastAPI (Railway) et une **application mobile** Flutter (iOS/Android), toutes interconnectées via la même API et le même flux WebSocket.

L'approche itérative (MVP d'abord, V2 ensuite) garantit la livraison d'un produit fonctionnel dans les délais impartis. Le pipeline CI/CD GitHub Actions assure une qualité de code continue et un déploiement fiable en production.

---

*Cahier des charges v2.0 — BusTrack MQ — Université des Antilles — Avril 2026*
