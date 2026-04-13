import clsx from "clsx";

const STATUTS = {
  en_service:   { label: "En service",   classes: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" },
  a_larret:     { label: "À l'arrêt",    classes: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400" },
  hors_service: { label: "Hors service", classes: "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400" },
};

export function BadgeStatut({ statut }: { statut: string }) {
  const s = STATUTS[statut as keyof typeof STATUTS] ?? STATUTS.hors_service;
  return (
    <span className={clsx("text-xs font-semibold px-2 py-0.5 rounded-full", s.classes)}>
      {s.label}
    </span>
  );
}
