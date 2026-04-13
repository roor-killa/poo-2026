"use client";
import { createContext, useContext } from "react";
import { useBusPositions } from "@/hooks/useBusPositions";
import type { BusPosition } from "@/types";

interface BusContextType {
  positions: BusPosition[];
  connected: boolean;
  error: string | null;
}

const BusContext = createContext<BusContextType>({
  positions: [],
  connected: false,
  error: null,
});

export function BusProvider({ children }: { children: React.ReactNode }) {
  const value = useBusPositions();
  return <BusContext.Provider value={value}>{children}</BusContext.Provider>;
}

export const useBus = () => useContext(BusContext);
