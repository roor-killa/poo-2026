import Link from "next/link";
import { api } from "@/lib/api";
import { BadgeStatut } from "@/components/ui/BadgeStatut";
import { ArrowLeft, MapPin, Bus } from "lucide-react";
import { notFound } from "next/navigation";

export const revalidate = 30;

export default async function LignePage({ params }: { params: { id: string } }) {
  let ligne;
  try {
    ligne = await api.getLigne(Number(params.id));
  } catch {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">

      {/* Retour */}
      <Link
        href="/lignes"
        className="inline-flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-brand-500 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Toutes les lignes
      </Link>

      {/* En-tête */}
      <div className="flex items-start gap-4 mb-8">
        <div
          className="w-3 h-full min-h-[60px] rounded-full flex-shrink-0"
          style={{ backgroundColor: ligne.couleur }}
        />
        <div>
          <h1 className="text-2xl font-bold mb-1">{ligne.nom}</h1>
          {ligne.description && (
            <p className="text-gray-500 dark:text-gray-400 text-sm">{ligne.description}</p>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">

        {/* Arrêts */}
        <div>
          <h2 className="font-semibold text-base mb-4 flex items-center gap-2">
            <MapPin className="w-4 h-4 text-brand-500" />
            Arrêts ({ligne.arrets?.length ?? 0})
          </h2>
          <ol className="space-y-1">
            {ligne.arrets?.map((arret, idx) => (
              <li key={arret.id} className="flex items-center gap-3">
                <div className="flex flex-col items-center">
                  <div
                    className="w-3 h-3 rounded-full border-2 bg-white dark:bg-gray-900 flex-shrink-0"
                    style={{ borderColor: ligne.couleur }}
                  />
                  {idx < (ligne.arrets?.length ?? 0) - 1 && (
                    <div className="w-0.5 h-5" style={{ backgroundColor: ligne.couleur, opacity: 0.4 }} />
                  )}
                </div>
                <span className="text-sm py-1">{arret.nom}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Bus sur cette ligne */}
        <div>
          <h2 className="font-semibold text-base mb-4 flex items-center gap-2">
            <Bus className="w-4 h-4 text-brand-500" />
            Bus en service ({ligne.bus?.length ?? 0})
          </h2>
          <div className="space-y-3">
            {ligne.bus?.length === 0 && (
              <p className="text-sm text-gray-400">Aucun bus actif sur cette ligne.</p>
            )}
            {ligne.bus?.map((bus) => (
              <Link
                key={bus.id}
                href={`/bus/${bus.id}`}
                className="block p-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-sm">{bus.nom}</span>
                  <BadgeStatut statut={bus.statut} />
                </div>
                {bus.arret_courant && (
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                    📍 {bus.arret_courant}
                  </p>
                )}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
