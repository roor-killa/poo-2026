/**
 * models/Arret.js
 * Requêtes SQL liées aux arrêts.
 * Fonctionne en mode PostgreSQL ou en mode mémoire (fallback).
 */

const { pool, memoryDB, isMemory } = require('../config/db');

const Arret = {
  /** Retourne tous les arrêts. */
  findAll: async () => {
    if (isMemory()) return memoryDB.arrets;
    const { rows } = await pool.query(`
      SELECT id, nom, latitude, longitude, description
      FROM arrets
      ORDER BY nom
    `);
    return rows;
  },

  /**
   * Retourne un arrêt par son identifiant.
   * @param {number} id
   */
  findById: async (id) => {
    if (isMemory()) return memoryDB.getArret(id);
    const { rows } = await pool.query(`
      SELECT id, nom, latitude, longitude, description
      FROM arrets
      WHERE id = $1
    `, [id]);
    return rows[0] || null;
  },

  /**
   * Retourne tous les arrêts d'une ligne donnée, dans l'ordre.
   * @param {number} ligneId
   */
  findByLigne: async (ligneId) => {
    if (isMemory()) return memoryDB.getArretsByLigne(ligneId);
    const { rows } = await pool.query(`
      SELECT
        a.id,
        a.nom,
        a.latitude,
        a.longitude,
        la.ordre
      FROM arrets a
      JOIN ligne_arrets la ON la.arret_id = a.id
      WHERE la.ligne_id = $1
      ORDER BY la.ordre
    `, [ligneId]);
    return rows;
  },
};

module.exports = Arret;
