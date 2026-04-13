"""
RAGEngine — Moteur de questions-réponses sur les données Kiprix.
Supporte Ollama (local) et OpenAI (fallback).
"""

import os
import logging
from typing import Optional, List, Dict

from .rag_database import RAGDatabase


class RAGEngine:
    """
    Moteur RAG : Retrieve → Augment → Generate
    
    1. Encode la question en embedding
    2. Recherche les chunks similaires dans pgvector
    3. Construit un prompt enrichi
    4. Génère une réponse via Ollama ou OpenAI
    """

    SYSTEM_PROMPT = """Tu es un assistant spécialisé dans la comparaison de prix 
entre la France métropolitaine et les territoires d'outre-mer (DOM).
Tu analyses les données du site Kiprix.com.
Réponds en français, de manière claire et précise.
Base-toi uniquement sur les données fournies dans le contexte.
Si tu ne sais pas, dis-le clairement."""

    def __init__(self, llm_provider: str = "ollama", model: str = "llama3"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rag_db = RAGDatabase()
        self.llm_provider = llm_provider
        self.model = model
        self._embedding_model = None

    def _get_embedding_model(self):
        if self._embedding_model is None:
            from sentence_transformers import SentenceTransformer
            self._embedding_model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
        return self._embedding_model

    def _embed_query(self, query: str) -> List[float]:
        model = self._get_embedding_model()
        return model.encode(query).tolist()

    def _retrieve(self, query: str, territory: Optional[str], top_k: int) -> List[Dict]:
        embedding = self._embed_query(query)
        return self.rag_db.similarity_search(embedding, territory, top_k)

    def _build_context(self, chunks: List[Dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            score = round(chunk.get('score', 0) * 100, 1)
            parts.append(f"[Source {i} — similarité {score}%]\n{chunk['chunk_text']}")
        return "\n\n".join(parts)

    def _generate_ollama(self, prompt: str) -> str:
        import ollama
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content']

    def _generate_openai(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=self.model if "gpt" in self.model else "gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def ask(self, question: str, territory: Optional[str] = None,
            top_k: int = 5) -> Dict:
        """
        Pose une question au RAG.
        
        Args:
            question: Question en langage naturel
            territory: Filtrer par territoire (ex: 'mq', 'gp')
            top_k: Nombre de chunks à récupérer
            
        Returns:
            Dict avec 'answer', 'sources', 'provider'
        """
        # 1. Retrieve
        chunks = self._retrieve(question, territory, top_k)
        if not chunks:
            return {
                "answer": "Aucune donnée trouvée. Lancez d'abord la vectorisation.",
                "sources": [],
                "provider": None
            }

        # 2. Augment
        context = self._build_context(chunks)
        prompt = f"""Contexte (données Kiprix) :
{context}

Question : {question}

Réponds en te basant sur les données ci-dessus."""

        # 3. Generate
        try:
            if self.llm_provider == "ollama":
                answer = self._generate_ollama(prompt)
                provider = f"Ollama ({self.model})"
            else:
                answer = self._generate_openai(prompt)
                provider = f"OpenAI ({self.model})"
        except Exception as e:
            self.logger.error(f"Erreur LLM ({self.llm_provider}): {e}")
            # Fallback sur l'autre provider
            try:
                if self.llm_provider == "ollama":
                    answer = self._generate_openai(prompt)
                    provider = "OpenAI (fallback)"
                else:
                    answer = self._generate_ollama(prompt)
                    provider = "Ollama (fallback)"
            except Exception as e2:
                return {
                    "answer": f"Erreur LLM : {e2}",
                    "sources": chunks,
                    "provider": None
                }

        return {
            "answer": answer,
            "sources": chunks,
            "provider": provider
        }
