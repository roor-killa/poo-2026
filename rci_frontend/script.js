document.addEventListener("DOMContentLoaded", () => {
    const container    = document.getElementById("news-container");
    const dateEl       = document.getElementById("current-date");
    const form         = document.getElementById("scrape-form");
    const btnScrape    = document.getElementById("btn-scrape");
    const statusBar    = document.getElementById("status-bar");
    const statusText   = document.getElementById("status-text");
    const searchSection= document.getElementById("search-section");
    const searchBar    = document.getElementById("search-bar");
    const overlay      = document.getElementById("article-overlay");
    const detailContent= document.getElementById("article-detail-content");
    const btnClose     = document.getElementById("btn-close");

    let articles = [];
    let pollTimer = null;

    if (dateEl) dateEl.textContent = new Date().toLocaleDateString("fr-FR", { dateStyle: "full" });

    // ----------------------------------------------------------------
    // Launch scrape
    // ----------------------------------------------------------------
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const params = {
            max_depth: parseInt(document.getElementById("max-depth").value, 10),
            max_pages: parseInt(document.getElementById("max-pages").value, 10),
            delay:     parseFloat(document.getElementById("delay").value),
        };

        btnScrape.disabled = true;
        statusBar.classList.remove("hidden");
        statusText.textContent = "Lancement du scraping…";
        container.innerHTML = "";
        searchSection.classList.add("hidden");

        fetch("/api/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(params),
        })
        .then((res) => {
            if (res.status === 409) throw new Error("Un scraping est déjà en cours.");
            if (!res.ok) throw new Error("Erreur serveur " + res.status);
            return res.json();
        })
        .then(() => {
            statusText.textContent = "Scraping en cours… (0 articles trouvés)";
            pollTimer = setInterval(pollStatus, 2000);
        })
        .catch((err) => {
            statusText.textContent = "Erreur : " + err.message;
            btnScrape.disabled = false;
        });
    });

    // ----------------------------------------------------------------
    // Poll scraper status
    // ----------------------------------------------------------------
    function pollStatus() {
        fetch("/api/status")
            .then((r) => r.json())
            .then((s) => {
                statusText.textContent = s.running
                    ? `Scraping en cours… (${s.articles} articles, ${s.pages_visited} pages visitées)`
                    : "Terminé !";
                if (!s.running) {
                    clearInterval(pollTimer);
                    fetchResults();
                }
            });
    }

    function fetchResults() {
        fetch("/api/results")
            .then((r) => r.json())
            .then((data) => {
                btnScrape.disabled = false;
                if (data.error) {
                    statusText.textContent = "Erreur : " + data.error;
                    return;
                }
                articles = data.articles || [];
                statusText.textContent = `Terminé — ${articles.length} articles récupérés.`;
                renderArticles(articles);
                if (articles.length) searchSection.classList.remove("hidden");
            });
    }

    // ----------------------------------------------------------------
    // Render article cards
    // ----------------------------------------------------------------
    function renderArticles(list) {
        container.innerHTML = "";
        if (!list.length) {
            container.innerHTML = '<p class="empty">Aucun article trouvé.</p>';
            return;
        }
        list.forEach((art, idx) => {
            const card = document.createElement("article");
            card.className = "article-card";
            card.dataset.index = idx;

            const imgHtml = art.photo
                ? `<img src="${escapeHtml(art.photo)}" alt="" class="article-image" loading="lazy">`
                : "";

            card.innerHTML = `
                ${imgHtml}
                <div class="article-content">
                    <span class="article-badge">Profondeur ${art.depth ?? "?"}</span>
                    <h2>${escapeHtml(art.title || "Sans titre")}</h2>
                    <div class="meta">
                        ${art.author ? "Par <strong>" + escapeHtml(art.author) + "</strong>" : ""}
                        ${art.infos ? " — " + escapeHtml(art.infos) : ""}
                    </div>
                    <p class="preview">${escapeHtml((art.body || "").slice(0, 250))}…</p>
                    <button class="btn-read">Lire l'article</button>
                </div>
            `;
            card.querySelector(".btn-read").addEventListener("click", () => openArticle(idx));
            container.appendChild(card);
        });
    }

    // ----------------------------------------------------------------
    // Article detail overlay
    // ----------------------------------------------------------------
    function openArticle(idx) {
        const art = articles[idx];
        if (!art) return;

        const imgHtml = art.photo
            ? `<img src="${escapeHtml(art.photo)}" alt="" class="detail-image">`
            : "";

        detailContent.innerHTML = `
            ${imgHtml}
            <h1>${escapeHtml(art.title || "Sans titre")}</h1>
            <div class="meta">
                ${art.author ? "Par <strong>" + escapeHtml(art.author) + "</strong>" : ""}
                ${art.infos ? " — " + escapeHtml(art.infos) : ""}
            </div>
            ${art.url ? `<a href="${escapeHtml(art.url)}" target="_blank" rel="noopener">Voir sur rci.fm</a>` : ""}
            <div class="detail-body">${escapeHtml(art.body || "Aucun contenu.")}</div>
        `;
        overlay.classList.remove("hidden");
        document.body.style.overflow = "hidden";
    }

    function closeOverlay() {
        overlay.classList.add("hidden");
        document.body.style.overflow = "";
    }
    btnClose.addEventListener("click", closeOverlay);
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) closeOverlay();
    });

    // ----------------------------------------------------------------
    // Search / filter
    // ----------------------------------------------------------------
    searchBar.addEventListener("input", () => {
        const q = searchBar.value.toLowerCase();
        const filtered = articles.filter((a) =>
            (a.title || "").toLowerCase().includes(q) ||
            (a.body || "").toLowerCase().includes(q) ||
            (a.author || "").toLowerCase().includes(q)
        );
        renderArticles(filtered);
    });

    // ----------------------------------------------------------------
    // Utility
    // ----------------------------------------------------------------
    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }
});