import "./globals.css"

export const metadata = {
  title: "Bizouk scraper",
  description: "Interface graphique pour lancer les scrapers"
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  )
}
