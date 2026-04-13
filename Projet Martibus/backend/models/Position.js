/**
 * models/Position.js
 * Requêtes SQL sur l'historique GPS.
 */

const pool = require('../config/db');

const Position = {
  /**
   * Retourne les N dernières positions d'un bus.
   * @param {number} busId
   * @param {number} limit  - Nombre de positions (défaut 50)
   */
  findByBus: async (busId, limit = 50) => {
    const { rows } = await pool.query(`
      SELECT id, bus_id, latitude, longitude, vitesse, cap, horodatage
      FROM positions_gps
      WHERE bus_id = $1
      ORDER BY horodatage DESC
      LIMIT $2
    `, [busId, limit]);
    return rows;
  },
};

module.exports = Position;
