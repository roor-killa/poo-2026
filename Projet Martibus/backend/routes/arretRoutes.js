/**
 * routes/arretRoutes.js
 * Endpoints REST pour les arrêts.
 */

const express = require('express');
const router  = express.Router();
const Arret   = require('../models/Arret');

// GET /api/arrets — Tous les arrêts
router.get('/', async (req, res) => {
  try {
    const arrets = await Arret.findAll();
    res.json({ success: true, data: arrets });
  } catch (err) {
    console.error('Erreur GET /api/arrets :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

// GET /api/arrets/:id — Un arrêt spécifique
router.get('/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (isNaN(id)) {
    return res.status(400).json({ success: false, error: 'ID invalide' });
  }
  try {
    const arret = await Arret.findById(id);
    if (!arret) return res.status(404).json({ success: false, error: 'Arrêt introuvable' });
    res.json({ success: true, data: arret });
  } catch (err) {
    console.error('Erreur GET /api/arrets/:id :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

module.exports = router;
