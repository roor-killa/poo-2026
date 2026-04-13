import Link from "next/link";
import { api } from "@/lib/api";
import { BadgeStatut } from "@/components/ui/BadgeStatut";
import { ArrowLeft, Navigation, Gauge, MapPin, ArrowRight } from "lucide-react";
import { notFound } from "next/navigation";

export const revalidate = 5;

export default async function BusPage({ params }: { params: { id: string } }) {
  let bus;
  try {
    bus = await api.getBusById(Number(params.id));
  } catch {
    notFound();
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">

      {/* Retour */}
      <Link
        href="/"
        className="inline-flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-brand-500 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Retour à la carte
      </Link>

      {/* En-tête */}
      <div className="flex items-center gap-4 mb-8">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-md"
          style={{ backgroundColor: bus.ligne_couleur }}
        >
          🚌
        </div>
        <div>
          <h1 className="text-2xl font-bold">{bus.nom}</h1>
          <Link
            href={`/lignes/${bus.ligne_id}`}
            className="text-sm font-medium hover:underline"
            style={{ color: bus.ligne_couleur }}
          >
            {bus.ligne_nom}
          </Link>
        </div>
        <div className="ml-auto">
          <BadgeStatut statut={bus.statut} />
        </div>
      </div>

      {/* Cartes infos */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center gap-2 text-gray-400 text-xs mb-2">
            <Navigation className="w-4 h-4" /> Position GPS
          </div>
          <div className="font-mono text-sm font-semibold">
            {bus.latitude.toFixed(5)}
          </div>
          <div className="font-mono text-sm font-semibold">
            {bus.longitude.toFixed(5)}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center gap-2 text-gray-400 text-xs mb-2">
            <Gauge className="w-4 h-4" /> Vitesse
          </div>
          <div className="text-2xl font-bold text-brand-500">
            {bus.vitesse}
            <span className="text-sm font-normal text-gray-400 ml-1">km/h</span>
          </div>
        </div>
      </div>

      {/* Progression entre arrêts */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 p-5">
        <h2 className="font-semibold text-sm text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-4">
          Progression
        </h2>
        <div className="flex items-center gap-3">
          <div className="flex-1 text-sm">
            <div className="flex items-center gap-1.5 text-gray-500 dark:text-gray-400 mb-1">
              <MapPin className="w-3.5 h-3.5" />
              <span className="text-xs">Arrêt courant</span>
            </div>
            <span className="font-medium">
              {bus.arret_courant ?? "—"}
            </span>
          </div>

          <ArrowRight className="w-5 h-5 text-gray-300 dark:text-gray-600 flex-shrink-0" />

          <div className="flex-1 text-sm text-right">
            <div className="flex items-center justify-end gap-1.5 text-gray-500 dark:text-gray-400 mb-1">
              <span className="text-xs">Prochain arrêt</span>
              <MapPin className="w-3.5 h-3.5" />
            </div>
            <span className="font-medium">
              {bus.prochain_arret ?? "—"}
            </span>
          </div>
        </div>
      </div>

      {/* Lien vers la ligne */}
      <div className="mt-6">
        <Link
          href={`/lignes/${bus.ligne_id}`}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-medium text-sm text-white transition-opacity hover:opacity-90"
          style={{ backgroundColor: bus.ligne_couleur }}
        >
          Voir tous les bus de cette ligne
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
