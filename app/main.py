from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.endpoints import led, sensors, actuators

app = FastAPI()

app.include_router(led.router, prefix="/led", tags=["LED"])
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(actuators.router, prefix="/actuators", tags=["Actuators"])

@app.on_event("startup")
def on_startup():
    init_db()