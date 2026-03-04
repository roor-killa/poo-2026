from fastapi import Header, HTTPException, Query

from .config import settings


def require_api_key(x_api_key: str = Header(...)) -> str:
    """Vérifie l'en-tête X-API-Key."""
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return x_api_key


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Numéro de page"),
        limit: int = Query(default=20, ge=1, le=100, description="Résultats par page"),
    ):
        self.page = page
        self.limit = limit

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
