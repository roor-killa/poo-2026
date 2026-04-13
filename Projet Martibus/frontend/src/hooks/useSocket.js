/**
 * hooks/useSocket.js
 *
 * Hook React personnalisé pour la connexion WebSocket avec Socket.io.
 * Gère la connexion, la reconnexion automatique et les événements GPS.
 */

import { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:3001';

/**
 * @returns {{
 *   positions: Map<number, Object>,  // busId → dernière position
 *   connecte: boolean,
 * }}
 */
export function useSocket() {
  // Map busId → objet position reçu du serveur
  const [positions, setPositions] = useState(new Map());
  const [connecte, setConnecte]   = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    // Création de la connexion Socket.io
    const socket = io(SOCKET_URL, {
      transports:     ['websocket', 'polling'],
      reconnectionDelay: 2000,
    });
    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('🟢 WebSocket connecté');
      setConnecte(true);
    });

    socket.on('disconnect', () => {
      console.log('🔴 WebSocket déconnecté');
      setConnecte(false);
    });

    /**
     * Événement reçu toutes les 5 secondes — tableau de toutes les positions.
     * On reconstruit la Map complète pour déclencher un re-render React.
     */
    socket.on('bus:positions', (positionsList) => {
      setPositions((prev) => {
        const next = new Map(prev);
        positionsList.forEach((pos) => {
          next.set(pos.busId, pos);
        });
        return next;
      });
    });

    // Nettoyage à la destruction du composant
    return () => {
      socket.disconnect();
    };
  }, []);

  return { positions, connecte };
}
