# Model to reperezntacja tabeli, schema to klasa służąca jako wejście/wyjście w API

from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator
from enum import Enum
from sqlalchemy import JSON, Column

def get_local_datetime():
    return datetime.now().astimezone()

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

class EventBase(SQLModel):
    info: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=get_local_datetime)


class EventSet(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str


class EventCreate(EventBase):
    uid: str


class EventPublic(EventBase):
    id: int
    uid: str