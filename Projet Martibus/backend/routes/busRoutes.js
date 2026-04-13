/**
 * routes/busRoutes.js
 * Endpoints REST pour les bus.
 */

const express = require('express');
const router  = express.Router();
const Bus     = require('../models/Bus');

// GET /api/bus — Tous les bus actifs
router.get('/', async (req, res) => {
  try {
    const bus = await Bus.findAll();
    res.json({ success: true, data: bus });
  } catch (err) {
    console.error('Erreur GET /api/bus :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

// GET /api/bus/:id — Un bus spécifique
router.get('/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (isNaN(id)) {
    return res.status(400).json({ success: false, error: 'ID invalide' });
  }
  try {
    const bus = await Bus.findById(id);
    if (!bus) return res.status(404).json({ success: false, error: 'Bus introuvable' });
    res.json({ success: true, data: bus });
  } catch (err) {
    console.error('Erreur GET /api/bus/:id :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

module.exports = router;
