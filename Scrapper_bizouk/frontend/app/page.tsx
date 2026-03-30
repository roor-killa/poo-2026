"use client"

import { useState } from "react"

type ApiResponse = {
  type: string
  count: number
  data: unknown[]
}

export default function HomePage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ApiResponse | null>(null)
  const [error, setError] = useState("")

  async function runScraper(kind: "business" | "news") {
    setLoading(true)
    setError("")
    setResult(null)

    try {
      const res = await fetch(`/api/scrape/${kind}`)
      if (!res.ok) {
        throw new Error("erreur pendant le scraping")
      }

      const data = await res.json()
      setResult(data)
    } catch (e) {
      setError("impossible de lancer le scraper")
    } finally {
      setLoading(false)
    }
  }

  const jsonText = result ? JSON.stringify(result.data, null, 2) : ""

  return (
    <main
      style={{
        maxWidth: 1100,
        margin: "0 auto",
        padding: 24,
      }}
    >
      <h1 style={{ marginBottom: 8 }}>bizouk scraper</h1>
      <p style={{ marginTop: 0 }}>
        clique sur un bouton pour lancer le scraper et afficher le json
      </p>

      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <button
          onClick={() => runScraper("business")}
          disabled={loading}
          style={{
            padding: "12px 18px",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            background: "#111",
            color: "#fff",
          }}
        >
          lancer business
        </button>

        <button
          onClick={() => runScraper("news")}
          disabled={loading}
          style={{
            padding: "12px 18px",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            background: "#2563eb",
            color: "#fff",
          }}
        >
          lancer news
        </button>
      </div>

      {loading && <p>scraping en cours</p>}
      {error && <p>{error}</p>}

      {result && (
        <div
          style={{
            background: "#fff",
            borderRadius: 12,
            padding: 16,
            boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
          }}
        >
          <p>
            type lancé <strong>{result.type}</strong>
          </p>
          <p>
            nombre de résultats <strong>{result.count}</strong>
          </p>

          <a
            href={`data:text/json;charset=utf-8,${encodeURIComponent(jsonText)}`}
            download={`${result.type}.json`}
            style={{
              display: "inline-block",
              marginBottom: 16,
              padding: "10px 14px",
              borderRadius: 8,
              background: "#16a34a",
              color: "#fff",
              textDecoration: "none",
            }}
          >
            télécharger le json
          </a>

          <pre
            style={{
              overflowX: "auto",
              whiteSpace: "pre-wrap",
              background: "#0f172a",
              color: "#e2e8f0",
              padding: 16,
              borderRadius: 8,
              maxHeight: 600,
            }}
          >
            {jsonText}
          </pre>
        </div>
      )}
    </main>
  )
}