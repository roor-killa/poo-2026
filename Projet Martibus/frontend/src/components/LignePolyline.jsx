/**
 * components/LignePolyline.jsx
 *
 * Trace le parcours d'une ligne de bus sous forme de polyligne colorée.
 */

import React from 'react';
import { Polyline, Tooltip } from 'react-leaflet';

/**
 * @param {{
 *   ligne: Object,  - Objet ligne avec { nom, couleur, arrets[] }
 * }} props
 */
function LignePolyline({ ligne }) {
  if (!ligne.arrets || ligne.arrets.length < 2) return null;

  // Tableau de paires [lat, lon] pour react-leaflet
  const points = ligne.arrets.map((a) => [a.latitude, a.longitude]);

  return (
    <Polyline
      positions={points}
      pathOptions={{
        color:     ligne.couleur || '#3388ff',
        weight:    4,
        opacity:   0.75,
        dashArray: null,
      }}
    >
      <Tooltip sticky>{ligne.nom}</Tooltip>
    </Polyline>
  );
}

export default LignePolyline;
