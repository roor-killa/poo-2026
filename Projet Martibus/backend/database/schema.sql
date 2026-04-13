-- ============================================================
-- MartiBus — Schéma de base de données PostgreSQL
-- ============================================================

-- Extension pour les UUID (optionnelle)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------------------------------------------
-- Table : lignes
-- Représente une ligne de bus (ex : Ligne 1 - Fort-de-France)
-- ------------------------------------------------------------
CREATE TABLE lignes (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(100)  NOT NULL,
    couleur     VARCHAR(7)    NOT NULL DEFAULT '#3388ff', -- Couleur HEX pour la carte
    description TEXT,
    actif       BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Table : arrets
-- Représente un arrêt de bus (point géographique)
-- ------------------------------------------------------------
CREATE TABLE arrets (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(150)  NOT NULL,
    latitude    DOUBLE PRECISION NOT NULL,
    longitude   DOUBLE PRECISION NOT NULL,
    description TEXT,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Table : ligne_arrets
-- Relation N-N ordonnée entre lignes et arrêts
-- (un arrêt peut appartenir à plusieurs lignes, avec un ordre)
-- ------------------------------------------------------------
CREATE TABLE ligne_arrets (
    id          SERIAL PRIMARY KEY,
    ligne_id    INTEGER NOT NULL REFERENCES lignes(id) ON DELETE CASCADE,
    arret_id    INTEGER NOT NULL REFERENCES arrets(id) ON DELETE CASCADE,
    ordre       INTEGER NOT NULL,  -- Position dans la séquence de la ligne
    UNIQUE (ligne_id, arret_id),
    UNIQUE (ligne_id, ordre)
);

-- ------------------------------------------------------------
-- Table : bus
-- Représente un véhicule (bus) en service
-- ------------------------------------------------------------
CREATE TABLE bus (
    id          SERIAL PRIMARY KEY,
    immatriculation VARCHAR(20) NOT NULL UNIQUE,
    ligne_id    INTEGER REFERENCES lignes(id) ON DELETE SET NULL,
    latitude    DOUBLE PRECISION,       -- Position courante
    longitude   DOUBLE PRECISION,       -- Position courante
    vitesse     DOUBLE PRECISION DEFAULT 0,  -- km/h
    cap         DOUBLE PRECISION DEFAULT 0,  -- En degrés (0-360)
    actif       BOOLEAN NOT NULL DEFAULT TRUE,
    dernier_arret_id INTEGER REFERENCES arrets(id) ON DELETE SET NULL,
    mis_a_jour  TIMESTAMP DEFAULT NOW(),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Table : positions_gps
-- Historique des positions GPS des bus
-- ------------------------------------------------------------
CREATE TABLE positions_gps (
    id          BIGSERIAL PRIMARY KEY,
    bus_id      INTEGER NOT NULL REFERENCES bus(id) ON DELETE CASCADE,
    latitude    DOUBLE PRECISION NOT NULL,
    longitude   DOUBLE PRECISION NOT NULL,
    vitesse     DOUBLE PRECISION DEFAULT 0,
    cap         DOUBLE PRECISION DEFAULT 0,
    horodatage  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index pour les requêtes fréquentes sur l'historique
CREATE INDEX idx_positions_bus_id ON positions_gps(bus_id);
CREATE INDEX idx_positions_horodatage ON positions_gps(horodatage DESC);
CREATE INDEX idx_bus_ligne_id ON bus(ligne_id);
CREATE INDEX idx_ligne_arrets_ligne ON ligne_arrets(ligne_id);

-- ============================================================
-- DONNÉES DE TEST — Martinique (coordonnées réelles)
-- ============================================================

-- Lignes de bus
INSERT INTO lignes (nom, couleur, description) VALUES
    ('Ligne 1 — Fort-de-France Centre',   '#e63946', 'Desserte du centre-ville de Fort-de-France'),
    ('Ligne 2 — Le Lamentin',             '#2a9d8f', 'Liaison Fort-de-France ↔ Le Lamentin'),
    ('Ligne 3 — Schoelcher',              '#e9c46a', 'Desserte de Schoelcher'),
    ('Ligne 4 — Le Robert',               '#f4a261', 'Liaison Fort-de-France ↔ Le Robert');

-- Arrêts réels en Martinique
INSERT INTO arrets (nom, latitude, longitude) VALUES
    ('Fort-de-France — Pointe Simon',        14.6099, -61.0731),
    ('Fort-de-France — Cathédrale',          14.6075, -61.0680),
    ('Fort-de-France — Marché',              14.6060, -61.0660),
    ('Fort-de-France — Hôpital Pierre Zobda',14.6120, -61.0600),
    ('Le Lamentin — Centre commercial',      14.5965, -60.9958),
    ('Le Lamentin — Aéroport',               14.5961, -60.9960),
    ('Schoelcher — Université',              14.6330, -61.0850),
    ('Schoelcher — Centre',                  14.6310, -61.0840),
    ('Fort-de-France — Place Stalingrad',    14.6090, -61.0700),
    ('Le Robert — Centre',                   14.6800, -60.9300);

-- Association lignes ↔ arrêts (avec ordre)
INSERT INTO ligne_arrets (ligne_id, arret_id, ordre) VALUES
    (1, 1, 1), (1, 9, 2), (1, 2, 3), (1, 3, 4), (1, 4, 5),
    (2, 1, 1), (2, 9, 2), (2, 5, 3), (2, 6, 4),
    (3, 7, 1), (3, 8, 2), (3, 1, 3),
    (4, 1, 1), (4, 4, 2), (4, 10, 3);

-- Bus en service
INSERT INTO bus (immatriculation, ligne_id, latitude, longitude, vitesse, cap, actif) VALUES
    ('MAR-001', 1, 14.6099, -61.0731, 0,   0,   TRUE),
    ('MAR-002', 1, 14.6075, -61.0680, 25,  45,  TRUE),
    ('MAR-003', 2, 14.5965, -60.9958, 30,  180, TRUE),
    ('MAR-004', 2, 14.6060, -61.0660, 20,  90,  TRUE),
    ('MAR-005', 3, 14.6330, -61.0850, 35,  270, TRUE),
    ('MAR-006', 4, 14.6800, -60.9300, 15,  225, TRUE);
