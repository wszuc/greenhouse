# Endpoints returning actual conditons in the greenhouse. Return n last records from conditionsset table.
from datetime import datetime
import os
from fastapi import FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, select
from app.db.models import ConditionsSet, ConditonsSetPublic
from app.db.session import engine
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.get("/read/", response_model=list[ConditonsSetPublic])
def read_live_conditions():
    temperature = gpio.get_temperature()
    ht_data = gpio.get_humidity_and_temperature()
    soil_humidity = gpio.get_soil_humidity()
    lighting = gpio.get_lighting()

    if temperature is None or ht_data is None:
        raise HTTPException(status_code=500, detail="Błąd odczytu z czujników")

    return [{
        "id": 0,
        "uid": "raspberry",
        "temp_1": temperature,
        "temp_2": ht_data["temperature"],
        "temp_3": 0.0,
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
    
@router.get("/read_mqqt/")
def read_live_conditions():
    temperature = gpio.get_temperature()
    ht_data = gpio.get_humidity_and_temperature()
    soil_humidity = gpio.get_soil_humidity()
    lighting = gpio.get_lighting()

    if temperature is None or ht_data is None:
        raise HTTPException(status_code=500, detail="Błąd odczytu z czujników")

    readings = {
        "id": 0,
        "uid": "raspberry",
        "temp_1": temperature,
        "temp_2": ht_data["temperature"],
        "temp_3": 0.0,
        "humidity": ht_data["humidity"],
        "soil_humidity": soil_humidity,
        "lighting": lighting,
        "date": datetime.now().astimezone()
    }

    # send data via MQQT to thingsboard

    result = os.system(f'mosquitto_pub -d -q 1 -h demo.thingsboard.io -p 1883 -t v1/devices/me/telemetry -u "eac44v98ye7olt0al0ge" -m "${readings}"')

    return result
    