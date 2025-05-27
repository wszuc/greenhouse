# Set of endpoints for steering actuators

from fastapi import APIRouter
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.post("/heater-on")
def turn_on():
    gpio.heater_on()
    return {"status": "HEATER ON"}

@router.post("/heater-off")
def turn_off():
    gpio.heater_off()
    return {"status": "HEATER OFF"}
