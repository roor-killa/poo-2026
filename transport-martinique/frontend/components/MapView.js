"use client";
import React from "react";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MARTINIQUE_CENTER = [14.6415, -61.0242];

const markerIcon = L.icon({
  iconUrl: "/bus-marker.svg",
  iconSize: [30, 30],
  iconAnchor: [12, 24]
});



// MapView now receives stops as a prop
export default function MapView({ onStopSelect, stops, polyline }) {
  let filteredStops = stops || [];
  let shapePoints = Array.isArray(polyline) ? polyline : [];

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <MapContainer center={MARTINIQUE_CENTER} zoom={11} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* Draw the polyline for the selected line */}
        {shapePoints.length > 1 && (
          <Polyline
            positions={shapePoints.map(pt => [pt.lat, pt.lon])}
            pathOptions={{ color: "#0074D9", weight: 5, opacity: 0.7 }}
          />
        )}
        {Array.isArray(filteredStops) && filteredStops.length > 0 ? (
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
              </Marker>
            ))
        ) : null}
      </MapContainer>
    </div>
  );
}
