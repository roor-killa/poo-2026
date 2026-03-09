document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('news-container');
    const dateElement = document.getElementById('current-date');

    if (dateElement) {
        dateElement.innerText = "Extractions du " + new Date().toLocaleDateString();
    }

    // On définit le chemin vers le fichier JSON
    // Note : Ajuste ce chemin si ton serveur ne trouve pas le fichier
    const jsonPath = "../data/processed/rci.json"; 

    // Utilisation de Fetch pour récupérer les données dynamiquement
    fetch(jsonPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP : ${response.status}`);
            }
            return response.json();
        })
        .then(articlesData => {
            // On vide le conteneur avant d'ajouter les nouveaux articles
            container.innerHTML = "";

            // Boucle sur les données du JSON
            for (const [title, data] of Object.entries(articlesData)) {
                const articleElement = document.createElement('article');
                articleElement.className = 'article-card';

                articleElement.innerHTML = `
                    <img src="${data.photo}" alt="${title}" class="article-image">
                    <div class="article-content">
                        <span class="article-badge">Actualité</span>
                        <h2>${title}</h2>
                        <div class="meta">
                            Par <strong>${data.auteur}</strong> | Extrait le ${data.date_extraction}
                        </div>
                        <div class="infos-box">
                            ${data.infos}
                        </div>
                        <div class="text-body">
                            ${data.contenu}
                        </div>
                    </div>
                `;
                container.appendChild(articleElement);
            }
        })
        .catch(error => {
            console.error("Erreur lors du chargement du JSON :", error);
            container.innerHTML = `<p style="color:red;">Impossible de charger les actualités. Vérifiez que le fichier rci.json est accessible.</p>`;
        });
});