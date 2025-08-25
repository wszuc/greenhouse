import time
from sqlmodel import Session
from app.db.session import engine
from app.db.models import ConditionsSet, SystemEvent, EventType, EventSeverity
from app.db.init_db import init_db
from app.core.gpio import GPIO

# TODO: Zrób prywatnego endpointa, który striggerowany przez cron joba będzie zapisywał odczyty do bazy danych

def save_to_db():
    try:
        init_db()
        gpio = GPIO()
        
        temp = gpio.get_temperature()
        print(f"[LOG] Aktualna temperatura z czujnika temperatury: {temp:.2f} °C")

        temp_humid_dict = gpio.get_humidity_and_temperature()
        print(f"[LOG] Aktualna temperatura i wilgotnosc: {temp_humid_dict['temperature']}°C i {temp_humid_dict['humidity']}%")

        soil_humidity = gpio.get_soil_humidity()
        lighting = gpio.get_lighting()
        print(f"[LOG] Wilgotnosc gleby: {soil_humidity:.2f}V, Oswietlenie: {lighting:.2f}V")

        with Session(engine) as session:
            new_entry = ConditionsSet(
                temp_1=temp,
                temp_2=temp_humid_dict['temperature'],  
                temp_3=0.0,
                humidity=temp_humid_dict['humidity'],  
                lighting=lighting,
                soil_humidity=soil_humidity,
                uid="raspberry"
            )
            session.add(new_entry)
            session.commit()
            print("[LOG] Zapisano dane do bazy.\n")
            return 0

    except Exception as e:
        print(f"[ERROR] Błąd podczas odczytu/zapisu: {e}")
        return -1

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
        
        with Session(engine) as session:
            new_event = SystemEvent(
                event_type=event_type,
                severity=severity,
                description=description,
                details=details,
                actuator_id=actuator_id,
                sensor_values=sensor_values,
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