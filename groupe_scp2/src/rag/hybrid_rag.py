"""
HybridRAGEngine — Combine RAG sémantique + requêtes SQL analytiques.

Détecte l'intention de la question et choisit la meilleure stratégie :
- Intent analytique → SQL direct (moins cher, plus cher, comparer, écart...)
- Intent sémantique → RAG classique (similarité vectorielle)
"""

import re
import logging
import psycopg2
from psycopg2.extras import DictCursor
from typing import Optional, List, Dict

from .rag_engine import RAGEngine
from .rag_database import RAGDatabase


class HybridRAGEngine(RAGEngine):
    """
    Extension de RAGEngine avec détection d'intention et requêtes SQL.
    """

    # Mots-clés qui déclenchent une requête SQL analytique
    ANALYTICAL_KEYWORDS = [
        "moins cher", "plus cher", "moins chère", "plus chère",
        "le moins", "le plus", "les moins", "les plus",
        "économique", "abordable", "cher", "chère",
        "comparer", "comparaison", "différence", "écart",
        "meilleur prix", "pire prix", "top", "classement",
        "trouver", "où trouver", "où acheter",
        "liste", "quels produits", "quelles produits",
        "combien", "quel prix", "quel est le prix",
        "résumé", "statistiques", "moyenne",
    ]

    def __init__(self, llm_provider: str = "ollama", model: str = "llama3"):
        super().__init__(llm_provider, model)
        self.logger = logging.getLogger(self.__class__.__name__)

    def _detect_intent(self, question: str) -> str:
        """
        Détecte l'intention de la question.
        Returns: 'analytical' ou 'semantic'
        """
        question_lower = question.lower()
        for keyword in self.ANALYTICAL_KEYWORDS:
            if keyword in question_lower:
                return "analytical"
        return "semantic"

    def _sql_query(self, question: str, territory: Optional[str]) -> str:
        """
        Génère et exécute une requête SQL selon la question.
        Retourne un contexte textuel enrichi.
        """
        question_lower = question.lower()
        conn = self.rag_db.get_connection()
        results = []

        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:

                # Produits les moins chers
                if any(k in question_lower for k in ["moins cher", "moins chère", "économique", "abordable", "meilleur prix"]):
                    query = """
                        SELECT name, price_france, price_dom, difference,
                               territory, territory_name
                        FROM produits
                        WHERE price_dom IS NOT NULL
                          AND price_dom != ''
                          {territory_filter}
                        ORDER BY CAST(
                            REPLACE(
                                REGEXP_REPLACE(
                                    REPLACE(REPLACE(price_dom, '€', ''), ' ', ''),
                                    '[^0-9,.]', '', 'g'
                                ),
                                ',', '.'
                            ) AS FLOAT
                        ) ASC NULLS LAST
                        LIMIT 10
                    """.format(
                        territory_filter="AND territory = %s" if territory else ""
                    )
                    cur.execute(query, (territory,) if territory else ())
                    rows = cur.fetchall()
                    context = "Produits les moins chers en DOM :\n"
                    for i, row in enumerate(rows, 1):
                        context += (
                            f"{i}. {row['name']} ({row['territory_name'] or row['territory']}) "
                            f"— Prix France : {row['price_france']} "
                            f"— Prix DOM : {row['price_dom']} "
                            f"— Écart : {row['difference']}\n"
                        )
                    return context

                # Produits les plus chers
                elif any(k in question_lower for k in ["plus cher", "plus chère", "cher", "chère", "pire prix"]):
                    query = """
                        SELECT name, price_france, price_dom, difference,
                               territory, territory_name
                        FROM produits
                        WHERE price_dom IS NOT NULL
                          AND price_dom != ''
                          {territory_filter}
                        ORDER BY CAST(
                            REPLACE(
                                REGEXP_REPLACE(
                                    REPLACE(REPLACE(price_dom, '€', ''), ' ', ''),
                                    '[^0-9,.]', '', 'g'
                                ),
                                ',', '.'
                            ) AS FLOAT
                        ) DESC NULLS LAST
                        LIMIT 10
                    """.format(
                        territory_filter="AND territory = %s" if territory else ""
                    )
                    cur.execute(query, (territory,) if territory else ())
                    rows = cur.fetchall()
                    context = "Produits les plus chers en DOM :\n"
                    for i, row in enumerate(rows, 1):
                        context += (
                            f"{i}. {row['name']} ({row['territory_name'] or row['territory']}) "
                            f"— Prix France : {row['price_france']} "
                            f"— Prix DOM : {row['price_dom']} "
                            f"— Écart : {row['difference']}\n"
                        )
                    return context

                # Écarts les plus grands
                elif any(k in question_lower for k in ["écart", "différence", "comparer", "comparaison"]):
                    query = """
                        SELECT name, price_france, price_dom, difference,
                               territory, territory_name,
                               unit_price_france, unit_price_dom, unit_reference
                        FROM produits
                        WHERE difference IS NOT NULL
                          AND difference != ''
                          {territory_filter}
                        ORDER BY CAST(
                            REPLACE(
                                REGEXP_REPLACE(
                                    REPLACE(REPLACE(price_dom, '€', ''), ' ', ''),
                                    '[^0-9,.]', '', 'g'
                                ),
                                ',', '.'
                            ) AS FLOAT
                        ) DESC NULLS LAST
                        LIMIT 10
                    """.format(
                        territory_filter="AND territory = %s" if territory else ""
                    )
                    cur.execute(query, (territory,) if territory else ())
                    rows = cur.fetchall()
                    context = "Produits avec les plus grands écarts de prix France/DOM :\n"
                    for i, row in enumerate(rows, 1):
                        context += (
                            f"{i}. {row['name']} ({row['territory_name'] or row['territory']}) "
                            f"— Prix France : {row['price_france']} "
                            f"— Prix DOM : {row['price_dom']} "
                            f"— Écart : {row['difference']}\n"
                        )
                    return context

                # Statistiques générales
                elif any(k in question_lower for k in ["résumé", "statistiques", "moyenne", "combien"]):
                    filter_clause = "WHERE territory = %s" if territory else ""
                    cur.execute(f"""
                        SELECT
                            COUNT(*) as total,
                            territory_name,
                            territory
                        FROM produits
                        {filter_clause}
                        GROUP BY territory, territory_name
                        ORDER BY total DESC
                    """, (territory,) if territory else ())
                    rows = cur.fetchall()
                    context = "Statistiques des produits Kiprix :\n"
                    for row in rows:
                        context += f"- {row['territory_name'] or row['territory']} : {row['total']} produits\n"
                    return context

                # Recherche par nom de produit
                else:
                    # Extraire les mots-clés produit de la question
                    stop_words = {"le", "la", "les", "un", "une", "des", "du", "de",
                                  "où", "ou", "quel", "quelle", "quels", "quelles",
                                  "trouver", "acheter", "prix", "produit", "produits",
                                  "en", "à", "au", "aux", "pour", "sur", "dans",
                                  "martinique", "guadeloupe", "réunion", "guyane"}
                    words = [w for w in re.findall(r'\b\w+\b', question_lower)
                             if len(w) > 3 and w not in stop_words]

                    if words:
                        search_term = " ".join(words[:3])
                        filter_clause = "AND territory = %s" if territory else ""
                        cur.execute(f"""
                            SELECT name, price_france, price_dom, difference,
                                   territory, territory_name
                            FROM produits
                            WHERE name ILIKE %s
                            {filter_clause}
                            LIMIT 10
                        """, (f"%{search_term}%", territory) if territory else (f"%{search_term}%",))
                        rows = cur.fetchall()
                        if rows:
                            context = f"Produits correspondant à '{search_term}' :\n"
                            for i, row in enumerate(rows, 1):
                                context += (
                                    f"{i}. {row['name']} ({row['territory_name'] or row['territory']}) "
                                    f"— Prix France : {row['price_france']} "
                                    f"— Prix DOM : {row['price_dom']} "
                                    f"— Écart : {row['difference']}\n"
                                )
                            return context

        finally:
            conn.close()

        return ""

    def ask(self, question: str, territory: Optional[str] = None,
            top_k: int = 5) -> Dict:
        """
        Pose une question au RAG hybride.
        Détecte l'intention et choisit SQL ou RAG selon le cas.
        """
        intent = self._detect_intent(question)
        self.logger.info(f"Intent détecté : {intent} pour '{question}'")

        # Récupérer le contexte selon l'intention
        if intent == "analytical":
            sql_context = self._sql_query(question, territory)
            if sql_context:
                # Compléter avec RAG pour enrichir
                rag_chunks = self._retrieve(question, territory, top_k=3)
                rag_context = self._build_context(rag_chunks) if rag_chunks else ""

                context = sql_context
                if rag_context:
                    context += f"\n\nContexte supplémentaire :\n{rag_context}"

                prompt = f"""Contexte (données Kiprix) :
{context}

Question : {question}

Réponds de manière claire et structurée en te basant sur les données ci-dessus.
Si la question demande où trouver des produits, liste-les avec leurs prix."""

                try:
                    if self.llm_provider == "ollama":
                        answer = self._generate_ollama(prompt)
                        provider = f"Ollama ({self.model}) — Mode analytique SQL"
                    else:
                        answer = self._generate_openai(prompt)
                        provider = f"OpenAI — Mode analytique SQL"
                except Exception as e:
                    return {
                        "answer": f"Erreur LLM : {e}",
                        "sources": [],
                        "provider": None,
                        "intent": intent
                    }

                return {
                    "answer": answer,
                    "sources": rag_chunks,
                    "provider": provider,
                    "intent": intent
                }

        # Fallback sur RAG sémantique classique
        result = super().ask(question, territory, top_k)
        result["intent"] = intent
        return result