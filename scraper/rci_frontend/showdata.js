document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("news-container");
    const dateElement = document.getElementById("current-date");
    const searchBar = document.getElementById("search-bar");

    if (!container) {
        return;
    }

    if (dateElement) {
        dateElement.textContent = "Extractions du " + new Date().toLocaleDateString("fr-FR");
    }

    const candidatePaths = [
        "/api/raw-data",     // Raw data from scraper
    ];

    let articles = [];

    try {
        const { data, sourcePath } = await loadFirstAvailableJson(candidatePaths);
        articles = normalizeArticles(data);

        if (!articles.length) {
            container.innerHTML = '<p class="error-message">Aucune actualite trouvee dans le JSON.</p>';
            return;
        }

        renderArticles(container, articles);
        if (searchBar) {
            searchBar.addEventListener("input", () => {
                const query = searchBar.value.trim().toLowerCase();
                const filtered = articles.filter((article) => {
                    const haystack = [
                        article.title,
                        article.author,
                        article.infos,
                        article.body,
                    ]
                        .join(" ")
                        .toLowerCase();
                    return haystack.includes(query);
                });
                renderArticles(container, filtered);
            });
        }

        console.info("Actualites chargees depuis:", sourcePath);
    } catch (error) {
        console.error("Erreur lors du chargement des actualites:", error);
        container.innerHTML = '<p class="error-message">Impossible de charger les actualites. Lance le projet via un serveur local et verifie les chemins JSON.</p>';
    }
});

async function loadFirstAvailableJson(paths) {
    const errors = [];

    for (const path of paths) {
        try {
            const response = await fetch(path, { cache: "no-store" });
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const data = await response.json();
            
            // Handle different response formats
            if (path === "/api/results" && data.articles) {
                return { data: data.articles, sourcePath: path };
            }
            if (path === "/api/raw-data") {
                // Raw data from scraper - convert to array format if needed
                return { data: Array.isArray(data) ? data : Object.values(data), sourcePath: path };
            }
            return { data, sourcePath: path };
        } catch (error) {
            errors.push(`${path}: ${error.message}`);
        }
    }

    throw new Error(errors.join(" | "));
}

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

function renderArticles(container, list) {
    container.innerHTML = "";

    if (!list.length) {
        container.innerHTML = '<p class="empty-message">Aucun article ne correspond a la recherche.</p>';
        return;
    }

    for (const article of list) {
        const articleElement = document.createElement("article");
        articleElement.className = "article-card";

        const imageHtml = article.photo
            ? `<img src="${escapeHtml(article.photo)}" alt="${escapeHtml(article.title)}" class="article-image" loading="lazy">`
            : "";

        const sourceHtml = article.url
            ? `<a href="${escapeHtml(article.url)}" target="_blank" rel="noopener">Voir la source</a>`
            : "";

        articleElement.innerHTML = `
            ${imageHtml}
            <div class="article-content">
                <span class="article-badge">Actualite</span>
                <h2>${escapeHtml(article.title)}</h2>
                <div class="meta">
                    Par <strong>${escapeHtml(article.author)}</strong>
                    ${article.extractionDate ? ` | Date: ${escapeHtml(article.extractionDate)}` : ""}
                </div>
                ${article.infos ? `<div class="infos-box">${escapeHtml(article.infos)}</div>` : ""}
                <div class="text-body">${escapeHtml(article.body)}</div>
                <div class="source-link">${sourceHtml}</div>
            </div>
        `;

        container.appendChild(articleElement);
    }
}

function escapeHtml(value) {
    const text = String(value ?? "");
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}