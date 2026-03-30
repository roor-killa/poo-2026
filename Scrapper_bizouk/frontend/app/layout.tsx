export const metadata = {
  title: "bizouk scraper",
  description: "interface graphique pour lancer les scrapers"
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body style={{ margin: 0, fontFamily: "Arial, sans-serif", background: "#f5f5f5" }}>
        {children}
      </body>
    </html>
  )
}