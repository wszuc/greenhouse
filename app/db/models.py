from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

def get_local_datetime():
    return datetime.now().astimezone()

# absctract base-class
class ConditionsSetBase(SQLModel):
    temp_1: float = None
    temp_2: Optional[float] = None
    temp_3: Optional[float] = None
    humidity: float = Field(default=0, ge=0)  
    lighting: float = Field(default=0, ge=0)
    date: datetime = Field(default_factory=get_local_datetime)
    comment: Optional[str] = None

# real table in db
class ConditionsSet(ConditionsSetBase, table=True):
    id: int = Field(primary_key=True)
    uid: str
