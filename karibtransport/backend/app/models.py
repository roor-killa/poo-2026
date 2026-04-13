from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)  # e.g. "T1", "N1"
    name = Column(String, nullable=False)
    color = Column(String, nullable=False, default="#3b82f6")       # hex color

    vehicles = relationship("Vehicle", back_populates="line")

    def __repr__(self):
        return f"<Line id={self.id} code={self.code}>"


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Stop id={self.id} name={self.name}>"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False, index=True)
    vehicle_type = Column(String, nullable=False, default="bus")  # bus, minibus, taxi
    capacity = Column(Integer, nullable=False, default=20)
    is_active = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)    # km/h
    heading = Column(Float, nullable=True)  # degrees 0-360
    last_seen = Column(DateTime, nullable=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)

    line = relationship("Line", back_populates="vehicles")

    def __repr__(self):
        return f"<Vehicle id={self.id} plate={self.license_plate}>"
