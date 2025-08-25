# Model to reperezntacja tabeli, schema to klasa służąca jako wejście/wyjście w API

from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator
from enum import Enum
from sqlalchemy import JSON

def get_local_datetime():
    return datetime.now().astimezone()

# Event types enum
class EventType(str, Enum):
    WATERING_ON = "watering_on"
    WATERING_OFF = "watering_off"
    HEATING_ON = "heating_on"
    HEATING_OFF = "heating_off"
    LED_ON = "led_on"
    LED_OFF = "led_off"
    FAN_ON = "fan_on"
    FAN_OFF = "fan_off"
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    SENSOR_ERROR = "sensor_error"
    ACTUATOR_ERROR = "actuator_error"
    MANUAL_OVERRIDE = "manual_override"
    SCHEDULED_ACTION = "scheduled_action"

# Event severity levels
class EventSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# absctract base-class
class ConditionsSetBase(SQLModel):
    temp_1: Optional[float] = None
    temp_2: Optional[float] = None
    temp_3: Optional[float] = None
    humidity: Optional[float] = None
    soil_humidity: Optional[float] = None
    lighting: Optional[float] = None
    date: datetime = Field(default_factory=get_local_datetime)

# real table in db
class ConditionsSet(ConditionsSetBase, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    uid: str

# create operation in db schema
class ConditionsSetCreate(ConditionsSetBase):
    uid: str

# get operation in db
class ConditonsSetPublic(ConditionsSetBase):
    id: int
    uid: str

# System Events Table
class SystemEventBase(SQLModel):
    event_type: EventType
    severity: EventSeverity = EventSeverity.INFO
    description: str
    details: Optional[dict] = Field(default=None, sa_column=JSON)
    actuator_id: Optional[str] = None  # Which actuator was affected
    sensor_values: Optional[dict] = Field(default=None, sa_column=JSON)  # Sensor readings at time of event
    user_id: Optional[str] = None  # Who triggered the event (if manual)
    date: datetime = Field(default_factory=get_local_datetime)

class SystemEvent(SystemEventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str

class SystemEventCreate(SystemEventBase):
    uid: str

class SystemEventPublic(SystemEventBase):
    id: int
    uid: str