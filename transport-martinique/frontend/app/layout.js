import "./globals.css";
import RegisterSW from "../components/RegisterSW";

export const metadata = {
  title: "Transport Martinique",
  description: "Carte des arrets et lignes de transport en Martinique",
  applicationName: "Transport Martinique",
  manifest: "/manifest.webmanifest",
  themeColor: "#0e6ba8"
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>
        <RegisterSW />
        {children}
      </body>
    </html>
  );
}
