from os import system
from gpiozero import LED 
from typing import Optional, Dict
import w1thermsensor
from app.external_libs.DFRobot_AHT20 import DFRobot_AHT20



class GPIO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPIO, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return 
        self.led = LED(17)
        self.relay_1 = LED(27)
        self.sensor = w1thermsensor.W1ThermSensor()
        self.aht20 = DFRobot_AHT20()
        while self.aht20.begin() != True:
            print("failed, please check if the connection is correct?")
            system.sleep(1)
            print("Initialization AHT20 Sensor...", end=" ")
        print("Done, AHT initialized")
        self.aht20.reset()
        self._initialized = True

    def led_on(self) -> Optional[int]:
        try:
            self.led.on()
            return 0
        except RuntimeError as error:
            print("Error during operation led.on(): ", error)
            return None

    def led_off(self) -> Optional[int]:
        try:
            self.led.off()
            return 0
        except RuntimeError as error:
            print("Error during operation led.off(): ", error)
            return None
        
    def heater_on(self) -> Optional[int]:
        try:
            self.relay_1.on()
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned on: ", error)
            return None
        
    def heater_off(self) -> Optional[int]:
        try:
            self.relay_1.off()
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            return None
        
    def get_temperature(self) -> Optional[float]:
        try:
            temp = self.sensor.get_temperature()
            return temp
        except RuntimeError as error:
            print("Error while reading temperature from temp. sensor: ", error)
            return None

    def get_humidity_and_temperature(self) -> Optional[Dict[str, float]]: 
        try:
            temperature = self.aht20.get_temperature_C()
            humidity = self.aht20.get_humidity_RH()
            return {
                "temperature": temperature,
                "humidity": humidity
            }
        except RuntimeError as e:
            print(f"Błąd odczytu z czujnika AHT20: {e}")
            return None
