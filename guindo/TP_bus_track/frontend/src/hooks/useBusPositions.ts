"use client";
import { useEffect, useRef, useState, useCallback } from "react";
import type { BusPosition } from "@/types";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export function useBusPositions() {
  const [positions, setPositions] = useState<BusPosition[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      const ws = new WebSocket(`${WS_URL}/ws/positions`);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnected(true);
        setError(null);
      };

      ws.onmessage = (e) => {
        try {
          const data: BusPosition[] = JSON.parse(e.data);
          setPositions(data);
        } catch {
          console.error("[WS] Erreur parsing:", e.data);
        }
      };

      ws.onerror = () => {
        setError("Connexion WebSocket impossible");
        setConnected(false);
      };

      ws.onclose = () => {
        setConnected(false);
        // Reconnexion automatique après 3s
        reconnectTimer.current = setTimeout(connect, 3000);
      };
    } catch (err) {
      setError("Impossible de se connecter au serveur");
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
    };
  }, [connect]);

  return { positions, connected, error };
}
