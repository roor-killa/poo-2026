/**
 * models/Bus.js
 * Requêtes SQL liées aux bus.
 * Fonctionne en mode PostgreSQL ou en mode mémoire (fallback).
 */

const { pool, memoryDB, isMemory } = require('../config/db');

const Bus = {
  /**
   * Retourne tous les bus actifs avec leur position courante.
   */
  findAll: async () => {
    if (isMemory()) return memoryDB.getBusEnrichi();
    const { rows } = await pool.query(`
      SELECT
        b.id,
        b.immatriculation,
        b.ligne_id,
        l.nom        AS ligne_nom,
        l.couleur    AS ligne_couleur,
        b.latitude,
        b.longitude,
        b.vitesse,
        b.cap,
        b.actif,
        b.dernier_arret_id,
        a.nom        AS dernier_arret_nom,
        b.mis_a_jour
      FROM bus b
      LEFT JOIN lignes  l ON l.id = b.ligne_id
      LEFT JOIN arrets  a ON a.id = b.dernier_arret_id
      WHERE b.actif = TRUE
      ORDER BY b.id
    `);
    return rows;
  },

  /**
   * Retourne un bus par son identifiant.
   * @param {number} id
   */
  findById: async (id) => {
    if (isMemory()) {
      return memoryDB.getBusEnrichi().find((b) => b.id === id) || null;
    }
    const { rows } = await pool.query(`
      SELECT
        b.id,
        b.immatriculation,
        b.ligne_id,
        l.nom        AS ligne_nom,
        l.couleur    AS ligne_couleur,
        b.latitude,
        b.longitude,
        b.vitesse,
        b.cap,
        b.actif,
        b.dernier_arret_id,
        a.nom        AS dernier_arret_nom,
        b.mis_a_jour
      FROM bus b
      LEFT JOIN lignes  l ON l.id = b.ligne_id
      LEFT JOIN arrets  a ON a.id = b.dernier_arret_id
      WHERE b.id = $1
    `, [id]);
    return rows[0] || null;
  },

  /**
   * Met à jour la position GPS d'un bus et insère un historique.
   * @param {number} id        - ID du bus
   * @param {number} latitude
   * @param {number} longitude
   * @param {number} vitesse   - en km/h
   * @param {number} cap       - en degrés
   */
  updatePosition: async (id, latitude, longitude, vitesse, cap) => {
    if (isMemory()) {
      memoryDB.updateBusPosition(id, latitude, longitude, vitesse, cap);
      return;
    }
    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Mise à jour position courante
      await client.query(`
        UPDATE bus
        SET latitude   = $1,
            longitude  = $2,
            vitesse    = $3,
            cap        = $4,
            mis_a_jour = NOW()
        WHERE id = $5
      `, [latitude, longitude, vitesse, cap, id]);

      // Enregistrement dans l'historique
      await client.query(`
        INSERT INTO positions_gps (bus_id, latitude, longitude, vitesse, cap)
        VALUES ($1, $2, $3, $4, $5)
      `, [id, latitude, longitude, vitesse, cap]);

      await client.query('COMMIT');
    } catch (err) {
      await client.query('ROLLBACK');
      throw err;
    } finally {
      client.release();
    }
  },
};

module.exports = Bus;
