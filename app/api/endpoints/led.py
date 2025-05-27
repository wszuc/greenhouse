# Set of endpoints mainly for testing purposes - turning LED on and off

from fastapi import APIRouter
from app.core.gpio import GPIO

router = APIRouter()
gpio = GPIO()

@router.post("/on")
def turn_on():
    gpio.led_on()
    return {"status": "LED ON"}

@router.post("/off")
def turn_off():
    gpio.led_off()
    return {"status": "LED OFF"}
