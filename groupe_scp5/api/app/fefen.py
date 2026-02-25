"""
fefen.py — Moteur Fèfèn intégré à l'API FastAPI
=================================================
Version allégée de chatbot/fefen.py : pas de CLI, pas de save/load,
index construit en mémoire au démarrage de l'app (lifespan).

Chemin dataset résolu par variable d'env FEFEN_DATASET_DIR
ou par défaut /app/dataset/data (volume Docker).
"""

from __future__ import annotations

import json
import logging
import os
import random
import re
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Chemin du dataset (configurable via env)
# ---------------------------------------------------------------------------

DATASET_DIR = Path(os.getenv("FEFEN_DATASET_DIR", "/app/dataset/data"))

# ---------------------------------------------------------------------------
# Phrases de réponse en créole
# ---------------------------------------------------------------------------

INTRO_LEXIQUE = ["Sa vle di :", "Définisyon :", "An mo-a di :"]
INTRO_CONTE   = ["An istwa :", "Men an bout istwa :"]
INTRO_POEME   = ["An pwézi :", "Men an bout pwézi :"]
ACCROCHES     = ["An mò pou ou :", "Man trouvé sa :", "Gadé sa man jwenn :"]
FALLBACKS     = [
    "Man pa konprann byen. Eséyé di mwen an lòt jan.",
    "Ou pé répété ? Man pa jwenn anyen pou sa.",
    "Man pa ka réponn sa-a. Mandé mwen anlè kréyol !",
]


# ---------------------------------------------------------------------------
# Classe Fèfèn
# ---------------------------------------------------------------------------

class Fefen:
    """Chatbot retrieval-based TF-IDF pour le créole martiniquais."""

    def __init__(self, min_score: float = 0.05) -> None:
        self.min_score   = min_score
        self._corpus:     list[dict[str, Any]] = []
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix:     Any = None

    # ------------------------------------------------------------------
    # Construction de l'index
    # ------------------------------------------------------------------

    def build(self) -> "Fefen":
        """Charge le dataset local et construit l'index TF-IDF."""
        self._load_data()
        if not self._corpus:
            log.warning("Corpus vide — Fèfèn en mode fallback uniquement")
            return self

        texts = [self._entry_text(e) for e in self._corpus]
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
            max_features=20_000,
        )
        self._matrix = self._vectorizer.fit_transform(texts)
        log.info("Fèfèn : index TF-IDF (%d entrées, %d features)",
                 *self._matrix.shape)
        return self

    def _load_data(self) -> None:
        seen: set[str] = set()
        for config in ("lexique", "corpus"):
            path = DATASET_DIR / config / "train.jsonl"
            if not path.exists():
                log.warning("Dataset introuvable : %s", path)
                continue
            with path.open(encoding="utf-8") as f:
                for line in f:
                    e = json.loads(line)
                    uid = e.get("id", "")
                    if uid not in seen:
                        seen.add(uid)
                        self._corpus.append(e)
        log.info("Fèfèn : %d entrées chargées depuis %s", len(self._corpus), DATASET_DIR)

    # ------------------------------------------------------------------
    # Réponse
    # ------------------------------------------------------------------

    def reply(self, message: str) -> str:
        """Retourne une réponse en créole pour le message donné."""
        if self._vectorizer is None or not self._corpus:
            return random.choice(FALLBACKS)

        vec  = self._vectorizer.transform([message.lower()])
        sims = cosine_similarity(vec, self._matrix).flatten()
        idx  = int(np.argmax(sims))

        if sims[idx] < self.min_score:
            return random.choice(FALLBACKS)

        return self._format(self._corpus[idx])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _entry_text(self, e: dict) -> str:
        parts = [
            e.get("texte", ""), e.get("mot", ""),
            e.get("definition", ""), e.get("titre", ""),
            " ".join(e.get("hashtags", [])),
        ]
        return re.sub(r"\s+", " ", " ".join(p for p in parts if p)).lower()

    def _format(self, e: dict) -> str:
        cat    = e.get("categorie", "")
        source = e.get("source", "")

        if source == "pawolotek.com" or e.get("mot"):
            mot = e.get("mot", "")
            dfn = e.get("definition", "")
            txt = f"**{mot}** — {dfn}" if dfn else f"**{mot}**"
            return f"{random.choice(INTRO_LEXIQUE)}\n\n{txt}"

        texte   = e.get("texte", "")
        extrait = texte[:300].rsplit(" ", 1)[0] + "…" if len(texte) > 300 else texte

        if cat == "poeme":
            titre = e.get("titre", "")
            return f"{random.choice(INTRO_POEME)}\n\n*{titre}*\n\n{extrait}"

        if cat == "conte":
            titre    = e.get("titre", "")
            titre_fr = e.get("titre_fr", "")
            header   = f"*{titre}*" + (f" ({titre_fr})" if titre_fr else "")
            return f"{random.choice(INTRO_CONTE)}\n\n{header}\n\n{extrait}"

        return f"{random.choice(ACCROCHES)}\n\n{extrait}"
