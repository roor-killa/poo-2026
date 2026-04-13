import Link from "next/link";
import { Bus } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <Bus className="w-16 h-16 text-gray-300 dark:text-gray-700 mb-4" />
      <h1 className="text-4xl font-bold mb-2">404</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-6">
        Cette page n&apos;existe pas ou le bus a déjà quitté l&apos;arrêt. 🚌
      </p>
      <Link
        href="/"
        className="px-5 py-2.5 bg-brand-500 text-white rounded-xl font-medium hover:bg-brand-600 transition-colors"
      >
        Retour à la carte
      </Link>
    </div>
  );
}
