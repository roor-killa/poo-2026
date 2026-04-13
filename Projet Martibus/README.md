# 🚌 MartiBus — Suivi des bus en temps réel (Martinique)

Application web de suivi des bus en temps réel basée sur React.js, Node.js,
Socket.io, PostgreSQL et Leaflet.js.

---

## Structure du projet

```
Projet Martibus/
├── README.md
├── backend/
│   ├── package.json
│   ├── .env.example
│   ├── server.js              # Point d'entrée principal
│   ├── config/
│   │   └── db.js              # Connexion PostgreSQL
│   ├── models/
│   │   ├── Bus.js
│   │   ├── Arret.js
│   │   ├── Ligne.js
│   │   └── Position.js
│   ├── routes/
│   │   ├── busRoutes.js
│   │   ├── arretRoutes.js
│   │   └── ligneRoutes.js
│   ├── socket/
│   │   └── gpsSimulator.js    # Simulation GPS toutes les 5 secondes
│   └── database/
│       └── schema.sql         # Script de création des tables
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── components/
│       │   ├── Map.jsx            # Carte Leaflet principale
│       │   ├── BusMarker.jsx      # Marqueur de bus
│       │   ├── StopMarker.jsx     # Marqueur d'arrêt
│       │   ├── LignePolyline.jsx  # Tracé de la ligne
│       │   └── InfoPanel.jsx      # Panneau d'info latéral
│       ├── hooks/
│       │   └── useSocket.js       # Hook de connexion WebSocket
│       ├── services/
│       │   └── api.js             # Appels REST
│       └── styles/
│           └── App.css
```

---

## Prérequis

- Node.js ≥ 18
- PostgreSQL ≥ 14
- npm ≥ 9

---

## Installation et lancement

### 1. Base de données

```bash
# Créer la base de données
psql -U postgres -c "CREATE DATABASE martibus;"

# Exécuter le schéma SQL
psql -U postgres -d martibus -f backend/database/schema.sql
```

### 2. Backend

```bash
cd backend
cp .env.example .env
# Éditer .env avec vos paramètres PostgreSQL
npm install
npm run dev
```

Le serveur démarre sur **http://localhost:3001**

### 3. Frontend

```bash
cd frontend
npm install
npm start
```

L'application s'ouvre sur **http://localhost:3000**

---

## API REST

| Méthode | Endpoint             | Description                        |
|---------|----------------------|------------------------------------|
| GET     | `/api/bus`           | Liste de tous les bus actifs        |
| GET     | `/api/bus/:id`       | Détail d'un bus                    |
| GET     | `/api/arrets`        | Liste de tous les arrêts           |
| GET     | `/api/arrets/:id`    | Détail d'un arrêt                  |
| GET     | `/api/lignes`        | Liste de toutes les lignes         |
| GET     | `/api/lignes/:id`    | Détail d'une ligne avec ses arrêts |

## WebSocket (Socket.io)

| Événement           | Direction       | Description                          |
|---------------------|-----------------|--------------------------------------|
| `bus:positions`     | Serveur → Client| Positions de tous les bus (5 sec)    |
| `bus:update`        | Serveur → Client| Mise à jour d'un bus spécifique      |

---

## Architecture

Voir les schémas `architecture_martiibus.svg` et `uml_cas_utilisation_martiibus.svg`
pour le détail de l'architecture en 5 couches (Clients → Frontend → Backend → BDD → IoT GPS).
