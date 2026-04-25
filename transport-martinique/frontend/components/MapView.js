"use client";
import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MARTINIQUE_CENTER = [14.6415, -61.0242];

const markerIcon = L.icon({
  iconUrl: "/bus-marker.svg",
  iconSize: [24, 24],
  iconAnchor: [12, 24],
  popupAnchor: [0, -20],
});



export default function MapView({ onStopSelect, search }) {
  const [stops, setStops] = React.useState([]);
  const [zoom, setZoom] = React.useState(11);
  React.useEffect(() => {
    fetch("http://localhost:8000/api/stops")
      .then(res => res.json())
      .then(data => {
        // Handle both array and {items: array} response
        const stopsArray = Array.isArray(data) ? data : (Array.isArray(data.items) ? data.items : []);
        setStops(stopsArray);
      });
  }, []);

  // Filter stops by search
  let filteredStops = stops;
  if (search && search.trim().length > 0) {
    const s = search.trim().toLowerCase();
    filteredStops = stops.filter(stop => {
      const name = (stop.stop_name || stop.name || "").toLowerCase();
      const code = (stop.stop_code || stop.code || "").toLowerCase();
      return name.includes(s) || code.includes(s);
    });
  }

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <MapContainer center={MARTINIQUE_CENTER} zoom={11} style={{ height: "100%", width: "100%" }}
        whenCreated={map => {
          map.on('zoomend', () => setZoom(map.getZoom()));
        }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {zoom >= 14 && Array.isArray(filteredStops) && filteredStops.length > 0 ? (
          filteredStops
            .filter(stop => {
              const lat = parseFloat(stop.stop_lat || stop.lat);
              const lon = parseFloat(stop.stop_lon || stop.lon);
              return !isNaN(lat) && !isNaN(lon);
            })
            .slice(0, 1000)
            .map(stop => (
              <Marker
                key={stop.stop_id || stop.id}
                position={[parseFloat(stop.stop_lat || stop.lat), parseFloat(stop.stop_lon || stop.lon)]}
                icon={markerIcon}
                eventHandlers={onStopSelect ? { click: () => onStopSelect(stop) } : {}}
              >
                <Popup>
                  <strong>{stop.stop_name || stop.name}</strong>
                  <br />Code: {stop.stop_code || stop.code}
                </Popup>
              </Marker>
            ))
        ) : zoom < 14 ? (
          <div style={{position:'absolute',top:10,left:10,background:'#fff',padding:8,borderRadius:8,boxShadow:'0 2px 8px #0002'}}>Zoomez pour voir les arrêts</div>
        ) : filteredStops && typeof filteredStops === 'object' && filteredStops.length === 0 && search && search.trim().length > 0 ? (
          <div style={{color: 'orange', padding: 8, position:'absolute',top:10,left:10,background:'#fff',borderRadius:8,boxShadow:'0 2px 8px #0002'}}>Aucun arrêt trouvé pour "{search}"</div>
        ) : stops && typeof stops === 'object' ? (
          <div style={{color: 'red', padding: 8}}>Erreur de chargement des arrêts</div>
        ) : null}
      </MapContainer>
    </div>
  );
}
