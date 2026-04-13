/**
 * App.js — Composant racine de MartiBus
 *
 * Charge les données statiques (bus, arrêts, lignes) via l'API REST,
 * puis écoute les mises à jour GPS via WebSocket.
 */

import React, { useState, useEffect, useCallback } from 'react';
import Map       from './components/Map';
import InfoPanel from './components/InfoPanel';
import { useSocket }                        from './hooks/useSocket';
import { fetchBus, fetchArrets, fetchLignes, fetchLigneDetail } from './services/api';
import './styles/App.css';

function App() {
  const [bus,         setBus]         = useState([]);
  const [arrets,      setArrets]      = useState([]);
  const [lignes,      setLignes]      = useState([]);  // lignes avec arrets[]
  const [chargement,  setChargement]  = useState(true);
  const [erreur,      setErreur]      = useState(null);

  // Connexion WebSocket
  const { positions, connecte } = useSocket();

  /**
   * Chargement initial des données depuis l'API REST.
   * Les lignes sont enrichies avec leurs arrêts ordonnés.
   */
  const chargerDonnees = useCallback(async () => {
    try {
      setChargement(true);
      setErreur(null);

      const [busData, arretsData, lignesBase] = await Promise.all([
        fetchBus(),
        fetchArrets(),
        fetchLignes(),
      ]);

      // Récupération des détails de chaque ligne (arrêts inclus)
      const lignesDetail = await Promise.all(
        lignesBase.map((l) => fetchLigneDetail(l.id))
      );

      setBus(busData);
      setArrets(arretsData);
      setLignes(lignesDetail);
    } catch (err) {
      console.error('Erreur chargement données :', err.message);
      setErreur('Impossible de charger les données. Vérifiez que le serveur est démarré.');
    } finally {
      setChargement(false);
    }
  }, []);

  useEffect(() => {
    chargerDonnees();
  }, [chargerDonnees]);

  // ── Rendu ────────────────────────────────────────────────────────────────────

  if (chargement) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner" />
        <p>Chargement des données MartiBus…</p>
      </div>
    );
  }

  if (erreur) {
    return (
      <div className="error-screen">
        <h2>⚠️ Erreur</h2>
        <p>{erreur}</p>
        <button onClick={chargerDonnees}>Réessayer</button>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <InfoPanel
        bus={bus}
        positions={positions}
        lignes={lignes}
        arrets={arrets}
        connecte={connecte}
      />
      <main className="map-container">
        <Map
          bus={bus}
          arrets={arrets}
          lignes={lignes}
          positions={positions}
        />
      </main>
    </div>
  );
}

export default App;
