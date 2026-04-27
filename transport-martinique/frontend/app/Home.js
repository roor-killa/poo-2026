"use client";
import dynamic from "next/dynamic";
import React, { useState, useEffect, useRef } from "react";

const MapView = dynamic(() => import("../components/MapView"), { ssr: false });

const API = "/api";

// ─────────────────────────────────────────────────────────────────────────────
// Mobile detection hook
// ─────────────────────────────────────────────────────────────────────────────

function useMobile() {
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 640);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);
  return isMobile;
}

// ─────────────────────────────────────────────────────────────────────────────
// Shared primitives
// ─────────────────────────────────────────────────────────────────────────────

function LineBadge({ name, color, textColor }) {
  return (
    <span style={{
      background: color ? `#${color}` : "#0074D9",
      color: textColor ? `#${textColor}` : "white",
      borderRadius: 6, padding: "3px 10px", fontWeight: 700, fontSize: 13,
      minWidth: 36, textAlign: "center", display: "inline-block", flexShrink: 0,
    }}>
      {name}
    </span>
  );
}

function PanelHeader({ children, onClose }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", padding: "14px 16px",
      borderBottom: "1px solid #eee", background: "#fafafa", flexShrink: 0,
    }}>
      <div style={{ display: "flex", alignItems: "center", flex: 1, minWidth: 0 }}>{children}</div>
      <button onClick={onClose} style={{
        marginLeft: 8, background: "#eee", border: "none", borderRadius: "50%",
        width: 36, height: 36, cursor: "pointer", fontSize: 18, color: "#555",
        display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
        touchAction: "manipulation",
      }}>×</button>
    </div>
  );
}

function SectionLabel({ children }) {
  return (
    <div style={{
      padding: "8px 16px 4px", fontSize: 11, fontWeight: 700,
      color: "#999", textTransform: "uppercase", letterSpacing: "0.08em",
    }}>{children}</div>
  );
}

function Muted({ children }) {
  return <div style={{ padding: "14px 16px", color: "#aaa", fontSize: 13 }}>{children}</div>;
}

// ─────────────────────────────────────────────────────────────────────────────
// SearchBar
// ─────────────────────────────────────────────────────────────────────────────

// allLines and allStops are loaded once by the parent — no API calls on keystrokes
function SearchBar({ onSelectStop, onSelectLine, allLines = [], allStops = [] }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const containerRef = useRef(null);
  const isMobile = useMobile();

  useEffect(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) { setResults(null); return; }

    const lines = allLines.filter(r =>
      r.route_short_name?.toLowerCase().includes(q) ||
      r.route_long_name?.toLowerCase().includes(q)
    ).slice(0, 8).map(r => ({ ...r, type: "line" }));

    const stops = allStops.filter(s =>
      s.stop_name?.toLowerCase().includes(q)
    ).slice(0, 12).map(s => ({ ...s, type: "stop" }));

    setResults({ lines, stops });
  }, [query, allLines, allStops]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) setResults(null);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const select = (item) => {
    setQuery(""); setResults(null);
    if (item.type === "stop") onSelectStop(item);
    else onSelectLine(item);
  };

  const hasResults = results && (results.lines?.length > 0 || results.stops?.length > 0);

  return (
    <div ref={containerRef} style={{
      position: "absolute",
      top: isMobile ? 12 : 16,
      left: isMobile ? 12 : "50%",
      right: isMobile ? 12 : "auto",
      transform: isMobile ? "none" : "translateX(-50%)",
      zIndex: 1000,
      width: isMobile ? "auto" : 430,
      maxWidth: isMobile ? "none" : "90vw",
      fontFamily: "system-ui, sans-serif",
    }}>
      {/* Input */}
      <div style={{ position: "relative" }}>
        <span style={{
          position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)",
          fontSize: 18, pointerEvents: "none",
        }}>🔍</span>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Rechercher un arrêt ou une ligne..."
          style={{
            width: "100%", padding: "13px 40px 13px 42px", fontSize: 15,
            borderRadius: hasResults ? "12px 12px 0 0" : 12, border: "none",
            boxShadow: "0 4px 24px rgba(0,0,0,0.22)", outline: "none",
            boxSizing: "border-box", background: "white",
          }}
        />
        {query && (
          <button onClick={() => { setQuery(""); setResults(null); }} style={{
            position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)",
            background: "none", border: "none", cursor: "pointer", fontSize: 18, color: "#aaa", padding: 0,
          }}>×</button>
        )}
      </div>

      {/* Dropdown */}
      {results && (
        <div style={{
          background: "white", borderRadius: "0 0 12px 12px",
          boxShadow: "0 8px 24px rgba(0,0,0,0.18)", maxHeight: 420, overflowY: "auto",
        }}>
          {!hasResults && (
            <div style={{ padding: "14px 16px", color: "#999", fontSize: 14 }}>
              Aucun résultat pour « {query} »
            </div>
          )}

          {results.lines?.length > 0 && (
            <>
              <div style={{ padding: "8px 16px 4px", fontSize: 11, fontWeight: 700, color: "#999", textTransform: "uppercase", letterSpacing: "0.08em", background: "#fafafa", borderTop: "1px solid #f0f0f0" }}>Lignes</div>
              {results.lines.map(line => (
                <DropdownRow key={line.route_id} onClick={() => select(line)}
                  left={<LineBadge name={line.route_short_name || line.route_id} color={line.route_color} textColor={line.route_text_color} />}
                  primary={line.route_long_name || line.route_short_name}
                />
              ))}
            </>
          )}

          {results.stops?.length > 0 && (
            <>
              <div style={{ padding: "8px 16px 4px", fontSize: 11, fontWeight: 700, color: "#999", textTransform: "uppercase", letterSpacing: "0.08em", background: "#fafafa", borderTop: "1px solid #f0f0f0" }}>Arrêts</div>
              {results.stops.map(stop => (
                <DropdownRow key={stop.stop_id} onClick={() => select(stop)}
                  left={<span style={{ fontSize: 20 }}>🚏</span>}
                  primary={stop.stop_name}
                />
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}

function DropdownRow({ onClick, left, primary }) {
  const [hover, setHover] = useState(false);
  return (
    <div onClick={onClick}
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        padding: "10px 16px", cursor: "pointer", display: "flex", alignItems: "center",
        gap: 12, background: hover ? "#f4f7ff" : "white", transition: "background 0.1s",
      }}>
      <div style={{ flexShrink: 0 }}>{left}</div>
      <div style={{ fontSize: 14, fontWeight: 500, color: "#1a1a1a" }}>{primary}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// InfoPanel — shows either stop next-departures or line direction+stops
// ─────────────────────────────────────────────────────────────────────────────

function InfoPanel({ selectedStop, selectedLine, activeDirection, setActiveDirection, onClose, onSelectStop }) {
  const isMobile = useMobile();
  if (!selectedStop && !selectedLine) return null;

  const mobileStyle = {
    position: "fixed",
    bottom: 0, left: 0, right: 0,
    zIndex: 1000,
    background: "white",
    borderRadius: "18px 18px 0 0",
    boxShadow: "0 -4px 24px rgba(0,0,0,0.18)",
    fontFamily: "system-ui, sans-serif",
    overflow: "hidden",
    maxHeight: "65vh",
    display: "flex", flexDirection: "column",
    // safe area for notched phones
    paddingBottom: "env(safe-area-inset-bottom)",
  };

  const desktopStyle = {
    position: "absolute",
    bottom: 24, left: 16,
    zIndex: 1000,
    width: 340, maxWidth: "calc(100vw - 32px)",
    background: "white",
    borderRadius: 16,
    boxShadow: "0 8px 32px rgba(0,0,0,0.18)",
    fontFamily: "system-ui, sans-serif",
    overflow: "hidden",
    maxHeight: "62vh",
    display: "flex", flexDirection: "column",
  };

  return (
    <div style={isMobile ? mobileStyle : desktopStyle}>
      {/* Drag handle on mobile */}
      {isMobile && (
        <div style={{ display: "flex", justifyContent: "center", padding: "10px 0 4px" }}>
          <div style={{ width: 36, height: 4, borderRadius: 2, background: "#ddd" }} />
        </div>
      )}
      {selectedStop
        ? <StopPanel stop={selectedStop} onClose={onClose} />
        : <LinePanel line={selectedLine} activeDirection={activeDirection} setActiveDirection={setActiveDirection} onClose={onClose} onSelectStop={onSelectStop} />
      }
    </div>
  );
}

// Stop panel: shows name + next departures filterable by direction
function StopPanel({ stop, onClose }) {
  const [departures, setDepartures] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeDir, setActiveDir] = useState("all");

  useEffect(() => {
    setLoading(true);
    setDepartures(null);
    setActiveDir("all");
    fetch(`${API}/stops/${stop.stop_id}/next-departures`)
      .then(r => r.json())
      .then(d => setDepartures(Array.isArray(d) ? d : []))
      .catch(() => setDepartures([]))
      .finally(() => setLoading(false));
  }, [stop.stop_id]);

  // Build unique directions from loaded departures: { key, headsign, color, textColor, shortName }
  const directions = React.useMemo(() => {
    if (!departures) return [];
    const seen = new Map();
    for (const dep of departures) {
      const key = `${dep.route_id}_${dep.direction_id}`;
      if (!seen.has(key)) {
        seen.set(key, {
          key,
          direction_id: dep.direction_id,
          route_id: dep.route_id,
          headsign: dep.trip_headsign || dep.route_long_name || `Direction ${dep.direction_id}`,
          shortName: dep.route_short_name || dep.route_id,
          color: dep.route_color,
          textColor: dep.route_text_color,
        });
      }
    }
    return Array.from(seen.values());
  }, [departures]);

  const filtered = React.useMemo(() => {
    if (!departures) return [];
    if (activeDir === "all") return departures;
    const [routeId, dirId] = activeDir.split("_");
    return departures.filter(d => d.route_id === routeId && d.direction_id === dirId);
  }, [departures, activeDir]);

  return (
    <>
      <PanelHeader onClose={onClose}>
        <span style={{ fontSize: 20, marginRight: 8 }}>🚏</span>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontWeight: 700, fontSize: 15, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{stop.stop_name}</div>
          {stop.stop_desc && <div style={{ fontSize: 12, color: "#888" }}>{stop.stop_desc}</div>}
        </div>
      </PanelHeader>

      {/* Direction filter tabs — shown only once departures are loaded and there are 2+ directions */}
      {!loading && directions.length > 1 && (
        <div style={{ display: "flex", overflowX: "auto", borderBottom: "1px solid #eee", background: "#fafafa", flexShrink: 0, gap: 0 }}>
          {/* "Tous" tab */}
          <button
            onClick={() => setActiveDir("all")}
            style={{
              flexShrink: 0, padding: "9px 14px", border: "none", cursor: "pointer",
              background: "none", fontSize: 12, fontWeight: activeDir === "all" ? 700 : 500,
              color: activeDir === "all" ? "#0074D9" : "#666",
              borderBottom: activeDir === "all" ? "2px solid #0074D9" : "2px solid transparent",
            }}
          >Tous</button>

          {directions.map(dir => (
            <button
              key={dir.key}
              onClick={() => setActiveDir(dir.key)}
              title={dir.headsign}
              style={{
                flexShrink: 0, padding: "9px 10px", border: "none", cursor: "pointer",
                background: "none", fontSize: 12,
                fontWeight: activeDir === dir.key ? 700 : 500,
                color: activeDir === dir.key ? "#0074D9" : "#666",
                borderBottom: activeDir === dir.key ? "2px solid #0074D9" : "2px solid transparent",
                display: "flex", alignItems: "center", gap: 6,
              }}
            >
              <LineBadge name={dir.shortName} color={dir.color} textColor={dir.textColor} />
              <span style={{ maxWidth: 90, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                ▶ {dir.headsign}
              </span>
            </button>
          ))}
        </div>
      )}

      <div style={{ overflowY: "auto", paddingBottom: 8 }}>
        <SectionLabel>
          Prochains passages{activeDir !== "all" ? ` — ${directions.find(d => d.key === activeDir)?.headsign}` : ""}
        </SectionLabel>
        {loading && <Muted>Chargement des passages…</Muted>}
        {!loading && filtered.length === 0 && <Muted>Aucun passage prévu pour le moment.</Muted>}
        {filtered.map((dep, i) => {
          const mins = dep.minutes_until;
          const timeLabel = mins === 0 ? "À l'arrêt" : mins < 60 ? `${mins} min` : dep.departure_time;
          const timeColor = mins <= 2 ? "#e74c3c" : mins <= 5 ? "#e67e22" : "#27ae60";
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "9px 16px", borderBottom: "1px solid #f5f5f5" }}>
              <LineBadge name={dep.route_short_name || "?"} color={dep.route_color} textColor={dep.route_text_color} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {dep.trip_headsign || dep.route_long_name}
                </div>
                <div style={{ fontSize: 11, color: "#888" }}>{dep.departure_time}</div>
              </div>
              <div style={{ fontWeight: 700, fontSize: 14, minWidth: 52, textAlign: "right", color: timeColor }}>
                {timeLabel}
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
}

// Line panel: shows direction tabs + ordered stops list
function LinePanel({ line, activeDirection, setActiveDirection, onClose, onSelectStop }) {
  const [directions, setDirections] = useState([]);
  const [stops, setStops] = useState(null);

  useEffect(() => {
    fetch(`${API}/lignes/${line.route_id}/directions`)
      .then(r => r.json())
      .then(d => {
        if (Array.isArray(d) && d.length) {
          setDirections(d);
          setActiveDirection(d[0].direction_id);
        }
      })
      .catch(() => {});
  }, [line.route_id]);

  useEffect(() => {
    setStops(null);
    fetch(`${API}/lignes/${line.route_id}/stops?direction_id=${activeDirection}`)
      .then(r => r.json())
      .then(d => setStops(Array.isArray(d) ? d : []))
      .catch(() => setStops([]));
  }, [line.route_id, activeDirection]);

  return (
    <>
      <PanelHeader onClose={onClose}>
        <LineBadge name={line.route_short_name || line.route_id} color={line.route_color} textColor={line.route_text_color} />
        <div style={{ marginLeft: 10, minWidth: 0 }}>
          <div style={{ fontWeight: 700, fontSize: 15, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
            {line.route_long_name}
          </div>
        </div>
      </PanelHeader>

      {/* Direction tabs */}
      {directions.length > 1 && (
        <div style={{ display: "flex", borderBottom: "1px solid #eee", background: "#fafafa", flexShrink: 0 }}>
          {directions.map(dir => (
            <button key={dir.direction_id} onClick={() => setActiveDirection(dir.direction_id)} style={{
              flex: 1, padding: "9px 8px", border: "none", cursor: "pointer", fontSize: 12, background: "none",
              borderBottom: activeDirection === dir.direction_id ? "2px solid #0074D9" : "2px solid transparent",
              fontWeight: activeDirection === dir.direction_id ? 700 : 500,
              color: activeDirection === dir.direction_id ? "#0074D9" : "#666",
              whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
            }} title={dir.headsign}>▶ {dir.headsign}</button>
          ))}
        </div>
      )}

      {/* Stops list */}
      <div style={{ overflowY: "auto", paddingBottom: 8 }}>
        <SectionLabel>Arrêts ({stops?.length ?? "…"})</SectionLabel>
        {!stops && <Muted>Chargement des arrêts…</Muted>}
        {stops?.map((stop, i) => (
          <div key={stop.stop_id} onClick={() => onSelectStop?.(stop)}
            style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 16px", cursor: "pointer", borderBottom: "1px solid #f5f5f5" }}
            onMouseEnter={e => e.currentTarget.style.background = "#f4f7ff"}
            onMouseLeave={e => e.currentTarget.style.background = "white"}
          >
            <div style={{
              width: 22, height: 22, borderRadius: "50%", background: "#0074D9", color: "white",
              fontSize: 10, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
            }}>{i + 1}</div>
            <div style={{ fontSize: 13, fontWeight: 500 }}>{stop.stop_name}</div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Main page
// ─────────────────────────────────────────────────────────────────────────────

export default function Home() {
  const [selectedStop, setSelectedStop] = useState(null);
  const [selectedLine, setSelectedLine] = useState(null);
  const [activeDirection, setActiveDirection] = useState("0");
  const [polyline, setPolyline] = useState([]);
  const [lineStops, setLineStops] = useState([]);
  const [buses, setBuses] = useState([]);
  const [mapCenter, setMapCenter] = useState(null);
  const [mapBounds, setMapBounds] = useState(null);
  const busIntervalRef = useRef(null);

  // Load all lines + stops once on mount — search filters locally, no API calls per keystroke
  const [allLines, setAllLines] = useState([]);
  const [allStops, setAllStops] = useState([]);

  useEffect(() => {
    fetch(`${API}/lignes`)
      .then(r => r.json())
      .then(d => setAllLines(Array.isArray(d) ? d : []))
      .catch(() => {});
    fetch(`${API}/stops`)
      .then(r => r.json())
      .then(d => setAllStops(Array.isArray(d) ? d : []))
      .catch(() => {});
  }, []);

  const handleSelectStop = (stop) => {
    setSelectedStop(stop);
    const lat = parseFloat(stop.stop_lat);
    const lon = parseFloat(stop.stop_lon);
    if (!isNaN(lat) && !isNaN(lon)) {
      setMapCenter([lat, lon]);
      setMapBounds(null);
    }
  };

  const handleSelectLine = (line) => {
    setSelectedLine(line);
    setSelectedStop(null);
    setActiveDirection("0");
  };

  // Re-fetch shape + stops + restart bus poll when line or direction changes
  useEffect(() => {
    if (!selectedLine) {
      setPolyline([]); setLineStops([]); setBuses([]);
      clearInterval(busIntervalRef.current);
      return;
    }
    const id = selectedLine.route_id;
    const dir = activeDirection;

    fetch(`${API}/lignes/${id}/shape?direction_id=${dir}`)
      .then(r => r.json())
      .then(d => {
        if (Array.isArray(d) && d.length) {
          setPolyline(d);
          setMapBounds(d.map(p => [p.lat, p.lon]));
          setMapCenter(null);
        }
      }).catch(() => {});

    fetch(`${API}/lignes/${id}/stops?direction_id=${dir}`)
      .then(r => r.json())
      .then(d => setLineStops(Array.isArray(d) ? d : []))
      .catch(() => {});

    clearInterval(busIntervalRef.current);
    const poll = () =>
      fetch(`${API}/lignes/${id}/buses?direction_id=${dir}&n_buses=3`)
        .then(r => r.json())
        .then(d => setBuses(Array.isArray(d) ? d : []))
        .catch(() => {});
    poll();
    busIntervalRef.current = setInterval(poll, 5000);

    return () => clearInterval(busIntervalRef.current);
  }, [selectedLine, activeDirection]);

  const handleClose = () => {
    setSelectedStop(null);
    setSelectedLine(null);
    setPolyline([]); setLineStops([]); setBuses([]);
    setMapCenter(null); setMapBounds(null);
  };

  return (
    <main style={{ position: "relative", width: "100vw", height: "100vh", overflow: "hidden" }}>
      <MapView
        stops={lineStops}
        polyline={polyline}
        buses={buses}
        selectedStop={selectedStop}
        onStopSelect={handleSelectStop}
        mapCenter={mapCenter}
        mapBounds={mapBounds}
      />
      <SearchBar
        onSelectStop={handleSelectStop}
        onSelectLine={handleSelectLine}
        allLines={allLines}
        allStops={allStops}
      />
      <InfoPanel
        selectedStop={selectedStop}
        selectedLine={selectedLine}
        activeDirection={activeDirection}
        setActiveDirection={setActiveDirection}
        onClose={handleClose}
        onSelectStop={handleSelectStop}
      />
    </main>
  );
}