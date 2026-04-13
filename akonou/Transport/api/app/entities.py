from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BusEntity(Base):
    __tablename__ = "buses"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    immatriculation: Mapped[str] = mapped_column(String(64), nullable=False)
    modele: Mapped[str] = mapped_column(String(64), nullable=False)
    capacite: Mapped[int] = mapped_column(Integer, nullable=False)
    statut: Mapped[str] = mapped_column(String(32), nullable=False)
    line_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    depot: Mapped[str | None] = mapped_column(String(64), nullable=True)


class LineEntity(Base):
    __tablename__ = "lines"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    numero: Mapped[str] = mapped_column(String(16), nullable=False)
    nom: Mapped[str] = mapped_column(String(128), nullable=False)
    couleur: Mapped[str] = mapped_column(String(16), nullable=False)
    direction_aller: Mapped[str] = mapped_column(String(128), nullable=False)
    direction_retour: Mapped[str] = mapped_column(String(128), nullable=False)


class StopEntity(Base):
    __tablename__ = "stops"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    nom: Mapped[str] = mapped_column(String(128), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    line_id: Mapped[str] = mapped_column(String(32), nullable=False)


class AlertEntity(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    bus_id: Mapped[str] = mapped_column(String(32), nullable=False)
    message: Mapped[str] = mapped_column(String(512), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    statut: Mapped[str] = mapped_column(String(32), nullable=False)
