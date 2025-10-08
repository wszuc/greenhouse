# Endpoints returning actual conditons in the greenhouse. Return n last records from conditionsset table.
from datetime import datetime
import json
import subprocess
from fastapi import FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, select
from app.db.models import ConditionsSet, ConditonsSetPublic
from app.db.session import engine
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.get("/read/", response_model=list[ConditonsSetPublic])
def read_live_conditions():
    # Get sensor readings with fallback to default values
    temperatures = gpio.get_temperatures()
    ht_data = gpio.get_humidity_and_temperature()
    soil_humidity = gpio.get_soil_humidity()
    lighting = gpio.get_lighting()

    temp_values = list(temperatures.values()) if temperatures else []
    temp_1 = temp_values[0] if len(temp_values) > 0 and temp_values[0] is not None else 0.0
    temp_2 = temp_values[1] if len(temp_values) > 1 and temp_values[1] is not None else 0.0

    if temperatures is None and ht_data is None:
        raise HTTPException(status_code=500, detail="Błąd odczytu z czujników")

    return [{
        "id": 0,
        "uid": "raspberry",
        "temp_1": temp_1,
        "temp_2": ht_data["temperature"],
        "temp_3": temp_2,
        "humidity": ht_data["humidity"],
        "soil_humidity": soil_humidity,
        "lighting": lighting,
        "date": datetime.now().astimezone()
    }]
    

@router.get("/from_db/", response_model=list[ConditonsSetPublic])
def get_values(limit: int = 1):
    with Session(engine) as session:
        values = session.exec(select(ConditionsSet).order_by(ConditionsSet.id.desc()).limit(limit)).all()
        return values


