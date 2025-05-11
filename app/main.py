from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.endpoints import led, sensors

app = FastAPI()

app.include_router(led.router, prefix="/led", tags=["LED"])
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])

@app.on_event("startup")
def on_startup():
    init_db()