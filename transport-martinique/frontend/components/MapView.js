"use client";
import React from "react";
import { MapContainer, TileLayer, Marker, Polyline, Tooltip } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MARTINIQUE_CENTER = [14.6415, -61.0242];

// Distinct icon for bus stops (blue circle)
const stopIcon = L.divIcon({
  className: "",
  html: `<div style="
    width: 10px; height: 10px;
    background: #0074D9;
    border: 2px solid white;
    border-radius: 50%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
  "></div>`,
  iconSize: [10, 10],
  iconAnchor: [5, 5],
});

// Distinct icon for buses (animated yellow square with emoji)
const busIcon = L.divIcon({
  className: "",
  html: `<div style="
    width: 28px; height: 28px;
    background: #FFDC00;
    border: 2px solid #333;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  ">🚌</div>`,
  iconSize: [28, 28],
  iconAnchor: [14, 14],
});

export default function MapView({ onStopSelect, stops, polyline, buses }) {
  const filteredStops = (stops || []).filter(stop => {
    const lat = parseFloat(stop.stop_lat || stop.lat);
    const lon = parseFloat(stop.stop_lon || stop.lon);
    return !isNaN(lat) && !isNaN(lon);
  });

  const shapePoints = Array.isArray(polyline) ? polyline : [];

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <MapContainer center={MARTINIQUE_CENTER} zoom={11} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Route polyline */}
        {shapePoints.length > 1 && (
          <Polyline
            positions={shapePoints.map(pt => [pt.lat, pt.lon])}
            pathOptions={{ color: "#0074D9", weight: 5, opacity: 0.7 }}
          />
        )}

        {/* Bus markers */}
        {Array.isArray(buses) && buses.map(bus => (
          <Marker
            key={bus.bus_id}
            position={[bus.lat, bus.lon]}
            icon={busIcon}
          >
            <Tooltip permanent={false} direction="top" offset={[0, -14]}>
              {bus.bus_id}
            </Tooltip>
          </Marker>
        ))}

        {/* Stop markers */}
        {filteredStops.slice(0, 1000).map(stop => (
          <Marker
            key={stop.stop_id || stop.id}
            position={[
              parseFloat(stop.stop_lat || stop.lat),
              parseFloat(stop.stop_lon || stop.lon),
            ]}
            icon={stopIcon}
            eventHandlers={onStopSelect ? { click: () => onStopSelect(stop) } : {}}
          >
            <Tooltip direction="top" offset={[0, -6]}>
              {stop.stop_name || stop.stop_id}
            </Tooltip>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}