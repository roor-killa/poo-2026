import "./globals.css";
 
export const metadata = {
  title: "Transport Martinique",
  description: "Lignes et arrêts de bus en Martinique",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Bus MTQ",
  },
};
 
export const viewport = {
  themeColor: "#0074D9",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,   // prevents double-tap zoom fighting Leaflet
  userScalable: false,
};
 
export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <head>
        {/* iOS PWA */}
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Bus MTQ" />
 
        {/* Android / Chrome PWA */}
        <link rel="manifest" href="/manifest.json" />
        <meta name="mobile-web-app-capable" content="yes" />
      </head>
      <body style={{ margin: 0, padding: 0, overflow: "hidden" }}>
        {/* Register service worker */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js');
                });
              }
            `,
          }}
        />
        {children}
      </body>
    </html>
  );
}