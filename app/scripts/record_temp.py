import requests
from datetime import datetime
from sqlmodel import Session
from app.db.session import engine
from app.db.models import ConditionsSet
from app.db.init_db import init_db

API_URL = "http://127.0.0.1:8000/sensors/read/"  

try:
    init_db()
    response = requests.get(API_URL, timeout=5)

    if response.status_code != 200:
        raise Exception(f"Niepoprawny kod odpowiedzi: {response.status_code}")

    data = response.json()
    if not data or not isinstance(data, list):
        raise Exception("API response in invalid format")

    readings = data[0]

    print("Data received: ")
    print(f"Temp_1 (ambient): {readings['temp_1']:.2f}°C")
    print(f"Temp_2 (heater): {readings['temp_2']:.2f}°C")
    print(f"Temp_3 (AHT): {readings['temp_3']:.2f}°C")
    print(f"Humidity: {readings['humidity']:.2f}%")
    print(f"Soil humidity: {readings['soil_humidity']:.2f}V")
    print(f"Oświetlenie: {readings['lighting']:.2f}V")

    with Session(engine) as session:
        new_entry = ConditionsSet(
            uid="raspberry",
            date=datetime.now().astimezone(),
            temp_1=readings["temp_1"],
            temp_2=readings["temp_2"],
            temp_3=readings["temp_3"],
            humidity=readings["humidity"],
            soil_humidity=readings["soil_humidity"],
            lighting=readings["lighting"],
        )
        session.add(new_entry)
        session.commit()

    print("Data succesfully saved in db\n")

except requests.exceptions.ConnectionError:
    print(f"Cannot connect to server")
    exit(-1)
except Exception as e:
    print(f"Read/write operation failed: {e}")
    exit(-1)