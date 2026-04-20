"use client";
import React, { useEffect, useState } from "react";

function normalizeArticles(rawData) {
  if (Array.isArray(rawData)) {
    return rawData.map((item) => ({
      title: item.title || item.titre || "Sans titre",
      author: item.author || item.auteur || "Auteur inconnu",
      photo: item.photo || "",
      infos: item.infos || item.resume || "",
      body: item.body || item.contenu || item.texte_creole || item.texte_fr || "",
      extractionDate: item.date_extraction || item.date_publication || "",
      url: item.url || "",
    }));
  }
  if (rawData && typeof rawData === "object") {
    return Object.entries(rawData).map(([title, item]) => ({
      title,
      author: item.auteur || item.author || "Auteur inconnu",
      photo: item.photo || "",
      infos: item.infos || "",
      body: item.contenu || item.body || "",
      extractionDate: item.date_extraction || "",
      url: item.url || "",
    }));
  }
  return [];
}

export default function ShowData() {
  const [articles, setArticles] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError("");
      try {
        const res = await fetch("/api/raw-data", { cache: "no-store" });
        if (!res.ok) throw new Error("Erreur HTTP " + res.status);
        const data = await res.json();
        setArticles(normalizeArticles(data));
      } catch (e) {
        setError("Impossible de charger les actualités.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const filtered = articles.filter((a) =>
    [a.title, a.author, a.infos, a.body].join(" ").toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', background: '#f4f4f9', minHeight: '100vh' }}>
      <header style={{ background: '#0056b3', color: 'white', padding: '2rem', textAlign: 'center', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
          <h1>Portail d'Information</h1>
          <nav style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <a href="/" style={{ padding: '0.6rem 1.2rem', background: 'rgba(255,255,255,0.2)', color: 'white', borderRadius: 6, fontWeight: 600, textDecoration: 'none' }}>Scraping</a>
            <a href="/showdata" style={{ padding: '0.6rem 1.2rem', background: 'rgba(255,255,255,0.5)', color: 'white', borderRadius: 6, fontWeight: 600, textDecoration: 'none', borderBottom: '3px solid white' }}>Données</a>
          </nav>
        </div>
        <p>{`Extractions du ${new Date().toLocaleDateString("fr-FR")}`}</p>
        <div style={{ marginTop: 24, maxWidth: 600, marginLeft: 'auto', marginRight: 'auto' }}>
          <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Rechercher un article (titre, auteur, contenu)..." style={{ width: '100%', padding: '0.8rem 1rem', border: '1px solid rgba(255,255,255,0.3)', background: 'rgba(255,255,255,0.1)', color: 'white', borderRadius: 6, fontSize: 16 }} />
        </div>
      </header>
      <main style={{ maxWidth: 1000, margin: '1rem auto 2rem', padding: '0 1rem' }}>
        {loading && <p id="loading-state">Chargement des actualités...</p>}
        {error && <p className="error-message">{error}</p>}
        {!loading && !error && filtered.length === 0 && <p className="empty-message">Aucun article ne correspond à la recherche.</p>}
        {filtered.map((a, i) => (
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
      <footer style={{ textAlign: 'center', padding: '2rem', color: '#888' }}>
        &copy; 2026 - Interface de démonstration de données RCI
      </footer>
    </div>
  );
}
