"""
Schémas Pydantic v2 — Lang Matinitjé API
"""
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _domain(url: Optional[str]) -> Optional[str]:
    """Extrait le domaine d'une URL (ex: 'pawolotek.com')."""
    if not url:
        return None
    return urlparse(url).netloc or url


# ---------------------------------------------------------------------------
# Dictionnaire
# ---------------------------------------------------------------------------

class TraductionBrief(BaseModel):
    langue_source: str
    texte_source: str
    texte_cible: str

    model_config = ConfigDict(from_attributes=True)


class DefinitionBrief(BaseModel):
    definition: str
    exemple: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MotSearchResult(BaseModel):
    id: int
    mot_creole: str
    phonetique: Optional[str] = None
    categorie_gram: Optional[str] = None
    traductions: List[TraductionBrief] = []
    definitions: List[DefinitionBrief] = []
    source: Optional[str] = None
    valide: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_mot(cls, mot) -> "MotSearchResult":
        return cls(
            id=mot.id,
            mot_creole=mot.mot_creole,
            phonetique=mot.phonetique,
            categorie_gram=mot.categorie_gram,
            traductions=[
                TraductionBrief(
                    langue_source=t.langue_source,
                    texte_source=t.texte_source,
                    texte_cible=t.texte_cible,
                )
                for t in mot.traductions
            ],
            definitions=[
                DefinitionBrief(definition=d.definition, exemple=d.exemple)
                for d in mot.definitions
            ],
            source=_domain(mot.source.url) if mot.source else None,
            valide=mot.valide,
        )


class MotDetail(BaseModel):
    id: int
    mot_creole: str
    phonetique: Optional[str] = None
    categorie_gram: Optional[str] = None
    traductions: List[TraductionBrief] = []
    definitions: List[DefinitionBrief] = []
    expressions: List[dict] = []
    source_id: Optional[int] = None
    valide: bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_mot(cls, mot) -> "MotDetail":
        return cls(
            id=mot.id,
            mot_creole=mot.mot_creole,
            phonetique=mot.phonetique,
            categorie_gram=mot.categorie_gram,
            traductions=[
                TraductionBrief(
                    langue_source=t.langue_source,
                    texte_source=t.texte_source,
                    texte_cible=t.texte_cible,
                )
                for t in mot.traductions
            ],
            definitions=[
                DefinitionBrief(definition=d.definition, exemple=d.exemple)
                for d in mot.definitions
            ],
            expressions=[],
            source_id=mot.source_id,
            valide=mot.valide,
            created_at=mot.created_at,
        )


class DictionarySearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: List[MotSearchResult]


class MotCreate(BaseModel):
    mot_creole: str
    phonetique: Optional[str] = None
    categorie_gram: Optional[str] = None
    source_id: Optional[int] = None


class MotUpdate(BaseModel):
    mot_creole: Optional[str] = None
    phonetique: Optional[str] = None
    categorie_gram: Optional[str] = None
    source_id: Optional[int] = None


# ---------------------------------------------------------------------------
# Traduction
# ---------------------------------------------------------------------------

class TranslateRequest(BaseModel):
    text: str
    source: str = "fr"
    target: str = "crm"


class TranslateResponse(BaseModel):
    source: str
    target: str
    input: str
    output: str
    confidence: float
    method: str


# ---------------------------------------------------------------------------
# Expressions
# ---------------------------------------------------------------------------

class ExpressionOut(BaseModel):
    id: int
    texte_creole: str
    texte_fr: Optional[str] = None
    type: str
    source: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_expr(cls, expr) -> "ExpressionOut":
        return cls(
            id=expr.id,
            texte_creole=expr.texte_creole,
            texte_fr=expr.texte_fr,
            type=expr.type,
            source=_domain(expr.source.url) if expr.source else None,
        )


class ExpressionsResponse(BaseModel):
    total: int
    results: List[ExpressionOut]


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------

class CorpusOut(BaseModel):
    id: int
    texte_creole: str
    texte_fr: Optional[str] = None
    domaine: str
    source: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_corpus(cls, c) -> "CorpusOut":
        return cls(
            id=c.id,
            texte_creole=c.texte_creole,
            texte_fr=c.texte_fr,
            domaine=c.domaine,
            source=_domain(c.source.url) if c.source else None,
        )


class CorpusResponse(BaseModel):
    total: int
    results: List[CorpusOut]


# ---------------------------------------------------------------------------
# Médias
# ---------------------------------------------------------------------------

class MediaOut(BaseModel):
    id: int
    url: str
    type: str
    titre: Optional[str] = None
    duree_sec: Optional[int] = None
    source: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_media(cls, m) -> "MediaOut":
        return cls(
            id=m.id,
            url=m.url,
            type=m.type,
            titre=m.titre,
            duree_sec=m.duree_sec,
            source=_domain(m.source.url) if m.source else None,
        )


class MediaResponse(BaseModel):
    total: int
    results: List[MediaOut]


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    model_version: str


# ---------------------------------------------------------------------------
# Contributeur
# ---------------------------------------------------------------------------

class ContributeurOut(BaseModel):
    id: int
    pseudo: Optional[str] = None
    nb_contrib: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
