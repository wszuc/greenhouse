from math import floor
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
        
        # initialize test LED
        try:
            self.led = LED(17)
            print("LED initialized successfully")
        except Exception as e:
            print(f"Warning: LED initialization failed: {e}")
            self.led = None
        
        # initialize atomiser
        try:
            self.atomiser = LED(13)
            print("Atomiser initialized successfully")
        except Exception as e:
            print(f"Warning: Atomiser initialization failed: {e}")
            self.atomiser = None

         # initialize 1st relay (water pump)
        try:
            self.relay_1 = LED(19)
            self.relay_1.on()
            print("Relay initialized successfully")
        except Exception as e:
            print(f"Warning: Relay initialization failed: {e}")
            self.relay_1 = None

        # initialize 2n relay (heater)
        try:
            self.relay_2 = LED(27)
            self.relay_2.on()
            print("Relay initialized successfully")
        except Exception as e:
            print(f"Warning: Relay initialization failed: {e}")
            self.relay_2 = None

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
            print(f"Warning: DS18B20 temperature sensor initialization failed: {e}")
            self.sensors = []

        # Initialize AHT20 
        try:
            self.I2C_ADDR = 0x38
            self.aht20 = smbus2.SMBus(1)

        except Exception as e:
            print(f"Warning: AHT20 sensor initialization failed: {e}")
            self.aht20 = None
        try:

        # Initialize SPI and MCP3008
            self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.cs = digitalio.DigitalInOut(board.D25)
            self.mcp = MCP.MCP3008(self.spi, self.cs)
            print("MCP3008 ADC initialized successfully")
        except Exception as e:
            print(f"Warning: MCP3008 ADC initialization failed: {e}")
            self.mcp = None

        # initialize LED strip WS2812B
        try:
            self.led_strip = neopixel.NeoPixel(board.D18, 28, auto_write=True, pixel_order=neopixel.GRB)
            print("LED strip initialized!")
        except Exception as e:
            print("Error while initializing LED strip: ", e)
            self.led_strip = None

        # init servo
        try:
            self.servo = Servo(22)
            print("Servo initialized successfully on GPIO22")
        except Exception as e:
            print(f"Warning: Servo initialization failed: {e}")
            self.servo = None

        self._initialized = True

    def roof_open(self) -> Optional[int]:
        if self.servo is None:
            print("Warning: Servo not available")
            return None
        try:
            position = max(-1.0, min(1.0, 0))
            self.servo.value = position
            print(f"Servo set to position OPEN")
            log_system_event(
                info="ROOF OPEN"
            )
        except Exception as e:
            print(f"Error while moving servo: {e}")
            log_system_event(
                info="[ERROR] ROOF OPEN"
            )

    def roof_close(self) -> Optional[int]:
        if self.servo is None:
            print("Warning: Servo not available")
            return None
        try:
            position = max(-1.0, min(1.0, 1))
            self.servo.value = position
            print(f"Servo set to position CLOSE")
            log_system_event(
                info="ROOF CLOSE"
            )
        except Exception as e:
            log_system_event(
                info="[ERROR] ROOF CLOSE"
            )
            print(f"Error while moving servo: {e}")

    def led_strip_on(self, brightness) -> Optional[int]:
        if self.led_strip is None:
            print("Warning: LED strip not available")
            return None
        try:
            if brightness == 0:
                self.led_strip_off()
                return 0
            brightness_val = floor(brightness/5*255)
            self.led_strip.fill((brightness_val, brightness_val, brightness_val))

            log_system_event(
                info=f"LED STRIP ON, LEVEL {brightness_val}"
            )
            return 0
        except RuntimeError as error:
            print("Error during LED strip on: ", error)
            log_system_event(
                info="[ERROR] LED STRIP ON"
            )
            return None

    def led_strip_off(self) -> Optional[int]:
        if self.led_strip is None:
            print("Warning: LED strip not available")
            return None
        try:
            self.led_strip.fill((0, 0, 0))  # zgaszony
            # Log the event
            log_system_event(
                info="LED STRIP OFF"
            )
            return 0
        except RuntimeError as error:
            print("Error during LED strip off: ", error)
            log_system_event(
                info="[ERROR] LED STRIP OFF"
            )
            return None

    def led_on(self) -> Optional[int]:
        if self.led is None:
            print("Warning: LED not available")
            return None
        try:
            self.led.on()
            log_system_event(
                info="LED ON"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation led.on(): ", error)
            log_system_event(
                info="[ERROR] LED ON"
            )
            return None

    def led_off(self) -> Optional[int]:
        if self.led is None:
            print("Warning: LED not available")
            return None
        try:
            self.led.off()
            # Log the event
            log_system_event(
                info="LED OFF"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation led.off(): ", error)
            # Log the error
            log_system_event(
                info="[ERROR] LED OFF"
            )
            return None
        
    def atomiser_on(self) -> Optional[int]:
        if self.atomiser is None:
            print("Warning: Atomiser not available")
            return None
        try:
            self.atomiser.on()
            log_system_event(
                info="ATOMISER ON"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation atomiser.on(): ", error)
            log_system_event(
                info="[ERROR] ATOMISER ON"
            )
            return None
        
    def atomiser_off(self) -> Optional[int]:
        if self.atomiser is None:
            print("Warning: Atomiser not available")
            return None
        try:
            self.atomiser.off()
            log_system_event(
                info="ATOMISER OFF"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation atomiser.off(): ", error)
            log_system_event(
                info="[ERROR] ATOMISER OFF"
            )
            return None
            
    def heating_off(self) -> Optional[int]:
        if self.relay_2 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_2.on()
            # Log the event
            log_system_event(
                info="HEATING OFF"
            )
            return 0
        except RuntimeError as error:
            print("Relay 2 couldn't be turned on: ", error)
            # Log the error
            log_system_event(
                info="[ERROR] HEATING OFF"
            )
            return None
        
    def heating_on(self) -> Optional[int]:
        if self.relay_2 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_2.off()
            # Log the event
            log_system_event(
                info="HEATING ON"
            )
            return 0
        except RuntimeError as error:
            print("Relay 2 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                info="[ERROR] HEATING ON"
            )
            return None
        
    def watering_on(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.off()
            # Log the event
            log_system_event(
                info="WATERING ON"
            )
            time.sleep(2)
            self.watering_off()
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                info="[ERROR] WATERING ON"
            )
            return None
        
    def watering_off(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.on()
            log_system_event(
                info="WATERING OFF"
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            log_system_event(
                info="[ERROR] WATERING OFF"
            )
            return None
        
    def get_temperatures(self):
        readings = {}
        if not hasattr(self, "sensors") or not self.sensors:
            print("No 1-Wire sensors available, returning empty readings")
            return readings

        for sensor in self.sensors:
            try:
                readings[sensor.id] = round(sensor.get_temperature(), 2)
            except Exception as e:
                print(f"Failed to read sensor {sensor.id}: {e}")
                readings[sensor.id] = None

        return readings

    def get_humidity_and_temperature(self) -> Optional[Dict[str, float]]: 
        if self.aht20 is None:
            print("Warning: AHT20 sensor not available, returning default values")
            return {
                "temperature": 0.0,  # Default temperature in Celsius
                "humidity": 0.0      # Default humidity in %
            }
        try:    
            self.aht20.write_i2c_block_data(self.I2C_ADDR, 0xAC, [0x33, 0x00])
            time.sleep(0.1)  # czas konwersji ~80ms

            data = self.aht20.read_i2c_block_data(self.I2C_ADDR, 0x00, 6)
            print("Raw I2C data:", [hex(x) for x in data]) 

            raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
            raw_temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5])

            humidity = (raw_humidity / 1048576.0) * 100.0
            temperature = ((raw_temperature / 1048576.0) * 200.0) - 50.0

            return {
                "temperature": temperature,
                "humidity": humidity
            }
            
        except RuntimeError as e:
            print(f"Error reading from AHT20 sensor: {e}, returning default values")
            return {
                "temperature": 0.0,  # Default temperature in Celsius
                "humidity": 0.0      # Default humidity in %
            } 

    def get_soil_humidity(self) -> Optional[float]: 
        if self.mcp is None:
            print("Warning: MCP3008 ADC not available, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
        try:
            humidity_voltage = AnalogIn(self.mcp, MCP.P6).voltage
            return humidity_voltage
        except RuntimeError as e:
            print(f"Error reading from soil humidity sensor: {e}, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
        
    def get_lighting(self) -> Optional[float]: 
        if self.mcp is None:
            print("Warning: MCP3008 ADC not available, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
        try:
            light_voltage = AnalogIn(self.mcp, MCP.P7).voltage
            return light_voltage
        except RuntimeError as e:
            print(f"Error reading from light sensor: {e}, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
