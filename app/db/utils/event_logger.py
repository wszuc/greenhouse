import json
from sqlmodel import Session
from app.db.session import engine
from app.db.models import SystemEvent, EventType, EventSeverity
from app.db.init_db import init_db


def log_system_event(
    event_type: EventType,
    description: str,
    severity: EventSeverity = EventSeverity.INFO,
    details: dict = None,
    actuator_id: str = None,
    sensor_values: dict = None,
    user_id: str = None,
    uid: str = "raspberry"
) -> bool:
    """
    Log a system event to the database.
    
    Args:
        event_type: Type of event (from EventType enum)
        description: Human-readable description of the event
        severity: Event severity level (default: INFO)
        details: Additional JSON data about the event
        actuator_id: ID of the actuator involved (if any)
        sensor_values: Sensor readings at time of event (if any)
        user_id: User who triggered the event (if manual)
        uid: Device identifier (default: "raspberry")
    
    Returns:
        bool: True if event was logged successfully, False otherwise
    """
    try:
        init_db()
        
        # Convert dict to JSON string for database storage
        details_json = json.dumps(details) if details else None
        sensor_values_json = json.dumps(sensor_values) if sensor_values else None
        
        with Session(engine) as session:
            new_event = SystemEvent(
                event_type=event_type,
                severity=severity,
                description=description,
                details=details_json,
                actuator_id=actuator_id,
                sensor_values=sensor_values_json,
                user_id=user_id,
                uid=uid
            )
            session.add(new_event)
            session.commit()
            print(f"[EVENT LOG] {event_type.value}: {description}")
            return True
            
    except Exception as e:
        print(f"[ERROR] Failed to log system event: {e}")
        return False
