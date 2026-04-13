"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bus, Map, List, Sun, Moon, Wifi, WifiOff } from "lucide-react";
import { useDarkMode } from "@/hooks/useDarkMode";
import { useBus } from "@/context/BusContext";
import clsx from "clsx";

export function Navbar() {
  const { dark, toggle } = useDarkMode();
  const { connected } = useBus();
  const pathname = usePathname();

  const links = [
    { href: "/",        label: "Carte",  icon: Map  },
    { href: "/lignes",  label: "Lignes", icon: List },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-16 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto h-full px-4 flex items-center justify-between">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-brand-600 dark:text-brand-100 text-lg">
          <Bus className="w-6 h-6" />
          <span>BusTrack <span className="text-brand-500">MQ</span></span>
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-1">
          {links.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                pathname === href
                  ? "bg-brand-500 text-white"
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              )}
            >
              <Icon className="w-4 h-4" />
              {label}
            </Link>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          {/* Indicateur connexion WS */}
          <div className={clsx(
            "flex items-center gap-1.5 text-xs font-medium px-2 py-1 rounded-full",
            connected
              ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
              : "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400"
          )}>
            {connected
              ? <><Wifi className="w-3 h-3" /> En direct</>
              : <><WifiOff className="w-3 h-3" /> Déconnecté</>
            }
          </div>

          {/* Toggle dark mode */}
          <button
            onClick={toggle}
            className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Basculer le thème"
          >
            {dark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </nav>
  );
}
