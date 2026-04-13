/**
 * components/Map.jsx
 *
 * Composant principal de la carte Leaflet.
 * Affiche :
 *  – Les polylignes des itinéraires
 *  – Les marqueurs d'arrêts
 *  – Les marqueurs de bus (mis à jour en temps réel)
 */

import React from 'react';
import { MapContainer, TileLayer, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

import BusMarker      from './BusMarker';
import StopMarker     from './StopMarker';
import LignePolyline  from './LignePolyline';

// Centre de la Martinique
const CENTRE_MARTINIQUE = [14.641528, -61.024174];
const ZOOM_INITIAL      = 12;

/**
 * @param {{
 *   bus:       Array,         - Liste des bus (données BDD)
 *   arrets:    Array,         - Liste des arrêts
 *   lignes:    Array,         - Liste des lignes avec leurs arrêts
 *   positions: Map,           - Map busId → position WebSocket
 * }} props
 */
function Map({ bus, arrets, lignes, positions }) {
  return (
    <MapContainer
      center={CENTRE_MARTINIQUE}
      zoom={ZOOM_INITIAL}
      zoomControl={false}
      style={{ height: '100%', width: '100%' }}
    >
      {/* Fond de carte OpenStreetMap */}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        maxZoom={19}
      />

      <ZoomControl position="bottomright" />

      {/* Itinéraires des lignes */}
      {lignes.map((ligne) => (
        <LignePolyline key={ligne.id} ligne={ligne} />
      ))}

      {/* Arrêts */}
      {arrets.map((arret) => (
        <StopMarker key={arret.id} arret={arret} />
      ))}

      {/* Bus en temps réel */}
      {bus.map((b) => (
        <BusMarker
          key={b.id}
          bus={b}
          position={positions.get(b.id)}
        />
      ))}
    </MapContainer>
  );
}

export default Map;
