from gpiozero import LED 
from typing import Optional,  Dict
import w1thermsensor
from app.external_libs import DFRobot_AHT20

led = LED(17)
relay_1 = LED(27)
sensor = w1thermsensor.W1ThermSensor()
aht20 = DFRobot_AHT20()
aht20.begin()
aht20.reset()

def led_on() -> Optional[int]:
    try:
        led.on()
        return 0
    except RuntimeError as error:
        print("Error during operation led.on(): ", error)
        return None

def led_off() -> Optional[int]:
    try:
        led.off()
        return 0
    except RuntimeError as error:
        print("Error during operation led.off(): ", error)
        return None
    
def heater_on() -> Optional[int]:
    try:
        relay_1.on()
        return 0
    except RuntimeError as error:
        print("Relay 1 coudln't be turned on: ", error)
        return None
    
def heater_off() -> Optional[int]:
    try:
        relay_1.off()
        return 0
    except RuntimeError as error:
        print("Relay 1 coudln't be turned off: ", error)
        return None
    
def get_temperature() -> Optional[int]:
    try:
        temp = sensor.get_temperature()
        return temp
    except RuntimeError as error:
        print("Error while reading temperature from temp. sensor: ", error)

def get_humidity_and_temperature() -> Optional[Dict[str, float]]: 
    try:
        temperature = aht20.get_temperature_C()
        humidity = aht20.get_humidity_RH()
        return {
            temperature: temperature,
            humidity: humidity
        }
    except RuntimeError as e:
        print(f"Blad odczytu z czujnika DHT11: {e}")
        return None