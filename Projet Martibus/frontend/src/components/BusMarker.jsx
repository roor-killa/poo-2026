/**
 * components/BusMarker.jsx
 *
 * Marqueur Leaflet représentant un bus sur la carte.
 * Affiche un icône SVG coloré selon la ligne, avec une popup détaillée.
 */

import React from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

/**
 * Génère une icône SVG de bus avec la couleur de la ligne.
 * @param {string} couleur - Couleur HEX de la ligne
 * @param {number} cap     - Orientation du bus en degrés
 */
function creerIconeBus(couleur = '#e63946', cap = 0) {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <circle cx="16" cy="16" r="14" fill="${couleur}" stroke="white" stroke-width="2"/>
      <text x="16" y="21" text-anchor="middle" font-size="16" fill="white">🚌</text>
    </svg>
  `;
  return L.divIcon({
    html: `<div style="transform: rotate(${cap}deg)">${svg}</div>`,
    className: '',
    iconSize:   [32, 32],
    iconAnchor: [16, 16],
    popupAnchor:[0, -20],
  });
}

/**
 * @param {{
 *   bus: Object,        - Données statiques du bus (BDD)
 *   position: Object,   - Données en temps réel (WebSocket)
 * }} props
 */
function BusMarker({ bus, position }) {
  // Utilise la position WebSocket si disponible, sinon la position BDD
  const lat = position?.latitude  ?? bus.latitude;
  const lon = position?.longitude ?? bus.longitude;

  if (!lat || !lon) return null;

  const couleur  = bus.ligne_couleur || '#3388ff';
  const cap      = position?.cap     ?? bus.cap ?? 0;
  const vitesse  = position?.vitesse ?? bus.vitesse ?? 0;
  const eta      = position?.etaMinutes;
  const prochain = position?.prochainArret ?? bus.dernier_arret_nom ?? '—';

  return (
    <Marker
      position={[lat, lon]}
      icon={creerIconeBus(couleur, cap)}
    >
      <Popup>
        <div style={{ minWidth: 180 }}>
          <strong style={{ color: couleur, fontSize: '1.05em' }}>
            🚌 Bus {bus.immatriculation}
          </strong>
          <hr style={{ margin: '4px 0' }} />
          <table style={{ fontSize: '0.9em', borderCollapse: 'collapse' }}>
            <tbody>
              <tr>
                <td style={{ paddingRight: 8, color: '#666' }}>Ligne</td>
                <td>
                  <span
                    style={{
                      background: couleur,
                      color: 'white',
                      padding: '1px 6px',
                      borderRadius: 4,
                      fontSize: '0.85em',
                    }}
                  >
                    {bus.ligne_nom || '—'}
                  </span>
                </td>
              </tr>
              <tr>
                <td style={{ color: '#666' }}>Vitesse</td>
                <td>{vitesse} km/h</td>
              </tr>
              <tr>
                <td style={{ color: '#666' }}>Cap</td>
                <td>{Math.round(cap)}°</td>
              </tr>
              <tr>
                <td style={{ color: '#666' }}>Prochain arrêt</td>
                <td>{prochain}</td>
              </tr>
              {eta !== undefined && (
                <tr>
                  <td style={{ color: '#666' }}>Arrivée dans</td>
                  <td>
                    <strong style={{ color: '#2a9d8f' }}>
                      {eta === 0 ? 'À quai' : `~${eta} min`}
                    </strong>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          <div style={{ marginTop: 6, fontSize: '0.75em', color: '#999' }}>
            Mis à jour : {position?.mis_a_jour
              ? new Date(position.mis_a_jour).toLocaleTimeString('fr-FR')
              : '—'}
          </div>
        </div>
      </Popup>
    </Marker>
  );
}

export default BusMarker;
