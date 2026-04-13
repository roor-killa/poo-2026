"use client";
import type { BusPosition, Ligne } from "@/types";
import { BadgeStatut } from "@/components/ui/BadgeStatut";
import clsx from "clsx";

interface SidebarProps {
  lignes: Ligne[];
  positions: BusPosition[];
  selectedLigneId: number | null;
  onSelectLigne: (id: number | null) => void;
  onSelectBus: (bus: BusPosition) => void;
}

export function Sidebar({ lignes, positions, selectedLigneId, onSelectLigne, onSelectBus }: SidebarProps) {
  const busVisibles = selectedLigneId
    ? positions.filter((b) => b.ligne_id === selectedLigneId)
    : positions;

  return (
    <aside className="w-80 h-full flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 overflow-hidden">

      {/* Filtres lignes */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">
          Lignes
        </h2>
        <div className="flex flex-col gap-1">
          <button
            onClick={() => onSelectLigne(null)}
            className={clsx(
              "text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors",
              selectedLigneId === null
                ? "bg-brand-500 text-white"
                : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
            )}
          >
            Toutes les lignes
          </button>
          {lignes.map((l) => (
            <button
              key={l.id}
              onClick={() => onSelectLigne(l.id)}
              className={clsx(
                "text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2",
                selectedLigneId === l.id
                  ? "bg-gray-100 dark:bg-gray-800"
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              )}
            >
              <span
                className="w-3 h-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: l.couleur }}
              />
              <span className="truncate">{l.nom}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Liste bus */}
      <div className="flex-1 overflow-y-auto p-4">
        <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">
          Bus actifs ({busVisibles.length})
        </h2>
        <div className="flex flex-col gap-2">
          {busVisibles.map((bus) => (
            <button
              key={bus.id}
              onClick={() => onSelectBus(bus)}
              className="text-left p-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-semibold text-sm">{bus.nom}</span>
                <BadgeStatut statut={bus.statut} />
              </div>
              <div className="text-xs font-medium mb-1" style={{ color: bus.ligne_couleur }}>
                {bus.ligne_nom}
              </div>
              {bus.arret_courant && (
                <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                  📍 {bus.arret_courant}
                </div>
              )}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}
