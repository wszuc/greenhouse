from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


def get_local_datetime():
    return datetime.now().astimezone()


# === CONDITIONS SET ===
class ConditionsSetBase(SQLModel):
    temp_1: Optional[float] = None
    temp_2: Optional[float] = None
    temp_3: Optional[float] = None
    humidity: Optional[float] = None
    soil_humidity: Optional[float] = None
    lighting: Optional[float] = None
    date: datetime = Field(default_factory=get_local_datetime)


class ConditionsSet(ConditionsSetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str
    synced: bool = Field(default=False, nullable=False)  # tylko dla lokalnego użytku


class ConditionsSetCreate(ConditionsSetBase):
    uid: str


class ConditionsSetPublic(ConditionsSetBase):
    id: int
    uid: str


# === EVENT SET ===
class EventBase(SQLModel):
    info: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=get_local_datetime)


class EventSet(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str
    synced: bool = Field(default=False, nullable=False)  # tylko dla lokalnego użytku


class EventCreate(EventBase):
    uid: str


class EventPublic(EventBase):
    id: int
    uid: str

# === DESIRED CLIMATE ===
class DesiredClimateBase(SQLModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soil_humidity: Optional[int] = None
    lighting: Optional[int] = None
    date: datetime = Field(default_factory=get_local_datetime)


class DesiredClimate(DesiredClimateBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str 


class DesiredClimateCreate(DesiredClimateBase):
    uid: str


class DesiredClimatePublic(DesiredClimateBase):
    id: int
    uid: str
