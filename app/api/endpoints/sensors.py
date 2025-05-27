# Endpoints returning actual conditons in the greenhouse. Return n last records from conditionsset table.
from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, select
from app.db.models import ConditionsSet, ConditonsSetPublic
from app.db.session import engine
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.get("/read/")
def read_live_conditions():
    temperature = gpio.get_temperature()
    ht_data = gpio.get_humidity_and_temperature()

    if temperature is None or ht_data is None:
        raise HTTPException(status_code=500, detail="Błąd odczytu z czujników")

    return JSONResponse(content={
        "temperature_ds18b20": temperature,
        "temperature_aht20": ht_data["temperature"],
        "humidity": ht_data["humidity"]
    })
    

@router.get("/from_db/", response_model=list[ConditonsSetPublic])
def get_values(limit: int = 1):
    with Session(engine) as session:
        values = session.exec(select(ConditionsSet).order_by(ConditionsSet.id.desc()).limit(limit)).all()
        return values