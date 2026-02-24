"""
Router /chat — Chatbot Fèfèn (stub déterministe)

reply_index = len(message) % 4 → tests stables sans mock.
"""
import uuid

from fastapi import APIRouter

from ..schemas.schemas import ChatRequest, ChatResponse


router = APIRouter(prefix="/chat", tags=["chat"])

_REPLIES = [
    "Mwen ka tchenbé ! Yo ka krié mwen Fèfèn ! é ou mèm, say i di a ?",
    "Sa ou vlé savé ? Mwen la pou aidé'w !",
    "Kréyòl la dous, palé'y toujou !",
    "Bonjou ! Ki jan ou rélé ? Mwen ka rélé Fèfèn !",
]


@router.post("", response_model=ChatResponse, summary="Chatbot Fèfèn")
def chat(request: ChatRequest) -> ChatResponse:
    """Envoie un message au chatbot Fèfèn (stub — Phase 3)."""
    reply_index = len(request.message) % 4
    session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}"
    return ChatResponse(
        reply=_REPLIES[reply_index],
        session_id=session_id,
        model_version="fèfèn-0.1",
    )
