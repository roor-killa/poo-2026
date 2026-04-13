# Fiche de Spécification Technique — Système de Suivi en Temps Réel des Bus Publics

**Version :** 1.0  
**Date :** 13 avril 2026  
**Statut :** Draft

---

## 1. Architecture Générale

### 1.1 Composants

| Composant | Rôle | Technologie |
|---|---|---|
| Client embarqué | Envoi GPS toutes les 5 s | Python 3.11+, `requests`, `gpsd`, Raspberry Pi |
| Serveur central | Réception, traitement, diffusion | Python 3.11+, FastAPI, Uvicorn, PostgreSQL 16 |
| Interface admin | Gestion et monitoring (localhost) | HTML/JS (servie par FastAPI), WebSocket |
| Site public | Consultation usagers | HTML/JS statique, WebSocket |
| Base de données | Persistance | PostgreSQL 16 + extension PostGIS |

### 1.2 Schéma de flux

```
[Bus N — Raspberry Pi]
        │
        │  POST /api/v1/positions  (toutes les 5 s, HTTPS)
        ▼
[Serveur FastAPI]
        │
        ├──▶ [PostgreSQL + PostGIS]   (écriture position, calcul ETA)
        │
        ├──▶ [WebSocket /ws/buses]    ──▶  Site public (lecture seule)
        │
        └──▶ [WebSocket /ws/admin]    ──▶  Interface admin (localhost)
```

### 1.3 Réseau et sécurité

- Communication client → serveur : HTTPS (TLS 1.3), authentification par token API (header `Authorization: Bearer <token>`).
- Interface admin : écoute uniquement sur `127.0.0.1:8080`. Accès externe interdit.
- API publique et site public : port `443` (reverse proxy nginx recommandé).
- Rate limiting API publique : 1 requête / 5 s par IP (middleware FastAPI + `slowapi`).

---

## 2. Modèle de Données — PostgreSQL + PostGIS

### 2.1 Table `routes` (Itinéraires)

```sql
CREATE TABLE routes (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(120) NOT NULL UNIQUE,   -- ex. "Ligne 3 — Centre → Aéroport"
    description   TEXT,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 2.2 Table `stops` (Arrêts)

```sql
CREATE TABLE stops (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(120) NOT NULL,           -- ex. "Place de la Liberté"
    location      GEOGRAPHY(POINT, 4326) NOT NULL, -- coordonnées GPS (lon, lat)
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_stops_location ON stops USING GIST(location);
```

### 2.3 Table `route_stops` (Séquence arrêts/itinéraire)

```sql
CREATE TABLE route_stops (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id      UUID NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    stop_id       UUID NOT NULL REFERENCES stops(id) ON DELETE CASCADE,
    stop_order    SMALLINT NOT NULL,               -- position dans la séquence (1, 2, 3…)
    distance_from_prev_m  DOUBLE PRECISION,        -- distance depuis l'arrêt précédent (mètres)
    UNIQUE (route_id, stop_order)
);
```

### 2.4 Table `buses`

```sql
CREATE TABLE buses (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code          VARCHAR(20) NOT NULL UNIQUE,     -- identifiant court, ex. "BUS-042"
    label         VARCHAR(80),                     -- description visible, ex. "Mercedes Citaro #42"
    route_id      UUID REFERENCES routes(id) ON DELETE SET NULL,
    api_token     VARCHAR(128) NOT NULL UNIQUE,    -- token d'authentification du client embarqué
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 2.5 Table `positions` (Journal des positions GPS)

```sql
CREATE TABLE positions (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bus_id        UUID NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
    location      GEOGRAPHY(POINT, 4326) NOT NULL,
    speed_kmh     DOUBLE PRECISION,                -- vitesse instantanée (km/h)
    heading       DOUBLE PRECISION,                -- cap en degrés (0-360)
    recorded_at   TIMESTAMPTZ NOT NULL,            -- horodatage côté client
    received_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Partition par semaine recommandée pour les gros volumes
CREATE INDEX idx_positions_bus_time ON positions (bus_id, recorded_at DESC);
CREATE INDEX idx_positions_location ON positions USING GIST(location);
```

### 2.6 Table `segment_speeds` (Vitesse moyenne historique par segment)

```sql
CREATE TABLE segment_speeds (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id        UUID NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    from_stop_order SMALLINT NOT NULL,
    to_stop_order   SMALLINT NOT NULL,
    hour_bucket     SMALLINT NOT NULL CHECK (hour_bucket BETWEEN 0 AND 23), -- tranche horaire
    day_type        VARCHAR(10) NOT NULL DEFAULT 'weekday', -- 'weekday' | 'weekend'
    avg_speed_kmh   DOUBLE PRECISION NOT NULL,
    sample_count    INTEGER NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (route_id, from_stop_order, to_stop_order, hour_bucket, day_type)
);
```

### 2.7 Table `bus_status` (Vue matérialisée ou cache)

```sql
CREATE TABLE bus_status (
    bus_id              UUID PRIMARY KEY REFERENCES buses(id) ON DELETE CASCADE,
    last_location       GEOGRAPHY(POINT, 4326),
    last_speed_kmh      DOUBLE PRECISION,
    last_seen_at        TIMESTAMPTZ,
    is_online           BOOLEAN NOT NULL DEFAULT FALSE,
    current_stop_id     UUID REFERENCES stops(id),       -- NULL si entre deux arrêts
    next_stop_id        UUID REFERENCES stops(id),
    eta_next_stop_s     INTEGER,                          -- secondes estimées avant prochain arrêt
    eta_terminus_s      INTEGER,                          -- secondes estimées avant terminus
    progress_pct        DOUBLE PRECISION,                 -- 0.0 → 100.0, progression sur l'itinéraire
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 3. Endpoints API

### 3.1 API privée — Client embarqué

| Méthode | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/positions` | Bearer token (bus) | Envoi d'une position GPS |

**Corps de la requête :**

```json
{
  "latitude": 14.6042,
  "longitude": -61.0690,
  "speed_kmh": 32.5,
  "heading": 180.0,
  "recorded_at": "2026-04-13T14:22:05.123Z"
}
```

**Réponse 201 :**

```json
{
  "status": "ok",
  "bus_id": "uuid",
  "server_time": "2026-04-13T14:22:05.200Z"
}
```

**Codes d'erreur :** `401` token invalide, `422` données invalides, `429` rate limit.

### 3.2 API publique — REST

Base URL : `/api/v1/public`

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/routes` | Liste des itinéraires actifs avec arrêts |
| `GET` | `/routes/{route_id}` | Détail d'un itinéraire (arrêts, géométrie) |
| `GET` | `/buses` | Liste des bus actifs avec position, statut, ETA |
| `GET` | `/buses/{bus_id}` | Détail d'un bus (position, ETA, historique récent) |
| `GET` | `/stops/{stop_id}/arrivals` | Prochains bus pour un arrêt donné avec ETA |

**Rate limit :** 1 requête / 5 s par IP. Header de réponse : `X-RateLimit-Remaining`, `Retry-After`.

**Exemple de réponse `GET /buses` :**

```json
[
  {
    "bus_id": "uuid",
    "code": "BUS-042",
    "route": { "id": "uuid", "name": "Ligne 3" },
    "location": { "lat": 14.6042, "lon": -61.0690 },
    "speed_kmh": 32.5,
    "is_online": true,
    "last_seen_at": "2026-04-13T14:22:05Z",
    "offline_since_s": null,
    "current_stop": null,
    "next_stop": { "id": "uuid", "name": "Mairie", "eta_seconds": 120 },
    "terminus": { "id": "uuid", "name": "Aéroport", "eta_seconds": 1830 },
    "progress_pct": 45.2
  }
]
```

### 3.3 API admin — REST (localhost uniquement)

Base URL : `/api/v1/admin`

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/buses` | Tous les bus (actifs + inactifs) |
| `POST` | `/buses` | Créer un bus (retourne le token API) |
| `PUT` | `/buses/{bus_id}` | Modifier un bus |
| `DELETE` | `/buses/{bus_id}` | Désactiver un bus |
| `GET` | `/routes` | Tous les itinéraires |
| `POST` | `/routes` | Créer un itinéraire + arrêts |
| `PUT` | `/routes/{route_id}` | Modifier un itinéraire |
| `DELETE` | `/routes/{route_id}` | Désactiver un itinéraire |
| `POST` | `/stops` | Créer un arrêt |
| `PUT` | `/stops/{stop_id}` | Modifier un arrêt |
| `DELETE` | `/stops/{stop_id}` | Supprimer un arrêt |

---

## 4. Schéma WebSocket

### 4.1 Canal public — `ws://host/ws/buses`

**Direction serveur → client.** Pas de message client → serveur attendu.

Le serveur pousse un snapshot toutes les 5 secondes :

```json
{
  "type": "snapshot",
  "timestamp": "2026-04-13T14:22:05Z",
  "buses": [
    {
      "bus_id": "uuid",
      "code": "BUS-042",
      "route_id": "uuid",
      "route_name": "Ligne 3",
      "lat": 14.6042,
      "lon": -61.0690,
      "speed_kmh": 32.5,
      "heading": 180.0,
      "is_online": true,
      "offline_since_s": null,
      "current_stop": null,
      "next_stop": { "id": "uuid", "name": "Mairie", "eta_s": 120 },
      "terminus_eta_s": 1830,
      "progress_pct": 45.2
    }
  ]
}
```

**Événement ponctuel (optionnel, en complément du snapshot) :**

```json
{
  "type": "bus_offline",
  "bus_id": "uuid",
  "last_seen_at": "2026-04-13T14:20:00Z"
}
```

### 4.2 Canal admin — `ws://localhost:8080/ws/admin`

Même format que le canal public, enrichi de champs supplémentaires :

- `api_token` (masqué partiellement)
- `is_active` (flag admin)
- `positions_last_hour` (compteur de pings reçus)

---

## 5. Logique Métier

### 5.1 Détection d'arrêt

Un bus est considéré **à l'arrêt N** lorsque :

```
ST_DWithin(bus.location, stop.location, 100)  -- distance ≤ 100 m
```

- Le `current_stop_id` est mis à jour dans `bus_status`.
- Le `next_stop_id` passe à l'arrêt suivant dans la séquence `route_stops.stop_order`.
- Si le bus est au dernier arrêt (terminus), `next_stop_id = NULL` et `eta_terminus_s = 0`.

### 5.2 Calcul de l'ETA

**Données d'entrée :**

1. `d_remaining` — distance GPS en ligne droite entre la position actuelle du bus et le prochain arrêt (mètres). Pour plus de précision, cumuler les distances par segment `route_stops.distance_from_prev_m`.
2. `v_avg` — vitesse moyenne historique sur le segment actuel, tirée de `segment_speeds` pour la tranche horaire courante et le type de jour.
3. `v_instant` — vitesse instantanée du bus (`speed_kmh`).

**Formule — ETA prochain arrêt :**

```
v_effective = 0.7 × v_avg + 0.3 × v_instant      (pondération configurable)
eta_next_stop_s = d_remaining / (v_effective / 3.6) -- conversion km/h → m/s
```

**Formule — ETA terminus :**

```
eta_terminus_s = eta_next_stop_s
                + Σ (distance_segment_i / (v_avg_segment_i / 3.6))
                  pour chaque segment restant jusqu'au terminus
```

**Cas limites :**

- Si `v_effective < 2 km/h` (bus très lent ou à l'arrêt) : utiliser `v_avg` seul.
- Si aucune donnée historique (`sample_count = 0`) : utiliser une vitesse par défaut de 20 km/h.
- Si le bus est au terminus : `eta_next_stop_s = NULL`, `eta_terminus_s = 0`.

### 5.3 Calcul de la progression

```
progress_pct = (distance parcourue depuis le départ) / (distance totale de l'itinéraire) × 100
```

La distance parcourue est estimée comme la somme des `distance_from_prev_m` jusqu'à l'arrêt précédent + la distance entre l'arrêt précédent et la position actuelle.

### 5.4 Gestion des pannes / hors ligne

**Paramètres :**

| Paramètre | Valeur par défaut |
|---|---|
| `OFFLINE_THRESHOLD_S` | 30 (secondes sans signal) |
| `STALE_THRESHOLD_S` | 300 (5 min — alerte critique) |

**Logique (exécutée par un job asyncio toutes les 10 s) :**

```python
now = datetime.utcnow()
for bus in bus_status_cache:
    delta = (now - bus.last_seen_at).total_seconds()
    if delta > OFFLINE_THRESHOLD_S:
        bus.is_online = False
        bus.offline_since_s = int(delta)
        # La dernière position connue reste affichée
        # L'ETA n'est plus calculé (affiché comme "indisponible")
    else:
        bus.is_online = True
        bus.offline_since_s = None
```

**Conséquences sur l'affichage :**

- Bus hors ligne : icône grisée, tooltip "Hors ligne depuis X min", ETA remplacé par "—".
- Bus hors ligne > `STALE_THRESHOLD_S` : badge rouge "Perte de signal".

### 5.5 Mise à jour des vitesses historiques

Après chaque passage d'un bus entre deux arrêts consécutifs (détection d'arrivée à l'arrêt N+1 après avoir été à l'arrêt N) :

```
temps_segment = arrivée_stop_N+1 - départ_stop_N
vitesse_segment = distance_segment / temps_segment
```

Mise à jour par moyenne mobile exponentielle dans `segment_speeds` :

```
new_avg = α × vitesse_segment + (1 − α) × old_avg     (α = 0.1)
sample_count += 1
```

---

## 6. Client Embarqué — Spécification

### 6.1 Matériel requis

- Raspberry Pi 3B+ ou supérieur (ou équivalent ARM)
- Module GPS USB (ex. u-blox 7) compatible `gpsd`
- Connexion 4G/LTE (clé USB ou HAT)
- Alimentation 5V depuis le réseau électrique du bus

### 6.2 Comportement

```
Boucle principale (toutes les 5 secondes) :
  1. Lire la position GPS depuis gpsd
  2. Si fix GPS valide :
       → POST /api/v1/positions avec lat, lon, vitesse, cap, timestamp
  3. Si fix GPS invalide :
       → Ne rien envoyer (le serveur détectera le silence)
  4. Si échec réseau :
       → Stocker la position dans un buffer local (file SQLite, max 1 000 entrées)
       → Retenter l'envoi du buffer au prochain cycle réussi
  5. Attendre 5 secondes
```

### 6.3 Résilience

- Redémarrage automatique du script via `systemd`.
- Watchdog matériel activé sur le Raspberry Pi.
- Logs locaux rotatifs (`/var/log/bus-client/`), rétention 7 jours.

---

## 7. Interfaces Utilisateur

### 7.1 Interface d'administration (localhost:8080)

**Page « Tableau de bord »**

- Carte interactive (Leaflet.js + OpenStreetMap) affichant en temps réel :
  - Position de chaque bus (icône colorée par itinéraire).
  - Tracé des itinéraires (polylignes).
  - Arrêts (marqueurs fixes).
  - Popup au clic sur un bus : code, itinéraire, vitesse, prochain arrêt + ETA, terminus + ETA, statut online/offline + durée.
- Tableau latéral listant tous les bus avec colonnes triables : Code, Ligne, Statut, Prochain arrêt, ETA, Dernier signal.
- Indicateur global : nombre de bus en ligne / total.
- Mise à jour via WebSocket `/ws/admin` (pas de polling).

**Page « Gestion des bus »**

- CRUD complet : formulaire de création (code, label, itinéraire affecté), modification, désactivation.
- Affichage du token API à la création (une seule fois, copier-coller).
- Indicateur de dernier signal pour chaque bus.

**Page « Gestion des itinéraires »**

- CRUD : nom, description, séquence d'arrêts.
- Sélection des arrêts par recherche ou clic sur carte.
- Réorganisation de l'ordre par glisser-déposer.
- Prévisualisation du tracé sur carte.

**Page « Gestion des arrêts »**

- CRUD : nom, coordonnées GPS (saisie manuelle ou clic sur carte).
- Liste avec filtre par itinéraire.

### 7.2 Site public

**Page unique — Vue temps réel**

- Carte plein écran (Leaflet.js + OpenStreetMap).
- Sélecteur de ligne (filtrer par itinéraire).
- Position des bus en temps réel avec animation de déplacement fluide (interpolation entre snapshots).
- Au clic sur un bus : ligne, direction, prochain arrêt, ETA prochain arrêt, ETA terminus, statut.
- Au clic sur un arrêt : liste des prochains bus avec ETA.
- Indicateur visuel bus hors ligne (icône grisée + badge).
- Connexion via WebSocket `/ws/buses`.
- Responsive : utilisable sur mobile sans application native.
- Pas d'authentification requise.

---

## 8. Contraintes Techniques et Non-Fonctionnelles

| Contrainte | Valeur cible |
|---|---|
| Latence position → affichage | < 2 secondes |
| Capacité simultanée | 200 bus, 5 000 connexions WebSocket |
| Disponibilité serveur | 99.5 % (hors maintenance planifiée) |
| Rétention positions brutes | 90 jours (puis archivage ou purge) |
| Rétention vitesses historiques | Illimitée |
| Taille base estimée (1 an, 100 bus) | ~15 Go positions, ~50 Mo vitesses |
| Précision GPS requise | ≤ 10 m CEP |
| Fréquence d'envoi client | 5 s ± 500 ms |
| Rate limit API publique | 12 req/min par IP |

---

## 9. Stack Technique Récapitulative

| Couche | Technologie |
|---|---|
| Serveur API | Python 3.11+, FastAPI, Uvicorn (workers ASGI) |
| Base de données | PostgreSQL 16 + PostGIS 3.4 |
| ORM / migrations | SQLAlchemy 2.x + Alembic |
| WebSocket | FastAPI WebSocket natif |
| Rate limiting | slowapi (basé sur limits) |
| Cache en mémoire | dict Python (bus_status) ou Redis (si scaling) |
| Cartographie frontend | Leaflet.js 1.9 + OpenStreetMap tiles |
| Client embarqué | Python 3.11+, requests, gpsd-py3 |
| Déploiement serveur | Docker Compose (API + PostgreSQL + nginx) |
| Reverse proxy | nginx (TLS, routage admin/public) |
