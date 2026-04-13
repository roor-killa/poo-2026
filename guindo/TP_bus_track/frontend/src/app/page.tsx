"use client";
import dynamic from "next/dynamic";
import { useState, useEffect } from "react";
import { useBus } from "@/context/BusContext";
import { Sidebar } from "@/components/map/Sidebar";
import { api } from "@/lib/api";
import type { Ligne, BusPosition } from "@/types";

// Import dynamique pour éviter le SSR (Leaflet nécessite window)
const BusMap = dynamic(
  () => import("@/components/map/BusMap").then((m) => m.BusMap),
  { ssr: false, loading: () => <div className="w-full h-full bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl" /> }
);

export default function HomePage() {
  const { positions, connected, error } = useBus();
  const [lignes, setLignes] = useState<Ligne[]>([]);
  const [selectedLigneId, setSelectedLigneId] = useState<number | null>(null);
  const [selectedBus, setSelectedBus] = useState<BusPosition | null>(null);

  useEffect(() => {
    api.getLignes().then(setLignes).catch(console.error);
  }, []);

  return (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Panneau latéral */}
      <Sidebar
        lignes={lignes}
        positions={positions}
        selectedLigneId={selectedLigneId}
        onSelectLigne={setSelectedLigneId}
        onSelectBus={setSelectedBus}
      />

      {/* Zone carte */}
      <div className="flex-1 relative p-4">
        {/* Bandeau erreur */}
        {error && (
          <div className="absolute top-6 left-1/2 -translate-x-1/2 z-10 bg-red-500 text-white text-sm px-4 py-2 rounded-full shadow-lg">
            ⚠️ {error} — reconnexion en cours…
          </div>
        )}

        {/* Carte */}
        <div className="w-full h-full rounded-xl overflow-hidden shadow-lg border border-gray-200 dark:border-gray-700">
          <BusMap
            positions={positions}
            lignes={lignes}
            selectedLigneId={selectedLigneId}
            onBusClick={setSelectedBus}
          />
        </div>

        {/* Compteur positions */}
        <div className="absolute bottom-8 right-8 bg-white dark:bg-gray-900 rounded-xl shadow-lg px-4 py-2 text-sm border border-gray-200 dark:border-gray-700">
          <span className="font-semibold text-brand-500">{positions.length}</span>
          <span className="text-gray-500 dark:text-gray-400"> bus en circulation</span>
        </div>
      </div>

      {/* Panneau détail bus (slide-in) */}
      {selectedBus && (
        <div className="absolute bottom-8 left-96 z-20 bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 p-5 w-72">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-bold text-base">🚌 {selectedBus.nom}</h3>
            <button
              onClick={() => setSelectedBus(null)}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none"
            >×</button>
          </div>
          <div className="text-sm font-medium mb-3" style={{ color: selectedBus.ligne_couleur }}>
            {selectedBus.ligne_nom}
          </div>
          <div className="space-y-1.5 text-sm text-gray-600 dark:text-gray-400">
            <div><span className="font-medium">Latitude :</span> {selectedBus.latitude.toFixed(5)}</div>
            <div><span className="font-medium">Longitude :</span> {selectedBus.longitude.toFixed(5)}</div>
            <div><span className="font-medium">Vitesse :</span> {selectedBus.vitesse} km/h</div>
            {selectedBus.arret_courant && (
              <div><span className="font-medium">Arrêt :</span> {selectedBus.arret_courant}</div>
            )}
            {selectedBus.prochain_arret && (
              <div><span className="font-medium">Prochain :</span> {selectedBus.prochain_arret}</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
