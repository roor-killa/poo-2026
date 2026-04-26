"use client";



import dynamic from "next/dynamic";
import React from "react";
const MapView = dynamic(() => import("../components/MapView"), { ssr: false });


export default function Home() {
  const [selectedStop, setSelectedStop] = React.useState(null);
  const [search, setSearch] = React.useState("");
  const [lines, setLines] = React.useState([]);
  const [filteredLines, setFilteredLines] = React.useState([]);
  const [selectedLine, setSelectedLine] = React.useState(null);
  const [stops, setStops] = React.useState([]);
  const [polyline, setPolyline] = React.useState([]);
  const [buses, setBuses] = React.useState([]);

  // Fetch all lines on mount
  React.useEffect(() => {
    fetch("http://localhost:8000/api/lignes")
      .then(res => res.json())
      .then(data => {
        setLines(data);
        setFilteredLines(data);
      });
  }, []);

  // Filter lines by search
  React.useEffect(() => {
    if (!search) {
      setFilteredLines(lines);
      return;
    }
    const s = search.trim().toLowerCase();
    setFilteredLines(
      lines.filter(line =>
        (line.route_short_name && line.route_short_name.toLowerCase().includes(s)) ||
        (line.route_long_name && line.route_long_name.toLowerCase().includes(s))
      )
    );
  }, [search, lines]);


  // Fetch stops and polyline for selected line
  React.useEffect(() => {
    if (!selectedLine) return;
    fetch(`http://localhost:8000/api/lignes/${selectedLine.route_id}/stops`)
      .then(res => res.json())
      .then(data => setStops(data));
    fetch(`http://localhost:8000/api/lignes/${selectedLine.route_id}/shape`)
      .then(res => res.json())
      .then(data => setPolyline(data));
  }, [selectedLine]);

  // Fetch simulated buses for selected line, poll every 5 seconds
  React.useEffect(() => {
    if (!selectedLine) {
      setBuses([]);
      return;
    }
    let isMounted = true;
    const fetchBuses = () => {
      fetch(`http://localhost:8000/api/lignes/${selectedLine.route_id}/buses`)
        .then(res => res.json())
        .then(data => { if (isMounted) setBuses(Array.isArray(data) ? data : []); });
    };
    fetchBuses();
    const interval = setInterval(fetchBuses, 5000);
    return () => { isMounted = false; clearInterval(interval); };
  }, [selectedLine]);

  return (
    <main className="w-screen h-screen flex flex-row min-h-0 min-w-0 p-0 m-0 overflow-hidden">
      <aside className="bg-white dark:bg-zinc-900 shadow-lg w-80 max-w-xs h-full p-4 overflow-y-auto z-10">
        <h1>Transport Martinique</h1>

        <div className="w-full p-4 bg-white/80 z-20 flex flex-col gap-2 shadow-md">
          <input
            type="text"
            className="border rounded px-3 py-2 w-full max-w-md"
            placeholder="Rechercher une ligne (numéro ou nom)..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{fontSize:'1rem'}}
          />
          <div className="max-h-48 overflow-y-auto mt-2">
            {filteredLines && filteredLines.length > 0 ? (
              filteredLines.slice(0, 20).map(line => (
                <div
                  key={line.route_id}
                  className={`cursor-pointer px-2 py-1 rounded hover:bg-blue-100 dark:hover:bg-zinc-800 ${selectedLine && selectedLine.route_id === line.route_id ? 'bg-blue-200 dark:bg-zinc-700' : ''}`}
                  onClick={() => { setSelectedLine(line); setSelectedStop(null); }}
                >
                  <span className="font-bold">{line.route_short_name}</span> <span className="text-xs text-zinc-500">{line.route_long_name}</span>
                </div>
              ))
            ) : (
              <div className="text-zinc-500 text-sm">Aucune ligne trouvée</div>
            )}
          </div>
        </div>

        {selectedLine && (
          <div className="mt-4">
            <h2 className="text-lg font-bold mb-2">Ligne sélectionnée</h2>
            <div className="font-semibold text-xl mb-1">{selectedLine.route_short_name}</div>
            <div className="text-sm text-zinc-500 mb-2">{selectedLine.route_long_name}</div>
          </div>
        )}

        {selectedStop ? (
          <div className="mt-4">
            <h2 className="text-lg font-bold mb-2">Arrêt sélectionné</h2>
            <div className="font-semibold text-xl mb-1">{selectedStop.stop_name}</div>
            <div className="text-sm text-zinc-500 mb-2">Code: {selectedStop.stop_code}</div>
            <div className="text-sm">Latitude: {selectedStop.stop_lat}</div>
            <div className="text-sm">Longitude: {selectedStop.stop_lon}</div>
          </div>
        ) : null}
      </aside>
      <div className="flex-1 h-full flex flex-col">
        <MapView onStopSelect={setSelectedStop} stops={stops} polyline={polyline} buses={buses} />
      </div>
    </main>
  );
}