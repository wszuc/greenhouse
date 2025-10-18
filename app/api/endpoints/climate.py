from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from app.db.models import DesiredClimate, DesiredClimateCreate, DesiredClimatePublic
from app.db.session import engine

router = APIRouter()


@router.post("/desired-climate", response_model=DesiredClimatePublic)
def set_desired_climate(data: DesiredClimateCreate):
    try:
        with Session(engine) as session:
            desired = DesiredClimate.from_orm(data)
            session.add(desired)
            session.commit()
            session.refresh(desired)
            return desired
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {e}")
