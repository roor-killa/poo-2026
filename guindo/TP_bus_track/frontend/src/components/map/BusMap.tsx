"use client";
import "leaflet/dist/leaflet.css";
import { useEffect, useRef } from "react";
import type { BusPosition, Ligne } from "@/types";

interface BusMapProps {
  positions: BusPosition[];
  lignes?: Ligne[];
  selectedLigneId?: number | null;
  onBusClick?: (bus: BusPosition) => void;
}

export function BusMap({ positions, lignes, selectedLigneId, onBusClick }: BusMapProps) {
  const mapRef = useRef<any>(null);
  const markersRef = useRef<Map<number, any>>(new Map());
  const ligneLayersRef = useRef<any[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  // Init carte
  useEffect(() => {
    if (typeof window === "undefined" || mapRef.current) return;

    import("leaflet").then((L) => {
      // Guard supplémentaire pour le double-invoke de StrictMode (async)
      if (mapRef.current) return;
      if ((containerRef.current as any)?._leaflet_id) return;

      // Fix icônes Leaflet dans Next.js
      delete (L.Icon.Default.prototype as any)._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
      });

      const map = L.map(containerRef.current!, {
        center: [14.6415, -61.0242], // Centre Martinique
        zoom: 11,
        zoomControl: true,
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(map);

      mapRef.current = { map, L };
    });

    return () => {
      mapRef.current?.map.remove();
      mapRef.current = null;
    };
  }, []);

  // Tracé des lignes
  useEffect(() => {
    if (!mapRef.current || !lignes) return;
    const { map, L } = mapRef.current;

    // Supprimer anciens tracés
    ligneLayersRef.current.forEach((l) => map.removeLayer(l));
    ligneLayersRef.current = [];

    lignes.forEach((ligne) => {
      if (!ligne.arrets || ligne.arrets.length < 2) return;
      const isSelected = selectedLigneId === null || selectedLigneId === undefined || selectedLigneId === ligne.id;
      const coords = ligne.arrets.map((a) => [a.latitude, a.longitude] as [number, number]);
      const poly = L.polyline(coords, {
        color: ligne.couleur,
        weight: isSelected ? 4 : 2,
        opacity: isSelected ? 0.9 : 0.3,
      }).addTo(map);

      // Marqueurs arrêts
      ligne.arrets.forEach((arret) => {
        const circle = L.circleMarker([arret.latitude, arret.longitude], {
          radius: 5,
          color: ligne.couleur,
          fillColor: "#fff",
          fillOpacity: 1,
          weight: 2,
          opacity: isSelected ? 1 : 0.3,
        })
          .bindTooltip(arret.nom, { permanent: false, direction: "top" })
          .addTo(map);
        ligneLayersRef.current.push(circle);
      });

      ligneLayersRef.current.push(poly);
    });
  }, [lignes, selectedLigneId]);

  // Mise à jour des marqueurs bus
  useEffect(() => {
    if (!mapRef.current) return;
    const { map, L } = mapRef.current;

    positions.forEach((bus) => {
      const isVisible = !selectedLigneId || bus.ligne_id === selectedLigneId;
      const existing = markersRef.current.get(bus.id);

      const popupContent = `
        <div style="min-width:180px">
          <div style="font-weight:700;font-size:14px;margin-bottom:4px">🚌 ${bus.nom}</div>
          <div style="font-size:12px;color:${bus.ligne_couleur};margin-bottom:6px">${bus.ligne_nom}</div>
          <div style="font-size:12px"><b>Statut :</b> ${bus.statut.replace("_", " ")}</div>
          ${bus.arret_courant ? `<div style="font-size:12px"><b>Arrêt :</b> ${bus.arret_courant}</div>` : ""}
          ${bus.prochain_arret ? `<div style="font-size:12px"><b>Prochain :</b> ${bus.prochain_arret}</div>` : ""}
          <div style="font-size:12px"><b>Vitesse :</b> ${bus.vitesse} km/h</div>
        </div>
      `;

      if (existing) {
        existing.setLatLng([bus.latitude, bus.longitude]);
        existing.setOpacity(isVisible ? 1 : 0);
        existing.getPopup()?.setContent(popupContent);
        if (onBusClick) {
          existing.off("click").on("click", () => onBusClick(bus));
        }
      } else {
        const icon = L.divIcon({
          className: "bus-marker",
          html: `<div class="bus-marker" style="background:${bus.ligne_couleur}">🚌</div>`,
          iconSize: [36, 36],
          iconAnchor: [18, 18],
        });

        const marker = L.marker([bus.latitude, bus.longitude], { icon })
          .bindPopup(popupContent)
          .addTo(map);

        if (onBusClick) {
          marker.on("click", () => onBusClick(bus));
        }

        markersRef.current.set(bus.id, marker);
      }
    });
  }, [positions, selectedLigneId, onBusClick]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full rounded-xl overflow-hidden"
      style={{ minHeight: "500px" }}
    />
  );
}
