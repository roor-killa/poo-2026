const API_BASE = window.location.port === "5500"
  ? "http://127.0.0.1:8000"
  : window.location.port === "18080"
    ? "http://127.0.0.1:18000"
    : window.location.origin;

const WS_BASE = window.location.port === "5500"
  ? "ws://127.0.0.1:8000"
  : window.location.port === "18080"
    ? "ws://127.0.0.1:18000"
    : `ws://${window.location.host}`;

const apiStatus = document.getElementById("apiStatus");
const refreshBtn = document.getElementById("refreshBtn");
const busTable = document.getElementById("busTable");
const lineList = document.getElementById("lineList");

const kpiTotal = document.getElementById("kpiTotal");
const kpiActive = document.getElementById("kpiActive");
const kpiAlerts = document.getElementById("kpiAlerts");
const kpiCoverage = document.getElementById("kpiCoverage");

const alertForm = document.getElementById("alertForm");
const alertBus = document.getElementById("alertBus");
const alertType = document.getElementById("alertType");
const alertMessage = document.getElementById("alertMessage");
const alertFeedback = document.getElementById("alertFeedback");

const aiForm = document.getElementById("aiForm");
const aiQuery = document.getElementById("aiQuery");
const aiAnswer = document.getElementById("aiAnswer");

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const payload = await res.json();
      if (payload.detail) {
        detail = payload.detail;
      }
    } catch {
      // ignore parse failures
    }
    throw new Error(detail);
  }

  return res.json();
}

function setApiStatus(ok) {
  apiStatus.textContent = ok ? "API connectee" : "API indisponible";
  apiStatus.classList.toggle("status-on", ok);
  apiStatus.classList.toggle("status-off", !ok);
}

function renderBuses(buses) {
  busTable.innerHTML = "";
  for (const bus of buses) {
    const tr = document.createElement("tr");
    const pos = bus.last_position;
    tr.innerHTML = `
      <td>${bus.id}</td>
      <td>${bus.immatriculation}</td>
      <td>${bus.line_id ?? "-"}</td>
      <td>${bus.statut}</td>
      <td>${pos ? `${pos.speed} km/h` : "-"}</td>
      <td>${pos ? new Date(pos.ts * 1000).toLocaleTimeString() : "-"}</td>
    `;
    busTable.appendChild(tr);
  }
}

function renderLines(lines) {
  lineList.innerHTML = "";
  for (const line of lines) {
    const li = document.createElement("li");
    li.textContent = `${line.numero} - ${line.nom} (${line.stops?.length ?? 0} arrets)`;
    lineList.appendChild(li);
  }
}

function renderKpi(kpi) {
  kpiTotal.textContent = kpi.total_buses;
  kpiActive.textContent = kpi.active_buses;
  kpiAlerts.textContent = kpi.open_alerts;
  kpiCoverage.textContent = `${Math.round((kpi.coverage_ratio ?? 0) * 100)}%`;
}

async function refreshAll() {
  try {
    const [health, buses, lines, kpi] = await Promise.all([
      apiGet("/health"),
      apiGet("/api/v1/buses"),
      apiGet("/api/v1/lines"),
      apiGet("/api/v1/analytics/kpi"),
    ]);

    setApiStatus(health.status === "ok");
    renderBuses(buses);
    renderLines(lines);
    renderKpi(kpi);

    if (!mapReady) {
      renderStopsOnMap(lines);
      connectLiveWS("LINE-001");
      connectLiveWS("LINE-002");
      mapReady = true;
    }
    renderBusesOnMap(buses);
  } catch (err) {
    setApiStatus(false);
    console.error(err);
  }
}

alertForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  alertFeedback.textContent = "Envoi en cours...";

  try {
    const payload = {
      bus_id: alertBus.value.trim(),
      type: alertType.value.trim(),
      message: alertMessage.value.trim(),
    };
    const res = await apiPost("/api/v1/alerts", payload);
    alertFeedback.textContent = `Alerte creee: ${res.id}`;
    await refreshAll();
  } catch (err) {
    alertFeedback.textContent = `Erreur: ${err.message}`;
  }
});

aiForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  aiAnswer.textContent = "Chargement...";

  try {
    const res = await apiPost("/api/v1/ai/query", { query: aiQuery.value.trim() });
    aiAnswer.textContent = `${res.answer}\n\n${JSON.stringify(res.data_points, null, 2)}`;
  } catch (err) {
    aiAnswer.textContent = `Erreur: ${err.message}`;
  }
});

refreshBtn.addEventListener("click", refreshAll);

// ─── CARTE LEAFLET — MARTINIQUE ──────────────────────────────────────────────

const stopMarkers = {};
const busMarkers  = {};
const lineColors  = {};
const linePolylines = {};
let mapReady = false;

let map = null;
try {
  map = L.map("map", { zoomControl: true }).setView([14.615, -61.047], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18,
  }).addTo(map);
} catch (e) {
  console.warn("Leaflet unavailable:", e);
}

function buildBusIcon(color, busId) {
  return L.divIcon({
    html: `<div class="bus-dot" style="background:${color}" title="${busId}">
             <span>${busId.replace("BUS-", "")}</span>
           </div>`,
    className: "",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
  });
}

function renderLegend(lines) {
  const legend = document.getElementById("mapLegend");
  if (!legend) return;
  legend.innerHTML = lines.map(l =>
    `<span class="legend-item">
       <span class="legend-dot" style="background:${l.couleur}"></span>
       Ligne ${l.numero} – ${l.nom}
     </span>`
  ).join("");
}

function renderStopsOnMap(lines) {
  if (!map) return;
  Object.values(stopMarkers).forEach(m => m.remove());
  Object.values(linePolylines).forEach(p => p.remove());

  for (const line of lines) {
    lineColors[line.id] = line.couleur;
    const coords = [];

    for (const stop of (line.stops || [])) {
      coords.push([stop.latitude, stop.longitude]);
      const m = L.circleMarker([stop.latitude, stop.longitude], {
        radius: 7,
        color: "#fff",
        weight: 2,
        fillColor: line.couleur,
        fillOpacity: 0.9,
      })
        .bindPopup(
          `<b>${stop.nom}</b><br>
           <span style="color:${line.couleur}">&#9632;</span> Ligne ${line.numero}<br>
           <small>${stop.latitude.toFixed(4)}, ${stop.longitude.toFixed(4)}</small>`
        )
        .addTo(map);
      stopMarkers[stop.id] = m;
    }

    if (coords.length > 1) {
      linePolylines[line.id] = L.polyline(coords, {
        color: line.couleur,
        weight: 3,
        opacity: 0.6,
        dashArray: "6 4",
      }).addTo(map);
    }
  }
  renderLegend(lines);
}

function renderBusesOnMap(buses) {
  if (!map) return;
  for (const bus of buses) {
    const pos = bus.last_position;
    if (!pos) continue;

    const color = lineColors[bus.line_id] || "#00bcd4";
    const popupHtml = `
      <b>${bus.id}</b> — ${bus.immatriculation}<br>
      <span style="color:${color}">&#9632;</span> Ligne ${bus.line_id ?? "?"}<br>
      Vitesse : <b>${pos.speed} km/h</b><br>
      Statut : ${bus.statut}<br>
      <small>${new Date(pos.ts * 1000).toLocaleTimeString("fr-FR")}</small>`;

    if (busMarkers[bus.id]) {
      busMarkers[bus.id].setLatLng([pos.lat, pos.lng]);
      busMarkers[bus.id].setPopupContent(popupHtml);
    } else {
      const icon = buildBusIcon(color, bus.id);
      busMarkers[bus.id] = L.marker([pos.lat, pos.lng], { icon })
        .bindPopup(popupHtml)
        .addTo(map);
    }
  }
}

function connectLiveWS(lineId) {
  if (!map) return;
  const ws = new WebSocket(`${WS_BASE}/ws/live/${lineId}`);
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      const marker = busMarkers[data.bus_id];
      if (marker) {
        marker.setLatLng([data.lat, data.lng]);
        const color = lineColors[data.line_id] || "#00bcd4";
        marker.setPopupContent(
          `<b>${data.bus_id}</b><br>
           <span style="color:${color}">&#9632;</span> Ligne ${data.line_id ?? "?"}<br>
           Vitesse : <b>${data.speed} km/h</b><br>
           <small>${new Date(data.ts * 1000).toLocaleTimeString("fr-FR")}</small>`
        );
      }
    } catch {
      // ignore parse errors
    }
  };
  ws.onclose = () => setTimeout(() => connectLiveWS(lineId), 3000);
}

// ─── INITIALISATION ───────────────────────────────────────────────────────────

refreshAll();
setInterval(refreshAll, 15000);
