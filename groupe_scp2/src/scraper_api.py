"""
scraper_api.py — API interne pour déclencher le scraping et le chatbot RAG Kiprix.

Usage interne Docker :
    POST http://scraper-api:8090/scrape   → déclenche un scraping
    POST http://scraper-api:8090/chat     → pose une question au RAG hybride
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Kiprix Scraper API")


# ── Scraping ─────────────────────────────────────────────────────

class ScrapeRequest(BaseModel):
    territory: str = "mq"
    pages: int = 1


class ScrapeResponse(BaseModel):
    nb_produits: int
    status: str
    message: Optional[str] = None


@app.post("/scrape", response_model=ScrapeResponse)
def run_scrape(req: ScrapeRequest) -> ScrapeResponse:
    try:
        from .scrapers.kiprix_scraper import KiprixScraper
        from .db_manager import DBManager

        scraper = KiprixScraper(territory=req.territory, delay=1.0)
        data = scraper.scrape(max_pages=req.pages)

        if data:
            db = DBManager()
            db.init_db()
            db.save_products(data)

        return ScrapeResponse(nb_produits=len(data), status="success")

    except ValueError as e:
        return ScrapeResponse(nb_produits=0, status="error", message=str(e))
    except Exception as e:
        return ScrapeResponse(nb_produits=0, status="error", message=str(e)[:500])


# ── Chatbot RAG ───────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str
    territory: Optional[str] = None
    provider: str = "ollama"
    model: str = "llama3"


class ChatResponse(BaseModel):
    answer: str
    provider: Optional[str] = None
    intent: Optional[str] = None


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    Répond à une question sur les prix Kiprix via RAG hybride (SQL + LLM).
    Si Ollama n'est pas disponible, retourne directement le contexte SQL.
    """
    # Ollama dans Docker doit pointer vers l'hôte Mac
    ollama_host = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")
    os.environ["OLLAMA_HOST"] = ollama_host

    from .rag.hybrid_rag import HybridRAGEngine

    engine = HybridRAGEngine(llm_provider=req.provider, model=req.model)

    # Détecter l'intention pour savoir si on peut répondre sans LLM
    intent = engine._detect_intent(req.question)

    # Essayer via le moteur complet (SQL + LLM)
    try:
        result = engine.ask(req.question, territory=req.territory)
        return ChatResponse(
            answer=result["answer"],
            provider=result.get("provider"),
            intent=result.get("intent", intent),
        )
    except Exception as e:
        # LLM indisponible → répondre avec le contexte SQL directement
        if intent == "analytical":
            try:
                sql_context = engine._sql_query(req.question, req.territory)
                if sql_context:
                    return ChatResponse(
                        answer=sql_context,
                        provider="SQL direct (LLM indisponible)",
                        intent=intent,
                    )
            except Exception:
                pass

        return ChatResponse(
            answer=(
                "⚠️ Le LLM (Ollama) n'est pas disponible.\n\n"
                "Pour activer le chatbot IA :\n"
                "1. Installe Ollama : https://ollama.com\n"
                "2. Lance : `ollama pull llama3`\n"
                "3. Ollama doit tourner sur ton Mac (port 11434)"
            ),
            provider=None,
            intent=intent,
        )


# ── Santé ─────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}
