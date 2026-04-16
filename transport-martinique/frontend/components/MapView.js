"use client";

import { useEffect, useMemo, useState } from "react";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { fetchSearch } from "../lib/api";

const MARTINIQUE_CENTER = [14.6415, -61.0242];

const markerIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34]
});

function FocusController({ stop }) {
  const map = useMap();

  useEffect(() => {
    if (!stop) {
      return;
    }
    map.flyTo([stop.lat, stop.lng], 14, { duration: 0.8 });
  }, [map, stop]);

  return null;
}

export default function MapView({ filters }) {
  const [stops, setStops] = useState([]);
  const [lines, setLines] = useState([]);
  const [selectedStopId, setSelectedStopId] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError("");
        const response = await fetchSearch(filters.search, filters.direction);
        if (cancelled) {
          return;
        }
        setStops(response.stops || []);
        setLines(response.lines || []);
      } catch (fetchError) {
        if (!cancelled) {
          setError("Impossible de charger les donnees de transport.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadData();
    return () => {
      cancelled = true;
    };
  }, [filters.direction, filters.search]);

  const selectedStop = useMemo(
    () => stops.find((stop) => stop.id === selectedStopId),
    [selectedStopId, stops]
  );

  if (error) {
    return <p className="map-error">{error}</p>;
  }

  if (loading) {
    return <p className="map-loading">Chargement des arrets et lignes...</p>;
  }

  return (
    <div className="map-wrap">
      <MapContainer center={MARTINIQUE_CENTER} zoom={11} scrollWheelZoom>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <FocusController stop={selectedStop} />

        {stops.map((stop) => (
          <Marker
            key={stop.id}
            position={[stop.lat, stop.lng]}
            icon={markerIcon}
            eventHandlers={{ click: () => setSelectedStopId(stop.id) }}
          >
            <Popup>
              <strong>{stop.name}</strong>
              <p>Prochain passage estime: {stop.next_eta_min} min</p>
              <div>
                {(stop.lines || []).map((line) => (
                  <p key={line.id} style={{ margin: "4px 0" }}>
                    <span className="badge">{line.code}</span>
                    {line.name} - {line.direction}
                  </p>
                ))}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {(filters.search || filters.direction) && (
        <aside className="results-overlay">
          {stops.length === 0 ? (
            <p className="map-empty">Aucun arret ou ligne correspondant.</p>
          ) : (
            <ul className="results-list">
              {stops.slice(0, 12).map((stop) => (
                <li key={stop.id}>
                  <button type="button" onClick={() => setSelectedStopId(stop.id)}>
                    <strong>{stop.name}</strong>
                    <br />
                    <small>
                      {stop.lines.map((line) => `${line.code} (${line.direction})`).join(" | ")}
                    </small>
                  </button>
                </li>
              ))}
            </ul>
          )}
          {lines.length > 0 && (
            <ul className="results-list">
              {lines.slice(0, 6).map((line) => (
                <li key={line.id}>
                  <button type="button">
                    <span className="badge">{line.code}</span>
                    {line.name} - {line.direction}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </aside>
      )}
    </div>
  );
}
