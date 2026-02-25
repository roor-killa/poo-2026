import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lang Matinitjé",
  description: "Dictionnaire en ligne du créole martiniquais",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children;
}
