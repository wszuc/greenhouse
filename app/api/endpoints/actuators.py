from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import Optional, List

from app.core.gpio import GPIO
from app.db.models import EventSet, EventPublic
from app.db.session import engine

router = APIRouter()
gpio = GPIO()


@router.post("/watering-on")
def watering_on() -> dict[str, str]:
    gpio.watering_on()
    return {"status": "Watering is ON"}

@router.post("/watering-off")
def watering_off() -> dict[str, str]:
    gpio.watering_off()
    return {"status": "Watering is OFF"}

@router.post("/heating-on")
def heating_on() -> dict[str, str]:
    gpio.heating_on()
    return {"status": "Heating is ON"}

@router.post("/heating-off")
def heating_off() -> dict[str, str]:
    gpio.heating_off()
    return {"status": "Heating is OFF"}

@router.post("/led-strip-on")
def led_strip_on() -> dict[str, str]:
    gpio.led_strip_on()
    return {"status": "LED strip is ON (white)"}


@router.post("/led-strip-off")
def led_strip_off() -> dict[str, str]:
    gpio.led_strip_off()
    return {"status": "LED strip is OFF"}

@router.post("/roof-open")
def roof_open() -> dict[str, str]:
    try:
        gpio.roof_open()
        return {"status": "Roof is OPEN"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/roof-close")
def roof_close() -> dict[str, str]:
    try:
        gpio.roof_close()
        return {"status": "Roof is CLOSED"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/", response_model=List[EventPublic])
def get_events(
    limit: int = 50,
    uid: Optional[str] = None
) -> List[EventPublic]:
    with Session(engine) as session:
        query = select(EventSet).order_by(EventSet.id.desc())

        if uid:
            query = query.where(EventSet.uid == uid)

        events = session.exec(query.limit(limit)).all()
        return events
