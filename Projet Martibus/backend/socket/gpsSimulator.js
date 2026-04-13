/**
 * socket/gpsSimulator.js
 *
 * Simule le mouvement des bus le long de leurs lignes.
 * Toutes les 5 secondes, chaque bus avance vers le prochain arrêt,
 * sa position est mise à jour (BDD ou mémoire) et diffusée via Socket.io.
 */

const Bus                          = require('../models/Bus');
const Arret                        = require('../models/Arret');
const { memoryDB }                 = require('../config/db');

// ── Constantes de simulation ──────────────────────────────────────────────────
const INTERVALLE_MS    = 5000;   // Fréquence de mise à jour (5 secondes)
const VITESSE_KMH      = 30;     // Vitesse fictive par défaut
const DISTANCE_ARRET_M = 50;     // Distance (mètres) pour considérer qu'on est à un arrêt

// ── Utilitaires géographiques ─────────────────────────────────────────────────

/**
 * Calcule la distance en mètres entre deux points GPS (formule de Haversine).
 */
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371000; // Rayon de la Terre en mètres
  const toRad = (deg) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/**
 * Calcule le cap en degrés entre deux points GPS.
 */
function calculerCap(lat1, lon1, lat2, lon2) {
  const toRad = (deg) => (deg * Math.PI) / 180;
  const toDeg = (rad) => (rad * 180) / Math.PI;
  const dLon = toRad(lon2 - lon1);
  const y = Math.sin(dLon) * Math.cos(toRad(lat2));
  const x =
    Math.cos(toRad(lat1)) * Math.sin(toRad(lat2)) -
    Math.sin(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.cos(dLon);
  return (toDeg(Math.atan2(y, x)) + 360) % 360;
}

/**
 * Interpole la position d'un bus se déplaçant à `vitesse` km/h pendant `dt` secondes.
 */
function interpoler(lat1, lon1, lat2, lon2, vitesseKmh, dtSecondes) {
  const distanceTotale = haversine(lat1, lon1, lat2, lon2);
  if (distanceTotale === 0) return { lat: lat2, lon: lon2 };

  const distanceParcourue = (vitesseKmh * 1000 / 3600) * dtSecondes;
  const ratio = Math.min(distanceParcourue / distanceTotale, 1);

  return {
    lat: lat1 + (lat2 - lat1) * ratio,
    lon: lon1 + (lon2 - lon1) * ratio,
  };
}

// ── État interne de la simulation ─────────────────────────────────────────────
// Clé : busId, Valeur : { arrets[], arretCourantIndex, lat, lon }
const etatsBus = new Map();

/**
 * Charge depuis la base les arrêts de chaque bus et initialise l'état.
 */
async function initialiserSimulation() {
  const busList = await Bus.findAll();

  for (const bus of busList) {
    if (!bus.ligne_id) continue;

    const arrets = await Arret.findByLigne(bus.ligne_id);
    if (arrets.length < 2) continue;

    etatsBus.set(bus.id, {
      arrets,
      arretCourantIndex: 0,      // Index de la destination actuelle
      lat: bus.latitude  || arrets[0].latitude,
      lon: bus.longitude || arrets[0].longitude,
      sensAller: true,           // true = aller, false = retour
    });
  }

  console.log(`🗺️  Simulation initialisée pour ${etatsBus.size} bus`);
}

/**
 * Calcule l'estimation d'arrivée (en minutes) pour un bus vers son prochain arrêt.
 */
function estimerArrivee(lat, lon, arretCible, vitesseKmh) {
  const distanceM = haversine(lat, lon, arretCible.latitude, arretCible.longitude);
  const vitesseMs = (vitesseKmh * 1000) / 3600;
  return Math.round((distanceM / vitesseMs) / 60); // En minutes
}

// ── Boucle principale de simulation ──────────────────────────────────────────

/**
 * Démarre la simulation GPS et la diffusion WebSocket.
 * @param {import('socket.io').Server} io  - Instance Socket.io
 */
async function demarrerSimulation(io) {
  await initialiserSimulation();

  setInterval(async () => {
    const positionsMises = [];

    for (const [busId, etat] of etatsBus.entries()) {
      const { arrets, sensAller } = etat;
      const indexDestination = sensAller
        ? etat.arretCourantIndex + 1
        : etat.arretCourantIndex - 1;

      // Inversion de sens en bout de ligne
      if (indexDestination >= arrets.length || indexDestination < 0) {
        etat.sensAller = !etat.sensAller;
        continue;
      }

      const destination = arrets[indexDestination];

      // Léger bruit GPS (±0.0001°) pour simuler le réalisme
      const bruit = () => (Math.random() - 0.5) * 0.0002;

      // Interpolation pendant 5 secondes vers la destination
      const { lat, lon } = interpoler(
        etat.lat, etat.lon,
        destination.latitude, destination.longitude,
        VITESSE_KMH,
        INTERVALLE_MS / 1000
      );

      etat.lat = lat + bruit();
      etat.lon = lon + bruit();

      const cap     = calculerCap(etat.lat, etat.lon, destination.latitude, destination.longitude);
      const vitesse = VITESSE_KMH + (Math.random() - 0.5) * 10; // ±5 km/h de variabilité
      const eta     = estimerArrivee(etat.lat, etat.lon, destination, vitesse);

      // Si le bus est arrivé à l'arrêt, on avance vers le suivant
      const dist = haversine(etat.lat, etat.lon, destination.latitude, destination.longitude);
      if (dist < DISTANCE_ARRET_M) {
        etat.arretCourantIndex = indexDestination;
      }

      // Persistance en base de données
      try {
        await Bus.updatePosition(busId, etat.lat, etat.lon, vitesse, cap);
      } catch (err) {
        console.error(`Erreur mise en base bus ${busId} :`, err.message);
      }

      positionsMises.push({
        busId,
        latitude:       etat.lat,
        longitude:      etat.lon,
        vitesse:        Math.round(vitesse),
        cap:            Math.round(cap),
        prochainArret:  destination.nom,
        etaMinutes:     eta,
        mis_a_jour:     new Date().toISOString(),
      });
    }

    // Diffusion vers tous les clients connectés
    if (positionsMises.length > 0) {
      io.emit('bus:positions', positionsMises);

      // Événement individuel pour chaque bus mis à jour
      positionsMises.forEach((pos) => {
        io.emit('bus:update', pos);
      });
    }

  }, INTERVALLE_MS);
}

module.exports = { demarrerSimulation };
