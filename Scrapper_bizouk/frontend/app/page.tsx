"use client"

import { FormEvent, useEffect, useMemo, useState } from "react"

// Structure d'un billet recupere sur une fiche detail Bizouk.
type PriceItem = {
  label?: string | null
  price?: number | null
  fee?: number | null
  total_with_fee?: number | null
  currency?: string
  max_quantity?: number | null
}

// Structure d'un evenement affiche dans les cartes de l'interface.
type EventItem = {
  title?: string | null
  subtitle?: string | null
  event_type?: string | null
  location?: string | null
  date?: string | null
  description?: string | null
  image_url?: string | null
  detail_url?: string | null
  min_total_price?: number | null
  price_items?: PriceItem[]
}

// Format de reponse renvoye par la route FastAPI /api/scrape/events.
type ApiResponse = {
  type: string
  region: string
  pages: number
  limit: number
  count: number
  data: EventItem[]
}

const regions = [
  "martinique",
  "guadeloupe",
  "guyane",
  "reunion",
  "ile-de-france",
]

// Le composant principal gere toute la page: formulaire, appels API et affichage des resultats.

// Affiche les prix en euros avec le format francais.
function formatPrice(value?: number | null) {
  if (value === null || value === undefined) {
    return "N/A"
  }

  return new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency: "EUR",
  }).format(value)
}

// Coupe les longues descriptions pour garder des cartes lisibles.
function shortText(value?: string | null, max = 150) {
  if (!value) {
    return "Description non renseignee."
  }

  return value.length > max ? `${value.slice(0, max).trim()}...` : value
}

export default function HomePage() {
  // Etats du formulaire: region, nombre de pages, limite et cle API.
  const [pages, setPages] = useState(1)
  const [limit, setLimit] = useState(12)
  const [region, setRegion] = useState("martinique")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ApiResponse | null>(null)
  const [error, setError] = useState("")
  const [view, setView] = useState<"cards" | "json">("cards")
  const [apiKey, setApiKey] = useState("")

  // La cle reste seulement dans la session du navigateur pour eviter de la retaper.
  useEffect(() => {
    const savedApiKey = window.sessionStorage.getItem("bizoukScraperApiKey")

    if (savedApiKey) {
      setApiKey(savedApiKey)
    }
  }, [])

  async function runScraper(event: FormEvent<HTMLFormElement>) {
    // Cette fonction appelle le backend FastAPI et met a jour l'interface avec les resultats.
    event.preventDefault()
    setLoading(true)
    setError("")

    try {
      const trimmedApiKey = apiKey.trim()

      if (!trimmedApiKey) {
        throw new Error("Renseigne la cle API avant de lancer le scraping.")
      }

      window.sessionStorage.setItem("bizoukScraperApiKey", trimmedApiKey)

      // URLSearchParams evite de construire l'URL a la main avec des concatenations fragiles.
      const params = new URLSearchParams({
        pages: String(pages),
        limit: String(limit),
        region,
      })
      const res = await fetch(`/api/scrape/events?${params.toString()}`, {
        // Le backend refuse les routes de scraping sans ce header.
        headers: {
          "X-API-Key": trimmedApiKey,
        },
      })

      if (!res.ok) {
        const messages: Record<number, string> = {
          401: "Cle API invalide.",
          429: "Trop de requetes. Attends un peu avant de relancer.",
          503: "La cle API serveur n'est pas configuree dans le .env.",
        }

        throw new Error(messages[res.status] ?? "Impossible de lancer le scraping Bizouk.")
      }

      // La reponse JSON du backend est typée avec ApiResponse pour aider TypeScript.
      const data = (await res.json()) as ApiResponse
      setResult(data)
      setView("cards")
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Impossible de lancer le scraping Bizouk.")
    } finally {
      setLoading(false)
    }
  }

  // Version JSON des donnees pour l'onglet JSON et le bouton d'export.
  const jsonText = useMemo(
    () => JSON.stringify(result?.data ?? [], null, 2),
    [result]
  )

  const eventCount = result?.count ?? 0

  // Cette metrique montre rapidement combien d'evenements ont au moins un prix extrait.
  const pricedEvents =
    result?.data.filter((item) => item.min_total_price !== null && item.min_total_price !== undefined).length ?? 0

  return (
    <main className="app-shell">
      {/* Bandeau haut: identite de l'app + formulaire de lancement du scraping. */}
      <section className="top-band">
        <div className="brand-block">
          <span className="brand-mark">BIZ</span>
          <div>
            <h1>Scraper Bizouk</h1>
            <p>Evenements, tarifs, descriptions et images depuis Bizouk.com.</p>
          </div>
        </div>

        <form className="scrape-form" onSubmit={runScraper}>
          <label>
            <span>Region</span>
            <select value={region} onChange={(event) => setRegion(event.target.value)}>
              {regions.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Pages</span>
            <input
              min={1}
              max={10}
              type="number"
              value={pages}
              onChange={(event) => {
                const nextValue = Number(event.target.value) || 1
                setPages(Math.min(10, Math.max(1, nextValue)))
              }}
            />
          </label>

          <label>
            <span>Max</span>
            <input
              min={1}
              max={100}
              type="number"
              value={limit}
              onChange={(event) => {
                const nextValue = Number(event.target.value) || 1
                setLimit(Math.min(100, Math.max(1, nextValue)))
              }}
            />
          </label>

          <label>
            <span>Cle API</span>
            <input
              autoComplete="off"
              placeholder="X-API-Key"
              type="password"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
            />
          </label>

          <button type="submit" disabled={loading}>
            <span aria-hidden="true">&gt;</span>
            {loading ? "Scraping..." : "Lancer"}
          </button>
        </form>
      </section>

      {/* Indicateurs rapides apres scraping: nombre de resultats, prix, region et limites. */}
      <section className="metrics-row">
        <div>
          <span>Resultats</span>
          <strong>{eventCount}</strong>
        </div>
        <div>
          <span>Avec prix</span>
          <strong>{pricedEvents}</strong>
        </div>
        <div>
          <span>Region</span>
          <strong>{result?.region ?? region}</strong>
        </div>
        <div>
          <span>Pages</span>
          <strong>{result?.pages ?? pages}</strong>
        </div>
        <div>
          <span>Max</span>
          <strong>{result?.limit ?? limit}</strong>
        </div>
      </section>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <>
          {/* Barre d'actions: basculer entre cartes/JSON et exporter les donnees. */}
          <section className="toolbar">
            <div className="segmented">
              <button
                className={view === "cards" ? "active" : ""}
                type="button"
                onClick={() => setView("cards")}
              >
                Cartes
              </button>
              <button
                className={view === "json" ? "active" : ""}
                type="button"
                onClick={() => setView("json")}
              >
                JSON
              </button>
            </div>

            <a
              className="export-link"
              href={`data:text/json;charset=utf-8,${encodeURIComponent(jsonText)}`}
              download={`bizouk-${result.region}-events.json`}
            >
              Exporter JSON
            </a>
          </section>
        </>
      )}

      {!result && !loading && (
        <>
          {/* Etat initial affiche avant le premier lancement. */}
          <section className="empty-state">
            <h2>Pret pour le scraping</h2>
            <p>Choisis une region et le nombre de pages, puis lance la collecte.</p>
          </section>
        </>
      )}

      {loading && (
        <>
          {/* Etat de chargement pendant que le backend scrape les pages Bizouk. */}
          <section className="loading-state">
            <div className="loader" />
            <p>Collecte des evenements et ouverture des fiches detail...</p>
          </section>
        </>
      )}

      {result && view === "json" && (
        <>
          {/* Vue brute pour montrer/exporter exactement les donnees JSON obtenues. */}
          <pre className="json-panel">
            <code>{jsonText}</code>
          </pre>
        </>
      )}

      {result && view === "cards" && (
        <>
          {/* Vue metier: chaque evenement devient une carte lisible par l'utilisateur. */}
          <section className="events-grid">
            {result.data.map((item, index) => (
              <article className="event-card" key={`${item.detail_url ?? item.title}-${index}`}>
                <div className="event-image">
                  {item.image_url ? (
                    <img src={item.image_url} alt={item.title ?? "Evenement Bizouk"} />
                  ) : (
                    <span>Bizouk</span>
                  )}
                </div>

                <div className="event-body">
                  <div className="event-kicker">
                    <span>{item.event_type ?? "Evenement"}</span>
                    <strong>{formatPrice(item.min_total_price)}</strong>
                  </div>

                  <h2>{item.title ?? "Sans titre"}</h2>
                  {item.subtitle && <p className="subtitle">{item.subtitle}</p>}

                  <div className="event-meta">
                    <p>{item.date ?? "Date non renseignee"}</p>
                    <p>{item.location ?? "Lieu non renseigne"}</p>
                  </div>

                  <p className="description">{shortText(item.description)}</p>

                  {item.price_items && item.price_items.length > 0 && (
                    <div className="prices">
                      {item.price_items.slice(0, 3).map((price, priceIndex) => (
                        <span key={`${price.label}-${priceIndex}`}>
                          {price.label ?? "Billet"} - {formatPrice(price.total_with_fee)}
                        </span>
                      ))}
                    </div>
                  )}

                  {item.detail_url && (
                    <a className="detail-link" href={item.detail_url} target="_blank" rel="noreferrer">
                      Ouvrir la fiche
                    </a>
                  )}
                </div>
              </article>
            ))}
          </section>
        </>
      )}
    </main>
  )
}
