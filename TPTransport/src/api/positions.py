"""POST /api/v1/positions — bus-client ingest endpoint (spec §3.1)."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, status

from src.api.deps import SessionDep
from src.schemas.position import PositionCreate, PositionResponse
from src.services.position_service import AuthError, PositionService

router = APIRouter(prefix="/api/v1", tags=["positions"])


@router.post(
    "/positions",
    response_model=PositionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a GPS position from an embedded bus client",
)
async def ingest_position(
    payload: PositionCreate,
    session: SessionDep,
    authorization: str = Header(..., description="Bearer <api_token>"),
) -> PositionResponse:
    """Authenticated endpoint for embedded bus clients.

    - **401** — token missing or inactive.
    - **422** — payload validation failure (FastAPI default).
    - **429** — rate-limited (enforced by nginx / slowapi upstream).
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '",
        )
    token = authorization.removeprefix("Bearer ").strip()

    try:
        result = await PositionService(session).ingest(token, payload)
        await session.commit()
        return result
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
