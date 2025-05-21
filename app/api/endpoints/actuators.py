# Set of endpoints for steering actuators

from fastapi import APIRouter
from app.core.gpio import heater_off, heater_on

router = APIRouter()

@router.post("/heater-on")
def turn_on():
    heater_on()
    return {"status": "LED ON"}

@router.post("/heater-off")
def turn_off():
    heater_off()
    return {"status": "LED OFF"}
