import time
from datetime import datetime
from sqlmodel import Session
from app.db.session import engine
from app.db.models import ConditionsSet
from app.db.init_db import init_db
from app.core.gpio import GPIO

def main():
    try:
        print("[INIT] Inicjalizacja bazy danych i GPIO...")
        init_db()
        gpio = GPIO()

        # Pobierz temperatury z czujników 1-Wire
        temperatures = gpio.get_temperatures() if hasattr(gpio, "get_temperatures") else {}
        temp_values = list(temperatures.values()) if temperatures else []

        temp_1 = temp_values[0] if len(temp_values) > 0 else 0.0
        temp_2 = temp_values[1] if len(temp_values) > 1 else 0.0

        # Odczytaj dane z AHT20 (temperatura i wilgotność)
        ht_data = gpio.get_humidity_and_temperature()
        temp_3 = ht_data.get("temperature", 0.0) if ht_data else 0.0
        humidity = ht_data.get("humidity", 0.0) if ht_data else 0.0

        # Czujniki analogowe
        soil_humidity = gpio.get_soil_humidity() or 0.0
        lighting = gpio.get_lighting() or 0.0

        # Logowanie wyników
        print(f"[LOG] Temp_1: {temp_1:.2f}°C | Temp_2: {temp_2:.2f}°C | Temp_3(AHT): {temp_3:.2f}°C")
        print(f"[LOG] Wilgotność: {humidity:.2f}% | Gleba: {soil_humidity:.2f}V | Oświetlenie: {lighting:.2f}V")

        # Zapis danych do bazy
        with Session(engine) as session:
            new_entry = ConditionsSet(
                uid="raspberry",
                date=datetime.now().astimezone(),
                temp_1=temp_1,
                temp_2=temp_2,
                temp_3=temp_3,
                humidity=humidity,
                soil_humidity=soil_humidity,
                lighting=lighting,
            )
            session.add(new_entry)
            session.commit()

        print("[SUCCESS] Dane zostały zapisane w bazie danych.\n")

    except Exception as e:
        print(f"[ERROR] Błąd podczas odczytu lub zapisu: {e}")
        exit(-1)


if __name__ == "__main__":
    main()
