# Endpoints returning actual conditons in the greenhouse. Return n last records from conditionsset table.
from fastapi import FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, select
from app.db.models import ConditionsSet, ConditonsSetPublic
from app.db.session import engine

router = APIRouter()

@router.get("/all/", response_model=list[ConditonsSetPublic])
def get_values(limit: int = 1):
    with Session(engine) as session:
        values = session.exec(select(ConditionsSet).order_by(ConditionsSet.id.desc()).limit(limit)).all()
        return values
    
    
