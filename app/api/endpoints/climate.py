from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from app.db.models import DesiredClimate, DesiredClimateCreate, DesiredClimatePublic
from app.db.session import engine

router = APIRouter()


@router.post("/set-climate", response_model=DesiredClimatePublic)
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
    
@router.get("/get-climate", response_model=DesiredClimatePublic)
def get_last_desired_climate():
    try:
        with Session(engine) as session:
            last_entry = session.query(DesiredClimate).order_by(DesiredClimate.date.desc()).first()
            if not last_entry:
                raise HTTPException(status_code=404, detail="No desired climate data found")
            return last_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {e}")


