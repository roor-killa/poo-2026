import type { Ligne, BusPosition } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API error ${res.status} — ${path}`);
  return res.json();
}

export const api = {
  getLignes: ()              => apiFetch<Ligne[]>("/api/lignes/"),
  getLigne:  (id: number)    => apiFetch<Ligne>(`/api/lignes/${id}`),
  getBus:    ()              => apiFetch<BusPosition[]>("/api/bus/"),
  getBusById:(id: number)    => apiFetch<BusPosition>(`/api/bus/${id}`),
};
