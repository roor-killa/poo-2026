import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/ui/Navbar";
import { BusProvider } from "@/context/BusContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BusTrack MQ — Suivi des bus en Martinique",
  description: "Suivez en temps réel la position des bus en Martinique",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className={`${inter.className} bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 min-h-screen`}>
        <BusProvider>
          <Navbar />
          <main className="pt-16">{children}</main>
        </BusProvider>
      </body>
    </html>
  );
}
