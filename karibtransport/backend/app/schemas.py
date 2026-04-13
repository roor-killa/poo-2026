from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Stop schemas ──────────────────────────────────────────────────────────────

class StopBase(BaseModel):
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    description: Optional[str] = None


class StopCreate(StopBase):
    pass


class StopUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None


class StopRead(StopBase):
    id: int

    class Config:
        from_attributes = True


# ── Vehicle schemas ───────────────────────────────────────────────────────────

class VehicleBase(BaseModel):
    license_plate: str
    vehicle_type: str = "bus"
    capacity: int = Field(20, gt=0)
    is_active: bool = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class GPSUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed: Optional[float] = Field(None, ge=0)
    heading: Optional[float] = Field(None, ge=0, le=360)


class VehicleRead(VehicleBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True
