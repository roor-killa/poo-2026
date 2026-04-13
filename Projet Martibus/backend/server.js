/**
 * server.js — Point d'entrée principal du backend MartiBus
 *
 * Stack : Express + Socket.io + PostgreSQL
 * Port  : 3001 (configurable via .env)
 */

require('dotenv').config();

const express    = require('express');
const http       = require('http');
const { Server } = require('socket.io');
const cors       = require('cors');

const busRoutes    = require('./routes/busRoutes');
const arretRoutes  = require('./routes/arretRoutes');
const ligneRoutes  = require('./routes/ligneRoutes');
const { demarrerSimulation } = require('./socket/gpsSimulator');

// ── Initialisation Express ────────────────────────────────────────────────────
const app    = express();
const server = http.createServer(app);

// ── Socket.io ─────────────────────────────────────────────────────────────────
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    methods: ['GET', 'POST'],
  },
});

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
}));
app.use(express.json());

// En-têtes de sécurité de base
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  next();
});

// ── Routes API REST ───────────────────────────────────────────────────────────
app.use('/api/bus',    busRoutes);
app.use('/api/arrets', arretRoutes);
app.use('/api/lignes', ligneRoutes);

// Route racine — check de santé
app.get('/', (req, res) => {
  res.json({
    app:     'MartiBus API',
    version: '1.0.0',
    status:  'ok',
    time:    new Date().toISOString(),
  });
});

// Gestion des routes inexistantes
app.use((req, res) => {
  res.status(404).json({ success: false, error: 'Route introuvable' });
});

// ── Événements WebSocket ──────────────────────────────────────────────────────
io.on('connection', (socket) => {
  console.log(`🔌 Client connecté : ${socket.id}`);

  socket.on('disconnect', () => {
    console.log(`🔌 Client déconnecté : ${socket.id}`);
  });
});

// ── Démarrage serveur ─────────────────────────────────────────────────────────
const PORT = parseInt(process.env.PORT || '3001', 10);

server.listen(PORT, () => {
  console.log(`🚌 MartiBus Backend démarré sur http://localhost:${PORT}`);
  console.log(`📡 WebSocket actif sur le même port`);

  // Lancement de la simulation GPS après démarrage
  demarrerSimulation(io).catch((err) => {
    console.error('❌ Erreur simulation GPS :', err.message);
  });
});
