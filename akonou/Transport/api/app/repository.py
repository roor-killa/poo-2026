from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .entities import AlertEntity, BusEntity, LineEntity, StopEntity
from .models import Alert
from .store import store


def seed_reference_data(db: Session) -> None:
    has_buses = db.scalar(select(func.count()).select_from(BusEntity))
    if has_buses and has_buses > 0:
        return

    for bus in store.buses.values():
        db.add(
            BusEntity(
                id=bus.id,
                immatriculation=bus.immatriculation,
                modele=bus.modele,
                capacite=bus.capacite,
                statut=bus.statut.value,
                line_id=bus.line_id,
                depot=bus.depot,
            )
        )

    for line in store.lines.values():
        db.add(
            LineEntity(
                id=line.id,
                numero=line.numero,
                nom=line.nom,
                couleur=line.couleur,
                direction_aller=line.direction_aller,
                direction_retour=line.direction_retour,
            )
        )

    for stop in store.stops.values():
        db.add(
            StopEntity(
                id=stop.id,
                nom=stop.nom,
                latitude=stop.latitude,
                longitude=stop.longitude,
                line_id=stop.line_id,
            )
        )

    db.commit()


def persist_alert(db: Session, alert: Alert) -> None:
    db.merge(
        AlertEntity(
            id=alert.id,
            type=alert.type,
            bus_id=alert.bus_id,
            message=alert.message,
            timestamp=alert.timestamp,
            statut=alert.statut.value,
        )
    )
    db.commit()


def count_open_alerts(db: Session) -> int:
    total = db.scalar(
        select(func.count()).select_from(AlertEntity).where(AlertEntity.statut == "open")
    )
    return int(total or 0)
