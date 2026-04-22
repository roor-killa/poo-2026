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



export default function MapView({ onStopSelect }) {
  const [stops, setStops] = React.useState([]);
  React.useEffect(() => {
    fetch("http://localhost:8000/api/stops")
      .then(res => res.json())
      .then(data => {
        // Handle both array and {items: array} response
        const stopsArray = Array.isArray(data) ? data : (Array.isArray(data.items) ? data.items : []);
        console.log("Fetched stops from backend:", stopsArray.length);
        setStops(stopsArray);
      });
  }, []);
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <MapContainer center={MARTINIQUE_CENTER} zoom={11} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {Array.isArray(stops) && stops.length > 0 ? (
          stops
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
        ) : stops && typeof stops === 'object' ? (
          <div style={{color: 'red', padding: 8}}>Erreur de chargement des arrêts</div>
        ) : null}
      </MapContainer>
    </div>
  );
}
