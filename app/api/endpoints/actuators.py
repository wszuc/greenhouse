# Set of endpoints for steering actuators

from fastapi import APIRouter
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.post("/watering-on")
def turn_on():
    gpio.watering_on()
    return {"status": "Watering is ON"}

@router.post("/watering-off")
def turn_off():
    gpio.watering_off()
    return {"status": "Watering is OFF"}
