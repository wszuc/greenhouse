from gpiozero import LED
from typing import Optional,  Dict
import w1thermsensor

led = LED(17)
sensor = w1thermsensor.W1ThermSensor()


def led_on() -> Optional[int]:
    try:
        led.on()
        return 0
    except RuntimeError as error:
        print("Blad operacji led.on(): ", error)
        return None

def led_off() -> Optional[int]:
    try:
        led.off()
        return 0
    except RuntimeError as error:
        print("Blad operacji led.off(): ", error)
        return None

def get_temperature() -> Optional[int]:
    try:
        temp = sensor.get_temperature()
        return temp
    except RuntimeError as error:
        print("Blad opercaji get_temperature() - odczytu z czujnika temperatury: ", error)

def get_humidity_and_temperature() -> Optional[Dict[str, float]]: 
    try:
        temperature: Optional[float] = 0.0
        humidity: Optional[float] = 0.0
        
        if temperature is None or humidity is None:
            raise RuntimeError("Brak odczytu z czujnika")
        return {
            "temperature": temperature,
            "humidity": humidity
        }
    except RuntimeError as e:
        print(f"Blad odczytu z czujnika DHT11: {e}")
        return None