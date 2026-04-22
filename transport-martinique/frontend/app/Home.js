"use client";
import dynamic from "next/dynamic";
import React from "react";
const MapView = dynamic(() => import("../components/MapView"), { ssr: false });

export default function Home() {
  const [selectedStop, setSelectedStop] = React.useState(null);
  return (
    <main className="w-screen h-screen flex flex-row min-h-0 min-w-0 p-0 m-0 overflow-hidden">
      <aside className="bg-white dark:bg-zinc-900 shadow-lg w-80 max-w-xs h-full p-4 overflow-y-auto z-10">
        <h2 className="text-lg font-bold mb-2">Arrêt sélectionné</h2>
        {selectedStop ? (
          <div>
            <div className="font-semibold text-xl mb-1">{selectedStop.stop_name}</div>
            <div className="text-sm text-zinc-500 mb-2">Code: {selectedStop.stop_code}</div>
            <div className="text-sm">Latitude: {selectedStop.stop_lat}</div>
            <div className="text-sm">Longitude: {selectedStop.stop_lon}</div>
            {/* Add more stop info here if needed */}
          </div>
        ) : (
          <div className="text-zinc-400">Cliquez sur un arrêt pour voir les détails.</div>
        )}
      </aside>
      <div className="flex-1 h-full">
        <MapView onStopSelect={setSelectedStop} />
      </div>
    </main>
  );
}