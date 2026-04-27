"use client";
import React, { useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Polyline, Tooltip, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const MARTINIQUE_CENTER = [14.6415, -61.0242];

// ── Programmatic map controller ───────────────────────────────────────────────

function MapController({ center, bounds }) {
  const map = useMap();
  useEffect(() => {
    if (bounds && bounds.length > 1) {
      map.fitBounds(L.latLngBounds(bounds), { padding: [60, 60], maxZoom: 15, animate: true });
    } else if (center) {
      map.setView(center, 16, { animate: true });
    }
  }, [center, bounds]);
  return null;
}

// ── Main component ────────────────────────────────────────────────────────────

export default function MapView({ stops, polyline, buses, selectedStop, onStopSelect, mapCenter, mapBounds }) {
  const shapePoints = Array.isArray(polyline) ? polyline : [];

  // Icons created inside the component so L is only called client-side,
  // after Leaflet has fully initialised. useMemo prevents re-creating on every render.
  const icons = useMemo(() => ({
    stop: L.divIcon({
      className: "",
      html: `<div style="width:11px;height:11px;background:#0074D9;border:2.5px solid white;border-radius:50%;box-shadow:0 1px 4px rgba(0,0,0,0.35)"></div>`,
      iconSize: [11, 11],
      iconAnchor: [5, 5],
    }),
    selectedStop: L.divIcon({
      className: "",
      html: `<div style="width:18px;height:18px;background:#e74c3c;border:3px solid white;border-radius:50%;box-shadow:0 2px 8px rgba(231,76,60,0.55)"></div>`,
      iconSize: [18, 18],
      iconAnchor: [9, 9],
    }),
    bus: L.divIcon({
      className: "",
      html: `<div style="width:30px;height:30px;background:#FFDC00;border:2.5px solid #333;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:17px;box-shadow:0 2px 8px rgba(0,0,0,0.3)">🚌</div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 15],
    }),
  }), []);

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <style>{`
        .leaflet-top.leaflet-right { top: 80px; }
        .leaflet-control-zoom a { width: 36px; height: 36px; line-height: 36px; font-size: 18px; }
      `}</style>
      <MapContainer
        center={MARTINIQUE_CENTER}
        zoom={11}
        style={{ height: "100%", width: "100%" }}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapController center={mapCenter} bounds={mapBounds} />

        {/* Route polyline */}
        {shapePoints.length > 1 && (
          <Polyline
            positions={shapePoints.map(pt => [pt.lat, pt.lon])}
            pathOptions={{ color: "#0074D9", weight: 5, opacity: 0.75 }}
          />
        )}

        {/* Stop markers */}
        {Array.isArray(stops) && stops
          .filter(s => !isNaN(parseFloat(s.stop_lat)) && !isNaN(parseFloat(s.stop_lon)))
          .map(stop => {
            const isSelected = selectedStop?.stop_id === stop.stop_id;
            return (
              <Marker
                key={stop.stop_id}
                position={[parseFloat(stop.stop_lat), parseFloat(stop.stop_lon)]}
                icon={isSelected ? icons.selectedStop : icons.stop}
                zIndexOffset={isSelected ? 500 : 0}
                eventHandlers={{ click: () => onStopSelect?.(stop) }}
              >
                <Tooltip direction="top" offset={[0, -8]}>{stop.stop_name}</Tooltip>
              </Marker>
            );
          })}

        {/* Bus markers */}
        {Array.isArray(buses) && buses.map(bus => (
          <Marker
            key={bus.bus_id}
            position={[bus.lat, bus.lon]}
            icon={icons.bus}
            zIndexOffset={1000}
          >
            <Tooltip direction="top" offset={[0, -16]}>{bus.bus_id}</Tooltip>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}