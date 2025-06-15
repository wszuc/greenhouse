from os import system
from gpiozero import LED 
from typing import Optional, Dict
import w1thermsensor
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
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
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D25)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
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
        
    def watering_on(self) -> Optional[int]:
        try:
            self.relay_1.on()
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned on: ", error)
            return None
        
    def watering_off(self) -> Optional[int]:
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
            if self.aht20.start_measurement_ready(crc_en = True):
                temperature = self.aht20.get_temperature_C()
                humidity = self.aht20.get_humidity_RH()
                return {
                    "temperature": temperature,
                    "humidity": humidity
                }
        except RuntimeError as e:
            print(f"Błąd odczytu z czujnika AHT20: {e}")
            return None

    def get_soil_humidity(self) -> Optional[float]: 
        try:
            humidity_voltage = AnalogIn(self.mcp, MCP.P0).voltage
            return humidity_voltage
        except RuntimeError as e:
            print(f"Błąd odczytu z czujnika wilgotności gleby: {e}")
            return None
        
    def get_lighting(self) -> Optional[float]: 
        try:
            light_voltage = AnalogIn(self.mcp, MCP.P1).voltage
            return light_voltage
        except RuntimeError as e:
            print(f"Błąd odczytu z fotorezystora: {e}")
            return None
