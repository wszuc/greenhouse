from fastapi import APIRouter
from app.core.gpio import led_on, led_off

router = APIRouter()

@router.post("/on")
def turn_on():
    led_on()
    return {"status": "LED ON"}

@router.post("/off")
def turn_off():
    led_off()
    return {"status": "LED OFF"}
