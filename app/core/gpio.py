from os import system
from gpiozero import LED, Servo
from typing import Optional, Dict
import w1thermsensor
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import smbus2
import time
from app.db.utils.event_logger import log_system_event
import neopixel


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
        
        # LED testowa
        try:
            self.led = LED(17)
            print("LED initialized successfully")
        except Exception as e:
            print(f"Warning: LED initialization failed: {e}")
            self.led = None
        
        # Pompa (przekaźnik 1)
        try:
            self.relay_1 = LED(19)
            self.relay_1.on()
            print("Relay 1 initialized successfully")
        except Exception as e:
            print(f"Warning: Relay 1 initialization failed: {e}")
            self.relay_1 = None

        # Grzałka (przekaźnik 2)
        try:
            self.relay_2 = LED(27)
            self.relay_2.on()
            print("Relay 2 initialized successfully")
        except Exception as e:
            print(f"Warning: Relay 2 initialization failed: {e}")
            self.relay_2 = None

        # Czujniki DS18B20 (1-Wire)
        try:
            sensors = w1thermsensor.W1ThermSensor.get_available_sensors()
            if sensors:
                self.sensors = sensors
                print(f"Detected {len(self.sensors)} 1-Wire temperature sensors:")
                for s in self.sensors:
                    print(f" - Sensor ID: {s.id}")
            else:
                print("Warning: No 1-Wire temperature sensors detected.")
                self.sensors = []
        except Exception as e:
            print(f"Warning: DS18B20 initialization failed: {e}")
            self.sensors = []

        # AHT20 (I2C)
        try:
            self.I2C_ADDR = 0x38
            self.aht20 = smbus2.SMBus(1)
        except Exception as e:
            print(f"Warning: AHT20 initialization failed: {e}")
            self.aht20 = None

        # MCP3008 (ADC)
        try:
            self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.cs = digitalio.DigitalInOut(board.D25)
            self.mcp = MCP.MCP3008(self.spi, self.cs)
            print("MCP3008 ADC initialized successfully")
        except Exception as e:
            print(f"Warning: MCP3008 ADC initialization failed: {e}")
            self.mcp = None

        # LED strip WS2812B
        try:
            self.led_strip = neopixel.NeoPixel(board.D18, 28, auto_write=True, pixel_order=neopixel.GRB)
            print("LED strip initialized!")
        except Exception as e:
            print("Error initializing LED strip:", e)
            self.led_strip = None

        # Serwo
        try:
            self.servo = Servo(22)
            print("Servo initialized successfully on GPIO22")
        except Exception as e:
            print(f"Warning: Servo initialization failed: {e}")
            self.servo = None

        self._initialized = True

    # --- AKTUATORY ---

    def led_strip_on(self):
        if not self.led_strip:
            print("Warning: LED strip not available")
            return
        try:
            self.led_strip.fill((200, 200, 200))
            log_system_event("LED strip turned ON")
        except Exception as e:
            log_system_event(f"LED strip ON failed: {e}")

    def led_strip_off(self):
        if not self.led_strip:
            print("Warning: LED strip not available")
            return
        try:
            self.led_strip.fill((0, 0, 0))
            log_system_event("LED strip turned OFF")
        except Exception as e:
            log_system_event(f"LED strip OFF failed: {e}")

    def led_on(self):
        if not self.led:
            print("Warning: LED not available")
            return
        try:
            self.led.on()
            log_system_event("LED indicator ON")
        except Exception as e:
            log_system_event(f"LED ON failed: {e}")

    def led_off(self):
        if not self.led:
            print("Warning: LED not available")
            return
        try:
            self.led.off()
            log_system_event("LED indicator OFF")
        except Exception as e:
            log_system_event(f"LED OFF failed: {e}")

    def heating_on(self):
        if not self.relay_2:
            print("Warning: Heater relay not available")
            return
        try:
            self.relay_2.off()
            log_system_event("Heating turned ON")
        except Exception as e:
            log_system_event(f"Heating ON failed: {e}")

    def heating_off(self):
        if not self.relay_2:
            print("Warning: Heater relay not available")
            return
        try:
            self.relay_2.on()
            log_system_event("Heating turned OFF")
        except Exception as e:
            log_system_event(f"Heating OFF failed: {e}")

    def watering_on(self):
        if not self.relay_1:
            print("Warning: Watering relay not available")
            return
        try:
            self.relay_1.off()
            log_system_event("Watering turned ON")
        except Exception as e:
            log_system_event(f"Watering ON failed: {e}")

    def watering_off(self):
        if not self.relay_1:
            print("Warning: Watering relay not available")
            return
        try:
            self.relay_1.on()
            log_system_event("Watering turned OFF")
        except Exception as e:
            log_system_event(f"Watering OFF failed: {e}")

    def roof_open(self):
        if not self.servo:
            print("Warning: Servo not available")
            return
        try:
            self.servo.value = 0
            log_system_event("Roof opened")
        except Exception as e:
            log_system_event(f"Roof open failed: {e}")

    def roof_close(self):
        if not self.servo:
            print("Warning: Servo not available")
            return
        try:
            self.servo.value = 1
            log_system_event("Roof closed")
        except Exception as e:
            log_system_event(f"Roof close failed: {e}")
