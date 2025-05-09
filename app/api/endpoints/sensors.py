from fastapi import APIRouter
import w1thermsensor

router = APIRouter()

@router.get("/temperature")
def get_temperature():
    sensor = w1thermsensor.W1ThermSensor()
    return {"temp": sensor.get_temperature()}
