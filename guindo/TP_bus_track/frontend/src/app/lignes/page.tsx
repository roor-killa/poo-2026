import Link from "next/link";
import { api } from "@/lib/api";
import { MapPin, Bus } from "lucide-react";

export const revalidate = 60;

export default async function LignesPage() {
  let lignes = [];
  try {
    lignes = await api.getLignes();
  } catch {
    // API indisponible — affichage dégradé
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">Lignes de bus</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-8 text-sm">
        {lignes.length} ligne{lignes.length > 1 ? "s" : ""} disponible{lignes.length > 1 ? "s" : ""}
      </p>

      {lignes.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <Bus className="w-12 h-12 mx-auto mb-3 opacity-40" />
          <p>Impossible de charger les lignes — vérifiez que l&apos;API est démarrée.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {lignes.map((ligne) => (
            <Link
              key={ligne.id}
              href={`/lignes/${ligne.id}`}
              className="group block p-5 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:shadow-lg transition-shadow"
            >
              {/* Bandeau couleur */}
              <div
                className="h-2 rounded-full mb-4"
                style={{ backgroundColor: ligne.couleur }}
              />
              <h2 className="font-semibold text-base mb-1 group-hover:text-brand-500 transition-colors">
                {ligne.nom}
              </h2>
              {ligne.description && (
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                  {ligne.description}
                </p>
              )}
              <div className="flex items-center gap-1 text-xs text-gray-400">
                <MapPin className="w-3.5 h-3.5" />
                {ligne.nombre_arrets} arrêts
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
