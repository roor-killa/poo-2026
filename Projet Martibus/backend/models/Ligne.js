/**
 * models/Ligne.js
 * Requêtes SQL liées aux lignes de bus.
 * Fonctionne en mode PostgreSQL ou en mode mémoire (fallback).
 */

const { pool, memoryDB, isMemory } = require('../config/db');

const Ligne = {
  /** Retourne toutes les lignes actives. */
  findAll: async () => {
    if (isMemory()) return memoryDB.lignes.filter((l) => l.actif);
    const { rows } = await pool.query(`
      SELECT id, nom, couleur, description, actif
      FROM lignes
      WHERE actif = TRUE
      ORDER BY nom
    `);
    return rows;
  },

  /**
   * Retourne une ligne avec ses arrêts dans l'ordre.
   * @param {number} id
   */
  findById: async (id) => {
    if (isMemory()) return memoryDB.getLigneWithArrets(id);

    // Données de la ligne
    const { rows: ligneRows } = await pool.query(`
      SELECT id, nom, couleur, description, actif
      FROM lignes
      WHERE id = $1
    `, [id]);

    if (!ligneRows[0]) return null;

    // Arrêts de la ligne, dans l'ordre
    const { rows: arretRows } = await pool.query(`
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
    `, [id]);

    return { ...ligneRows[0], arrets: arretRows };
  },
};

module.exports = Ligne;
