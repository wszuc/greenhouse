import time
from sqlmodel import Session
from app.db.session import engine
from app.db.models import ConditionsSet
from app.db.init_db import init_db
from app.core.gpio import GPIO


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
        exit(0)

except Exception as e:
    print(f"[ERROR] Błąd podczas odczytu/zapisu: {e}")
    exit(-1)





