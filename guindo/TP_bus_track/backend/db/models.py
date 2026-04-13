from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class LigneDB(Base):
    __tablename__ = "lignes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    couleur = Column(String(7), default="#2E75B6")  # hex color
    description = Column(Text, nullable=True)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    arrets = relationship("ArretDB", back_populates="ligne", order_by="ArretDB.ordre")
    bus = relationship("BusDB", back_populates="ligne")


class ArretDB(Base):
    __tablename__ = "arrets"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    ordre = Column(Integer, nullable=False)  # position dans la ligne
    ligne_id = Column(Integer, ForeignKey("lignes.id"), nullable=False)

    ligne = relationship("LigneDB", back_populates="arrets")


class BusDB(Base):
    __tablename__ = "bus"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)  # ex: "Bus L1-A"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    vitesse = Column(Float, default=40.0)  # km/h
    statut = Column(String(20), default="en_service")  # en_service | a_larret | hors_service
    arret_courant_idx = Column(Integer, default=0)  # index dans la liste d'arrêts
    direction = Column(Integer, default=1)  # 1 = aller, -1 = retour
    ligne_id = Column(Integer, ForeignKey("lignes.id"), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    ligne = relationship("LigneDB", back_populates="bus")


class PositionHistoriqueDB(Base):
    __tablename__ = "positions_historiques"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("bus.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class PushSubscriptionDB(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(Text, nullable=False, unique=True)
    p256dh = Column(Text, nullable=False)
    auth = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
