/**
 * config/db.js
 *
 * Connexion PostgreSQL avec fallback automatique en mode "mémoire".
 * Si PostgreSQL n'est pas disponible, le serveur tourne avec des données
 * en RAM — utile pour démonstration sans base installée.
 */

const { Pool } = require('pg');

// ── Données en mémoire (fallback sans PostgreSQL) ─────────────────────────────

const memDB = {
  lignes: [
    { id: 1, nom: 'Ligne 1 — Fort-de-France Centre',  couleur: '#e63946', description: 'Desserte du centre-ville', actif: true },
    { id: 2, nom: 'Ligne 2 — Le Lamentin',             couleur: '#2a9d8f', description: 'FdF ↔ Le Lamentin',        actif: true },
    { id: 3, nom: 'Ligne 3 — Schoelcher',              couleur: '#e9c46a', description: 'Desserte de Schoelcher',   actif: true },
    { id: 4, nom: 'Ligne 4 — Le Robert',               couleur: '#f4a261', description: 'FdF ↔ Le Robert',         actif: true },
  ],
  arrets: [
    { id: 1,  nom: 'Fort-de-France — Pointe Simon',         latitude: 14.6099, longitude: -61.0731 },
    { id: 2,  nom: 'Fort-de-France — Cathédrale',           latitude: 14.6075, longitude: -61.0680 },
    { id: 3,  nom: 'Fort-de-France — Marché',               latitude: 14.6060, longitude: -61.0660 },
    { id: 4,  nom: 'Fort-de-France — Hôpital Pierre Zobda', latitude: 14.6120, longitude: -61.0600 },
    { id: 5,  nom: 'Le Lamentin — Centre commercial',       latitude: 14.5965, longitude: -60.9958 },
    { id: 6,  nom: 'Le Lamentin — Aéroport',                latitude: 14.5961, longitude: -60.9960 },
    { id: 7,  nom: 'Schoelcher — Université',               latitude: 14.6330, longitude: -61.0850 },
    { id: 8,  nom: 'Schoelcher — Centre',                   latitude: 14.6310, longitude: -61.0840 },
    { id: 9,  nom: 'Fort-de-France — Place Stalingrad',     latitude: 14.6090, longitude: -61.0700 },
    { id: 10, nom: 'Le Robert — Centre',                    latitude: 14.6800, longitude: -60.9300 },
  ],
  ligneArrets: [
    { ligne_id: 1, arret_id: 1, ordre: 1 }, { ligne_id: 1, arret_id: 9, ordre: 2 },
    { ligne_id: 1, arret_id: 2, ordre: 3 }, { ligne_id: 1, arret_id: 3, ordre: 4 },
    { ligne_id: 1, arret_id: 4, ordre: 5 },
    { ligne_id: 2, arret_id: 1, ordre: 1 }, { ligne_id: 2, arret_id: 9, ordre: 2 },
    { ligne_id: 2, arret_id: 5, ordre: 3 }, { ligne_id: 2, arret_id: 6, ordre: 4 },
    { ligne_id: 3, arret_id: 7, ordre: 1 }, { ligne_id: 3, arret_id: 8, ordre: 2 },
    { ligne_id: 3, arret_id: 1, ordre: 3 },
    { ligne_id: 4, arret_id: 1, ordre: 1 }, { ligne_id: 4, arret_id: 4, ordre: 2 },
    { ligne_id: 4, arret_id: 10, ordre: 3 },
  ],
  bus: [
    { id: 1, immatriculation: 'MAR-001', ligne_id: 1, latitude: 14.6099, longitude: -61.0731, vitesse: 0,  cap: 0,   actif: true, dernier_arret_id: 1 },
    { id: 2, immatriculation: 'MAR-002', ligne_id: 1, latitude: 14.6075, longitude: -61.0680, vitesse: 25, cap: 45,  actif: true, dernier_arret_id: 2 },
    { id: 3, immatriculation: 'MAR-003', ligne_id: 2, latitude: 14.5965, longitude: -60.9958, vitesse: 30, cap: 180, actif: true, dernier_arret_id: 5 },
    { id: 4, immatriculation: 'MAR-004', ligne_id: 2, latitude: 14.6060, longitude: -61.0660, vitesse: 20, cap: 90,  actif: true, dernier_arret_id: null },
    { id: 5, immatriculation: 'MAR-005', ligne_id: 3, latitude: 14.6330, longitude: -61.0850, vitesse: 35, cap: 270, actif: true, dernier_arret_id: 7 },
    { id: 6, immatriculation: 'MAR-006', ligne_id: 4, latitude: 14.6800, longitude: -60.9300, vitesse: 15, cap: 225, actif: true, dernier_arret_id: null },
  ],
};

function getLigne(id) { return memDB.lignes.find((l) => l.id === id) || null; }
function getArret(id) { return memDB.arrets.find((a) => a.id === id) || null; }
function getArretsByLigne(ligneId) {
  return memDB.ligneArrets
    .filter((la) => la.ligne_id === ligneId)
    .sort((a, b) => a.ordre - b.ordre)
    .map((la) => ({ ...getArret(la.arret_id), ordre: la.ordre }));
}

exports.memoryDB = {
  lignes:  memDB.lignes,
  arrets:  memDB.arrets,
  bus:     memDB.bus,
  getLigne,
  getArret,
  getArretsByLigne,
  getLigneWithArrets: (id) => {
    const l = getLigne(id);
    if (!l) return null;
    return { ...l, arrets: getArretsByLigne(id) };
  },
  getBusEnrichi: () => memDB.bus
    .filter((b) => b.actif)
    .map((b) => ({
      ...b,
      ligne_nom:         b.ligne_id  ? getLigne(b.ligne_id)?.nom     : null,
      ligne_couleur:     b.ligne_id  ? getLigne(b.ligne_id)?.couleur  : null,
      dernier_arret_nom: b.dernier_arret_id ? getArret(b.dernier_arret_id)?.nom : null,
      mis_a_jour:        new Date().toISOString(),
    })),
  updateBusPosition: (id, latitude, longitude, vitesse, cap) => {
    const bus = memDB.bus.find((b) => b.id === id);
    if (bus) { bus.latitude = latitude; bus.longitude = longitude; bus.vitesse = vitesse; bus.cap = cap; }
  },
};

// ── Tentative de connexion PostgreSQL ─────────────────────────────────────────
// Par défaut : mode mémoire. Bascule vers PostgreSQL si la connexion réussit.

let _useMemory = true;

const pool = new Pool({
  host:     process.env.DB_HOST     || 'localhost',
  port:     parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME     || 'martibus',
  user:     process.env.DB_USER     || 'postgres',
  password: process.env.DB_PASSWORD || '',
  connectionTimeoutMillis: 3000,
});

pool.connect((err, client, release) => {
  if (err) {
    _useMemory = true;
    console.warn('⚠️  PostgreSQL indisponible — mode mémoire activé (données simulées)');
    return;
  }
  release();
  _useMemory = false;
  console.log('✅ Connexion PostgreSQL établie');
});

exports.pool     = pool;
exports.isMemory = () => _useMemory;
