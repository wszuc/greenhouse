import time
from sqlmodel import Session
from app.db.session import engine
from app.db.models import ConditionsSet
from app.db.init_db import init_db
from app.core.gpio import get_humidity_and_temperature, get_temperature

# TODO: Zrób prywatnego endpointa, który striggerowany przez cron joba będzie zapisywał odczyty do bazy danych

def save_to_db():
    try:
        init_db()
        temp = get_temperature()
        print(f"[LOG] Aktualna temperatura z czujnika temperatury: {temp:.2f} °C")

        temp_humid_dict = get_humidity_and_temperature()
        print(f"[LOG] Aktualna temperatura i wilgotnosc: {temp_humid_dict['temperature']}°C i {temp_humid_dict['humidity']}%")


        with Session(engine) as session:
            new_entry = ConditionsSet(
                temp_1=temp,
                temp_2=temp_humid_dict['temperature'],  
                temp_3=0.0,
                humidity=temp_humid_dict['humidity'],  
                lighting=0.0,
                soil_humidity=0.0,
                comment="record_temp script",
                uid="raspberry"
            )
            session.add(new_entry)
            session.commit()
            print("[LOG] Zapisano dane do bazy.\n")
            return 0

    except Exception as e:
        print(f"[ERROR] Błąd podczas odczytu/zapisu: {e}")
        return -1