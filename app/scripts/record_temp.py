import time
from sqlmodel import Session
from gpiozero import LED
from w1thermsensor import W1ThermSensor
from app.db.session import engine
from app.db.models import ConditionsSet
from app.db.init_db import init_db

def read_temperature() -> float:
    sensor = W1ThermSensor()
    return sensor.get_temperature()

def main():
    init_db()
    while True:
        try:
            temp = read_temperature()
            print(f"[LOG] Aktualna temperatura: {temp:.2f} °C")

            with Session(engine) as session:
                new_entry = ConditionsSet(
                    temp_1=temp,
                    temp_2=0.0,  
                    temp_3=0.0,
                    humidity=0.0,  
                    lighting=0.0,
                    comment="record_temp script",
                    uid="raspberry"
                )
                session.add(new_entry)
                session.commit()
                print("[LOG] Zapisano dane do bazy.\n")

        except Exception as e:
            print(f"[ERROR] Błąd podczas odczytu/zapisu: {e}")

        time.sleep(10)  

if __name__ == "__main__":
    main()
