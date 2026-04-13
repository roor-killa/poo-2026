from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from db.database import get_db
from db.models import PushSubscriptionDB
from api.schemas import PushSubscriptionCreate
from core.config import settings
import json
import logging

try:
    from pywebpush import webpush, WebPushException
    WEBPUSH_AVAILABLE = True
except ImportError:
    WEBPUSH_AVAILABLE = False

router = APIRouter(prefix="/api/notifications", tags=["Notifications Push"])
logger = logging.getLogger(__name__)


@router.get("/vapid-public-key")
async def get_vapid_public_key():
    """Retourne la clé publique VAPID pour l'abonnement côté client."""
    if not settings.VAPID_PUBLIC_KEY:
        raise HTTPException(status_code=503, detail="VAPID non configuré")
    return {"public_key": settings.VAPID_PUBLIC_KEY}


@router.post("/subscribe", status_code=201)
async def subscribe(payload: PushSubscriptionCreate, db: AsyncSession = Depends(get_db)):
    """Enregistre un abonnement push navigateur."""
    # Vérifier si déjà abonné
    result = await db.execute(
        select(PushSubscriptionDB).where(PushSubscriptionDB.endpoint == payload.endpoint)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return {"message": "Déjà abonné", "id": existing.id}

    sub = PushSubscriptionDB(
        endpoint=payload.endpoint,
        p256dh=payload.p256dh,
        auth=payload.auth,
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    logger.info(f"[Push] Nouveau abonnement #{sub.id}")
    return {"message": "Abonnement enregistré", "id": sub.id}


@router.delete("/unsubscribe")
async def unsubscribe(endpoint: str, db: AsyncSession = Depends(get_db)):
    """Supprime un abonnement push."""
    await db.execute(
        delete(PushSubscriptionDB).where(PushSubscriptionDB.endpoint == endpoint)
    )
    await db.commit()
    return {"message": "Désabonnement effectué"}


async def envoyer_notification(db: AsyncSession, titre: str, corps: str, url: str = "/") -> int:
    """
    Utilitaire interne — envoie une notification push à tous les abonnés.
    Retourne le nombre de notifications envoyées avec succès.
    """
    if not WEBPUSH_AVAILABLE or not settings.VAPID_PRIVATE_KEY:
        logger.warning("[Push] Web Push non disponible (VAPID non configuré).")
        return 0

    result = await db.execute(select(PushSubscriptionDB))
    abonnes = result.scalars().all()
    success = 0

    for abonne in abonnes:
        try:
            webpush(
                subscription_info={
                    "endpoint": abonne.endpoint,
                    "keys": {"p256dh": abonne.p256dh, "auth": abonne.auth},
                },
                data=json.dumps({"title": titre, "body": corps, "url": url}),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": settings.VAPID_EMAIL},
            )
            success += 1
        except WebPushException as e:
            logger.error(f"[Push] Échec envoi abonné #{abonne.id}: {e}")
            # Abonnement expiré → supprimer
            if e.response and e.response.status_code in (404, 410):
                await db.delete(abonne)
                await db.commit()

    return success
