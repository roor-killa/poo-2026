/**
 * components/StopMarker.jsx
 *
 * Marqueur Leaflet représentant un arrêt de bus.
 * Icône petit cercle bleu avec popup du nom.
 */

import React from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Icône SVG pour un arrêt de bus
const iconeArret = L.divIcon({
  html: `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="6" fill="white" stroke="#3388ff" stroke-width="2.5"/>
      <circle cx="8" cy="8" r="2" fill="#3388ff"/>
    </svg>
  `,
  className: '',
  iconSize:   [16, 16],
  iconAnchor: [8, 8],
  popupAnchor:[0, -12],
});

/**
 * @param {{ arret: Object }} props
 */
function StopMarker({ arret }) {
  return (
    <Marker position={[arret.latitude, arret.longitude]} icon={iconeArret}>
      <Popup>
        <div>
          <strong>🚏 {arret.nom}</strong>
          {arret.description && (
            <p style={{ margin: '4px 0 0', fontSize: '0.85em', color: '#555' }}>
              {arret.description}
            </p>
          )}
        </div>
      </Popup>
    </Marker>
  );
}

export default StopMarker;
