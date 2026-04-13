/**
 * routes/ligneRoutes.js
 * Endpoints REST pour les lignes de bus.
 */

const express = require('express');
const router  = express.Router();
const Ligne   = require('../models/Ligne');

// GET /api/lignes — Toutes les lignes actives
router.get('/', async (req, res) => {
  try {
    const lignes = await Ligne.findAll();
    res.json({ success: true, data: lignes });
  } catch (err) {
    console.error('Erreur GET /api/lignes :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

// GET /api/lignes/:id — Une ligne avec ses arrêts
router.get('/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (isNaN(id)) {
    return res.status(400).json({ success: false, error: 'ID invalide' });
  }
  try {
    const ligne = await Ligne.findById(id);
    if (!ligne) return res.status(404).json({ success: false, error: 'Ligne introuvable' });
    res.json({ success: true, data: ligne });
  } catch (err) {
    console.error('Erreur GET /api/lignes/:id :', err.message);
    res.status(500).json({ success: false, error: 'Erreur serveur' });
  }
});

module.exports = router;
