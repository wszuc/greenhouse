from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from gpiozero import LED
import w1thermsensor


app = FastAPI()

mocked_readings = {"temperature": 22.3, "humidity": 66, "lighting": 44}

class ConditionsSetBase(SQLModel):
    temperature: float | None = None
    humidity: float | None = None
    lighting: float | None = None
    comment: str | None = None

class ConditionsSet(ConditionsSetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_key: str

class ConditionsSetPublic(ConditionsSetBase):
    id: int

class ConditionsSetCreate(ConditionsSetBase):
    secret_key: str  # Usunięto `Field(default=None)` aby pole było wymagane

class ConditionsSetUpdate(ConditionsSetBase):
    secret_key: str | None = None  # Opcjonalne dla aktualizacji

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}" 

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/set_conditions/", response_model=ConditionsSetPublic)
async def set_conditions(new_conditions: ConditionsSetCreate, session: SessionDep):
    db_conditions = ConditionsSet.model_validate(new_conditions)
    session.add(db_conditions)
    session.commit()
    session.refresh(db_conditions)
    return db_conditions

@app.patch("/update_conditions/{conditions_set_id}", response_model=ConditionsSetPublic)
async def update_conditions(conditions_set_id: int, updated_conditions: ConditionsSet, session: SessionDep):
    db_conditions = session.get(ConditionsSet, conditions_set_id)
    if not db_conditions:
        raise HTTPException(status_code=404, detail="No object found!")
    received_data = updated_conditions.model_dump(exclude_unset=True)
    db_conditions.sqlmodel_update(received_data)
    session.add(db_conditions)
    session.commit()
    session.refresh(db_conditions)
    return db_conditions

@app.get("/get_conditions/", response_model=list[ConditionsSetPublic])
async def get_conditions(session: SessionDep) -> list[ConditionsSet]:
    conditions_sets = session.exec(select(ConditionsSet)).all()
    return conditions_sets

# Tworzymy globalny obiekt LED                                              
led = LED(17)

@app.post("/led_on/")
def led_on():                                                               
    led.on()  # Zapal diodę LED                                              
    return {"status": "LED ON"} 

@app.post("/led_off/")
def led_off():                                                                  
    led.off()  # Zgaś diodę LED                                             
    return {"status": "LED OFF"} 

@app.get("/get_temp/")
def get_temp():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    return temp
    