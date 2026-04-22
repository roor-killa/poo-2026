"use client";
import React, { useState, useRef } from "react";

export default function Home() {
  const [maxDepth, setMaxDepth] = useState(1);
  const [maxPages, setMaxPages] = useState(10);
  const [delay, setDelay] = useState(1.5);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState([]);
  const [search, setSearch] = useState("");
  const [scraping, setScraping] = useState(false);
  const pollTimer = useRef(null);

  const filteredArticles = articles.filter((a) =>
    [a.title, a.author, a.infos, a.body].join(" ").toLowerCase().includes(search.toLowerCase())
  );

  function startScrape(e) {
    e.preventDefault();
    setLoading(true);
    setStatus("Lancement du scraping…");
    setArticles([]);
    setScraping(true);
    fetch("/api/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ max_depth: maxDepth, max_pages: maxPages, delay }),
    })
      .then((res) => {
        if (res.status === 409) throw new Error("Un scraping est déjà en cours.");
        if (!res.ok) throw new Error("Erreur serveur " + res.status);
        return res.json();
      })
      .then(() => {
        setStatus("Scraping en cours… (0 articles trouvés)");
        pollTimer.current = setInterval(pollStatus, 2000);
      })
      .catch((err) => {
        setStatus("Erreur : " + err.message);
        setLoading(false);
        setScraping(false);
      });
  }

  function pollStatus() {
    fetch("/api/status")
      .then((r) => r.json())
      .then((s) => {
        setStatus(
          s.running
            ? `Scraping en cours… (${s.articles} articles, ${s.pages_visited} pages visitées)`
            : "Terminé !"
        );
        if (!s.running) {
          clearInterval(pollTimer.current);
          fetchResults();
        }
      });
  }

  function fetchResults() {
    fetch("/api/results")
      .then((r) => r.json())
      .then((data) => {
        setLoading(false);
        setScraping(false);
        if (data.error) {
          setStatus("Erreur : " + data.error);
        } else {
          setArticles(data.articles || []);
        }
      });
  }

  return (
    <div style={{ fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', background: '#f4f4f9', minHeight: '100vh' }}>
      <header style={{ background: '#0056b3', color: 'white', padding: '2rem', textAlign: 'center', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
        <h1>RCI Scraper</h1>
        <p>{new Date().toLocaleDateString("fr-FR", { dateStyle: "full" })}</p>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
          <h1>Portail d'Information</h1>
          <nav style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <a href="/" style={{ padding: '0.6rem 1.2rem', background: 'rgba(255,255,255,0.5)', color: 'white', borderRadius: 6, fontWeight: 600, textDecoration: 'none', borderBottom: '3px solid white' }}>Scraping</a>
            <a href="/showdata" style={{ padding: '0.6rem 1.2rem', background: 'rgba(255,255,255,0.2)', color: 'white', borderRadius: 6, fontWeight: 600, textDecoration: 'none' }}>Données</a>
          </nav>
        </div>
      </header>

      <section style={{ maxWidth: 700, margin: '2rem auto', background: 'white', borderRadius: 10, padding: '2rem', boxShadow: '0 4px 15px rgba(0,0,0,0.08)' }}>
        <h2 style={{ color: '#0056b3' }}>Paramètres du scraping</h2>
        <form onSubmit={startScrape} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1.2rem', marginBottom: '1.5rem' }}>
          <label>
            Profondeur max
            <input type="number" value={maxDepth} min={0} max={3} onChange={e => setMaxDepth(Number(e.target.value))} style={{ marginTop: 6, padding: 8, borderRadius: 6, border: '1px solid #ccc' }} />
            <span style={{ fontSize: 12, color: '#888' }}>0 = page de départ seule, max 3</span>
          </label>
          <label>
            Pages max
            <input type="number" value={maxPages} min={1} max={100} onChange={e => setMaxPages(Number(e.target.value))} style={{ marginTop: 6, padding: 8, borderRadius: 6, border: '1px solid #ccc' }} />
            <span style={{ fontSize: 12, color: '#888' }}>Nombre total de pages visitées (1-100)</span>
          </label>
          <label>
            Délai (s)
            <input type="number" value={delay} min={0.5} max={10} step={0.5} onChange={e => setDelay(Number(e.target.value))} style={{ marginTop: 6, padding: 8, borderRadius: 6, border: '1px solid #ccc' }} />
            <span style={{ fontSize: 12, color: '#888' }}>Pause entre requêtes (0.5-10s)</span>
          </label>
          <button type="submit" disabled={loading} style={{ gridColumn: '1/-1', marginTop: 16, padding: '0.8rem', background: loading ? '#aaa' : '#0056b3', color: 'white', border: 'none', borderRadius: 8, fontSize: 16, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer' }}>Lancer le scraping</button>
        </form>
        {scraping && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 12, padding: '0.8rem 1rem', background: '#eef4ff', borderRadius: 8, fontSize: 15 }}>
            <div style={{ width: 18, height: 18, border: '3px solid #ccc', borderTopColor: '#0056b3', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
            <span>{status}</span>
          </div>
        )}
      </section>

      {articles.length > 0 && (
        <section style={{ maxWidth: 700, margin: '0 auto 1.5rem' }}>
          <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Filtrer les articles…" style={{ width: '100%', padding: '0.7rem 1rem', border: '1px solid #ccc', borderRadius: 8, fontSize: 16 }} />
        </section>
      )}

      <main style={{ maxWidth: 1000, margin: '1rem auto 2rem', padding: '0 1rem' }}>
        {articles.length === 0 && !scraping && <p style={{ textAlign: 'center', color: '#888', fontStyle: 'italic', padding: '2rem' }}>Aucun article à afficher.</p>}
        {filteredArticles.map((a, i) => (
          <article key={i} style={{ background: 'white', marginBottom: '2rem', borderRadius: 10, overflow: 'hidden', boxShadow: '0 4px 15px rgba(0,0,0,0.08)' }}>
            {a.photo && <img src={a.photo} alt={a.title} style={{ width: '100%', height: 260, objectFit: 'cover' }} />}
            <div style={{ padding: '1.5rem 2rem' }}>
              <span style={{ display: 'inline-block', background: '#e63946', color: 'white', padding: '0.25rem 0.7rem', borderRadius: 20, fontSize: 12, marginBottom: 10 }}>Actualité</span>
              <h2 style={{ color: '#0056b3', margin: '0.3rem 0 0.6rem' }}>{a.title}</h2>
              <div style={{ fontSize: 14, color: '#666', borderBottom: '1px solid #eee', paddingBottom: 13, marginBottom: 13 }}>
                Par <strong>{a.author}</strong>
                {a.extractionDate ? ` | Date: ${a.extractionDate}` : ""}
              </div>
              {a.infos && <div style={{ background: '#f8f9fa', borderLeft: '5px solid #0056b3', padding: 16, fontStyle: 'italic', margin: '1rem 0' }}>{a.infos}</div>}
              <div style={{ lineHeight: 1.6, whiteSpace: 'pre-line' }}>{a.body}</div>
              {a.url && <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid #eee' }}><a href={a.url} target="_blank" rel="noopener" style={{ color: '#0056b3', fontWeight: 600, textDecoration: 'none' }}>Voir la source</a></div>}
            </div>
          </article>
        ))}
      </main>
    </div>
  );
}
