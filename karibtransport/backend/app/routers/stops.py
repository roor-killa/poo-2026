from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Stop
from ..schemas import StopCreate, StopRead, StopUpdate

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/", response_model=List[StopRead])
def list_stops(db: Session = Depends(get_db)):
    return db.query(Stop).all()


@router.get("/{stop_id}", response_model=StopRead)
def get_stop(stop_id: int, db: Session = Depends(get_db)):
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")
    return stop


@router.post("/", response_model=StopRead, status_code=status.HTTP_201_CREATED)
def create_stop(payload: StopCreate, db: Session = Depends(get_db)):
    stop = Stop(**payload.model_dump())
    db.add(stop)
    db.commit()
    db.refresh(stop)
    return stop


@router.put("/{stop_id}", response_model=StopRead)
def update_stop(stop_id: int, payload: StopUpdate, db: Session = Depends(get_db)):
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(stop, field, value)
    db.commit()
    db.refresh(stop)
    return stop


@router.delete("/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stop(stop_id: int, db: Session = Depends(get_db)):
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")
    db.delete(stop)
    db.commit()
