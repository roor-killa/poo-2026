"""
Lang Matinitjé — API FastAPI (Phase 3)

Endpoints:
  GET  /health
  GET  /api/v1/me          🔒 (X-API-Key)
  ...  /api/v1/dictionary/*
  POST /api/v1/translate
  GET  /api/v1/expressions
  GET  /api/v1/corpus
  GET  /api/v1/media
  GET  /api/v1/media/{id}
  POST /api/v1/chat
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import require_api_key
from .models.models import Contributeur
from .routers import chat, dictionary, media, translation
from .schemas.schemas import ContributeurOut


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Les tables sont gérées par schema.sql / Docker — pas de create_all ici.
    yield


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Lang Matinitjé API",
    description=(
        "API REST pour le dictionnaire créole martiniquais (kréyòl matinitjé). "
        "Données issues de Pawolotek et Potomitan."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes globales
# ---------------------------------------------------------------------------

@app.get("/health", tags=["meta"], summary="Santé de l'API")
def health():
    """Vérifie que l'API est opérationnelle."""
    return {"status": "ok", "service": "lang-matinitje-api"}


@app.get(
    "/api/v1/me",
    response_model=ContributeurOut,
    tags=["auth"],
    summary="Profil contributeur 🔒",
    dependencies=[Depends(require_api_key)],
)
def me(db: Session = Depends(get_db)) -> ContributeurOut:
    """Retourne le profil du premier contributeur (stub Phase 3)."""
    contributeur = db.query(Contributeur).first()
    if not contributeur:
        raise HTTPException(status_code=404, detail="Aucun contributeur en base")
    return ContributeurOut.model_validate(contributeur)


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

PREFIX = "/api/v1"

app.include_router(dictionary.router, prefix=PREFIX)
app.include_router(translation.router, prefix=PREFIX)
app.include_router(media.router, prefix=PREFIX)
app.include_router(chat.router, prefix=PREFIX)
