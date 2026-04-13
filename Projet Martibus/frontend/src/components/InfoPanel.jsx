/**
 * components/InfoPanel.jsx
 *
 * Panneau latéral affichant :
 *  – Le statut de la connexion WebSocket
 *  – La liste des bus actifs avec leur ETA
 *  – La légende des lignes
 */

import React, { useMemo, useState } from 'react';

function distanceMetres(lat1, lon1, lat2, lon2) {
  const toRad = (v) => (v * Math.PI) / 180;
  const R = 6371000;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function distanceCumulStops(stops, startIdx, endIdx) {
  if (startIdx === endIdx) return 0;
  const step = startIdx < endIdx ? 1 : -1;
  let sum = 0;
  for (let i = startIdx; i !== endIdx; i += step) {
    const a = stops[i];
    const b = stops[i + step];
    sum += distanceMetres(a.latitude, a.longitude, b.latitude, b.longitude);
  }
  return sum;
}

function formatMinutes(minutes) {
  if (minutes <= 0) return 'imminent';
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}h${m.toString().padStart(2, '0')}`;
}

function normaliserTexte(value) {
  return (value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function indexArretPlusProche(stops, lat, lon) {
  let bestIdx = 0;
  let bestDist = Number.POSITIVE_INFINITY;
  for (let i = 0; i < stops.length; i += 1) {
    const d = distanceMetres(lat, lon, stops[i].latitude, stops[i].longitude);
    if (d < bestDist) {
      bestDist = d;
      bestIdx = i;
    }
  }
  return bestIdx;
}

function simulerEtaBusVersTrajet({ ligne, depart, arrivee, posLat, posLon, speedMs, nextStopName }) {
  const stops = ligne.arrets;
  const depIdx = stops.findIndex((s) => s.id === depart.id);
  const arrIdx = stops.findIndex((s) => s.id === arrivee.id);
  if (depIdx < 0 || arrIdx < 0 || depIdx === arrIdx) return null;

  const desiredDir = arrIdx > depIdx ? 1 : -1;
  let nextIdx = nextStopName
    ? stops.findIndex((s) => normaliserTexte(s.nom) === normaliserTexte(nextStopName))
    : -1;

  if (nextIdx < 0) nextIdx = indexArretPlusProche(stops, posLat, posLon);
  const nextStop = stops[nextIdx];
  const timeToNextSec = distanceMetres(posLat, posLon, nextStop.latitude, nextStop.longitude) / speedMs;
  const maxSteps = stops.length * 8;

  const initialDirs = [];
  if (nextIdx === 0) {
    initialDirs.push(1);
  } else if (nextIdx === stops.length - 1) {
    initialDirs.push(-1);
  } else {
    initialDirs.push(-1, 1);
  }

  const directDistanceDepartArrivee = distanceCumulStops(stops, depIdx, arrIdx);
  const stepStops = [];
  for (let i = depIdx + desiredDir; i !== arrIdx + desiredDir; i += desiredDir) {
    if (i === arrIdx) break;
    stepStops.push(stops[i]);
  }

  let best = null;

  for (const dirStart of initialDirs) {
    let idx = nextIdx;
    let dir = dirStart;
    let t = timeToNextSec;

    for (let step = 0; step < maxSteps; step += 1) {
      let outDir = dir;
      if (idx === 0 && outDir === -1) outDir = 1;
      if (idx === stops.length - 1 && outDir === 1) outDir = -1;

      if (idx === depIdx && outDir === desiredDir) {
        const etaDepartMin = Math.round(t / 60);
        const etaArriveeMin = Math.round((t + (directDistanceDepartArrivee / speedMs)) / 60);

        const candidate = {
          etaDepartMin,
          etaArriveeMin,
          prochainArret: nextStopName || nextStop.nom,
          stopsAvantArrivee: stepStops,
        };

        if (!best || candidate.etaDepartMin < best.etaDepartMin) {
          best = candidate;
        }
        break;
      }

      const nextSegmentIdx = idx + outDir;
      if (nextSegmentIdx < 0 || nextSegmentIdx >= stops.length) break;

      const segDist = distanceMetres(
        stops[idx].latitude,
        stops[idx].longitude,
        stops[nextSegmentIdx].latitude,
        stops[nextSegmentIdx].longitude
      );

      t += segDist / speedMs;
      idx = nextSegmentIdx;
      dir = outDir;
    }
  }

  return best;
}

function InfoPanel({ bus, positions, lignes, arrets, connecte }) {
  const [onglet, setOnglet] = useState('bus'); // 'bus' | 'lignes' | 'trajet'
  const [departTexte, setDepartTexte] = useState('');
  const [arriveeTexte, setArriveeTexte] = useState('');

  const recommandation = useMemo(() => {
    const depart = arrets.find((a) => normaliserTexte(a.nom) === normaliserTexte(departTexte));
    const arrivee = arrets.find((a) => normaliserTexte(a.nom) === normaliserTexte(arriveeTexte));
    if (!depart || !arrivee || depart.id === arrivee.id) return null;

    const candidats = [];

    for (const b of bus) {
      const ligne = lignes.find((l) => l.id === b.ligne_id);
      if (!ligne || !ligne.arrets || ligne.arrets.length < 2) continue;

      const depIdx = ligne.arrets.findIndex((s) => s.id === depart.id);
      const arrIdx = ligne.arrets.findIndex((s) => s.id === arrivee.id);
      if (depIdx < 0 || arrIdx < 0 || depIdx === arrIdx) continue;

      const live = positions.get(b.id);
      const nextStopName = live?.prochainArret;

      const posLat = live?.latitude ?? b.latitude;
      const posLon = live?.longitude ?? b.longitude;
      if (!posLat || !posLon) continue;

      const speedKmh = Math.max(10, live?.vitesse ?? b.vitesse ?? 25);
      const speedMs = speedKmh * 1000 / 3600;

      const projection = simulerEtaBusVersTrajet({
        ligne,
        depart,
        arrivee,
        posLat,
        posLon,
        speedMs,
        nextStopName,
      });
      if (!projection) continue;

      candidats.push({
        bus: b,
        ligne,
        etaDepartMin: projection.etaDepartMin,
        etaArriveeMin: projection.etaArriveeMin,
        prochainArret: projection.prochainArret,
        stopsAvantArrivee: projection.stopsAvantArrivee,
      });
    }

    if (candidats.length === 0) {
      return {
        message: 'Aucun bus direct trouvé pour ce trajet pour le moment.',
      };
    }

    candidats.sort((a, b) => a.etaDepartMin - b.etaDepartMin);
    return { depart, arrivee, meilleur: candidats[0], alternatives: candidats.slice(1, 4) };
  }, [departTexte, arriveeTexte, arrets, bus, lignes, positions]);

  return (
    <aside className="info-panel">
      {/* En-tête */}
      <div className="panel-header">
        <h1 className="panel-title">🚌 MartiBus</h1>
        <span className={`connexion-badge ${connecte ? 'connecte' : 'deconnecte'}`}>
          {connecte ? '● En direct' : '○ Déconnecté'}
        </span>
      </div>

      {/* Onglets */}
      <div className="onglets">
        <button
          className={`onglet-btn ${onglet === 'bus' ? 'actif' : ''}`}
          onClick={() => setOnglet('bus')}
        >
          Bus ({bus.length})
        </button>
        <button
          className={`onglet-btn ${onglet === 'lignes' ? 'actif' : ''}`}
          onClick={() => setOnglet('lignes')}
        >
          Lignes ({lignes.length})
        </button>
        <button
          className={`onglet-btn ${onglet === 'trajet' ? 'actif' : ''}`}
          onClick={() => setOnglet('trajet')}
        >
          Trajet
        </button>
      </div>

      {/* Contenu */}
      <div className="panel-body">
        {onglet === 'bus' && (
          <ul className="bus-list">
            {bus.map((b) => {
              const pos = positions.get(b.id);
              const eta = pos?.etaMinutes;
              return (
                <li key={b.id} className="bus-item">
                  <div className="bus-item-header">
                    <span
                      className="bus-badge"
                      style={{ background: b.ligne_couleur || '#3388ff' }}
                    >
                      {b.immatriculation}
                    </span>
                    <span className="bus-ligne">{b.ligne_nom || '—'}</span>
                  </div>
                  <div className="bus-item-details">
                    <span>🏎 {pos?.vitesse ?? b.vitesse ?? 0} km/h</span>
                    {eta !== undefined && (
                      <span className="eta">
                        ⏱ {eta === 0 ? 'À quai' : `~${eta} min`}
                      </span>
                    )}
                  </div>
                  {pos?.prochainArret && (
                    <div className="bus-prochain">
                      → {pos.prochainArret}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        )}

        {onglet === 'lignes' && (
          <ul className="ligne-list">
            {lignes.map((l) => (
              <li key={l.id} className="ligne-item">
                <span
                  className="ligne-dot"
                  style={{ background: l.couleur || '#3388ff' }}
                />
                <span className="ligne-nom">{l.nom}</span>
              </li>
            ))}
          </ul>
        )}

        {onglet === 'trajet' && (
          <div className="trajet-box">
            <label className="trajet-label" htmlFor="depart">Départ</label>
            <input
              id="depart"
              className="trajet-select"
              list="liste-arrets-depart"
              placeholder="Ex: Schoelcher — Université"
              value={departTexte}
              onChange={(e) => setDepartTexte(e.target.value)}
            />
            <datalist id="liste-arrets-depart">
              {arrets.map((a) => (
                <option key={a.id} value={a.nom} />
              ))}
            </datalist>

            <label className="trajet-label" htmlFor="arrivee">Arrivée</label>
            <input
              id="arrivee"
              className="trajet-select"
              list="liste-arrets-arrivee"
              placeholder="Ex: Fort-de-France — Pointe Simon"
              value={arriveeTexte}
              onChange={(e) => setArriveeTexte(e.target.value)}
            />
            <datalist id="liste-arrets-arrivee">
              {arrets.map((a) => (
                <option key={a.id} value={a.nom} />
              ))}
            </datalist>

            {!recommandation && (
              <p className="trajet-hint">Sélectionne un départ et une arrivée pour trouver le meilleur bus.</p>
            )}

            {recommandation?.message && (
              <p className="trajet-hint">{recommandation.message}</p>
            )}

            {recommandation?.meilleur && (
              <div className="trajet-result">
                <div className="trajet-title">Bus recommandé</div>
                <div className="trajet-main">
                  <span className="bus-badge" style={{ background: recommandation.meilleur.bus.ligne_couleur || '#3388ff' }}>
                    {recommandation.meilleur.bus.immatriculation}
                  </span>
                  <span>{recommandation.meilleur.ligne.nom}</span>
                </div>
                <div className="trajet-metrics">
                  <span>Arrive au départ: {formatMinutes(recommandation.meilleur.etaDepartMin)}</span>
                  <span>Arrive destination: {formatMinutes(recommandation.meilleur.etaArriveeMin)}</span>
                  <span>Prochain arrêt du bus: {recommandation.meilleur.prochainArret}</span>
                </div>
                <div className="trajet-title">Arrêts avant arrivée</div>
                <ul className="trajet-stops">
                  {recommandation.meilleur.stopsAvantArrivee.length === 0 && (
                    <li>Direct après départ</li>
                  )}
                  {recommandation.meilleur.stopsAvantArrivee.map((s) => (
                    <li key={s.id}>{s.nom}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="panel-footer">
        Données GPS mises à jour toutes les 5 s
      </div>
    </aside>
  );
}

export default InfoPanel;
