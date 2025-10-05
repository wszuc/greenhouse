# Set of endpoints for steering actuators

from fastapi import APIRouter
from sqlmodel import Session, select
from app.core.gpio import GPIO
from app.db.models import SystemEvent, SystemEventPublic
from app.db.session import engine

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

@router.post("/led-strip-on")
def led_strip_on():
    gpio.led_strip_on()
    return {"status": "LED strip is ON (white)"}

@router.post("/led-strip-off")
def led_strip_off():
    gpio.led_strip_off()
    return {"status": "LED strip is OFF"}

@router.post("/roof-open")
def roof_open():
    try:
        gpio.roof_open()
        return {"status": f"Servo set to OPEN"}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/roof-close")
def roof_close():
    try:
        gpio.roof_close()
        return {"status": f"Servo set to CLOSE"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/events/", response_model=list[SystemEventPublic])
def get_system_events(
    limit: int = 50,
    event_type: str = None,
    severity: str = None,
    actuator_id: str = None
):
    """
    Get system events with optional filtering.
    
    Args:
        limit: Maximum number of events to return (default: 50)
        event_type: Filter by event type (e.g., "watering_on", "led_on")
        severity: Filter by severity level (e.g., "info", "warning", "error")
        actuator_id: Filter by specific actuator (e.g., "relay_gpio27")
    """
    with Session(engine) as session:
        query = select(SystemEvent).order_by(SystemEvent.id.desc())
        
        if event_type:
            query = query.where(SystemEvent.event_type == event_type)
        if severity:
            query = query.where(SystemEvent.severity == severity)
        if actuator_id:
            query = query.where(SystemEvent.actuator_id == actuator_id)
            
        events = session.exec(query.limit(limit)).all()
        return events
