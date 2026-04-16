"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";

const MapView = dynamic(() => import("../components/MapView"), {
  ssr: false,
  loading: () => <p className="map-loading">Chargement de la carte...</p>
});

export default function HomePage() {
  const [search, setSearch] = useState("");
  const [direction, setDirection] = useState("");

  const filters = useMemo(
    () => ({ search: search.trim(), direction: direction.trim() }),
    [search, direction]
  );

  return (
    <main className="page-shell">
      <header className="top-panel">
        <div className="title-wrap">
          <h1>Transport Martinique</h1>
          <p>Carte interactive des arrets et lignes</p>
        </div>

        <div className="search-grid">
          <label className="field">
            <span>Recherche arret / ligne</span>
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Ex: Savane, M1, TCSP"
            />
          </label>

          <label className="field">
            <span>Direction</span>
            <input
              value={direction}
              onChange={(event) => setDirection(event.target.value)}
              placeholder="Ex: Fort-de-France -> Le Lamentin"
            />
          </label>
        </div>
      </header>

      <section className="map-card">
        <MapView filters={filters} />
      </section>
    </main>
  );
}
