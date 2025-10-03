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
import time
from app.db.utils.event_logger import log_system_event
from app.db.models import EventType, EventSeverity


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
        
        # Initialize GPIO pins with error handling
        try:
            self.led = LED(17)
            print("LED initialized successfully")
        except Exception as e:
            print(f"Warning: LED initialization failed: {e}")
            self.led = None
            
        try:
            self.relay_1 = LED(27)
            self.relay_1.on()
            print("Relay initialized successfully")
        except Exception as e:
            print(f"Warning: Relay initialization failed: {e}")
            self.relay_1 = None

        

        # Initialize temperature sensor with error handling
        try:
            self.sensor = w1thermsensor.W1ThermSensor()
            print("DS18B20 temperature sensor initialized successfully")
        except Exception as e:
            print(f"Warning: DS18B20 temperature sensor initialization failed: {e}")
            self.sensor = None

        # Initialize AHT20 sensor with error handling
        try:
            self.aht20 = DFRobot_AHT20()
            # Try to initialize AHT20 with timeout
            timeout = 10
            start_time = time.time()
            while self.aht20.begin() != True and (time.time() - start_time) < timeout:
                print("Initializing AHT20 Sensor...", end=" ")
                time.sleep(0.5)
            
            if self.aht20.begin() == True:
                print("Done, AHT20 initialized")
                self.aht20.reset()
            else:
                print("Warning: AHT20 initialization timed out")
                self.aht20 = None
        except Exception as e:
            print(f"Warning: AHT20 sensor initialization failed: {e}")
            self.aht20 = None

        # Initialize SPI and MCP3008 with error handling
        try:
            self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            self.cs = digitalio.DigitalInOut(board.D25)
            self.mcp = MCP.MCP3008(self.spi, self.cs)
            print("MCP3008 ADC initialized successfully")
        except Exception as e:
            print(f"Warning: MCP3008 ADC initialization failed: {e}")
            self.mcp = None

        self._initialized = True

    def led_on(self) -> Optional[int]:
        if self.led is None:
            print("Warning: LED not available")
            return None
        try:
            self.led.on()
            # Log the event
            log_system_event(
                event_type=EventType.LED_ON,
                description="LED indicator turned on",
                actuator_id="led_gpio17"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation led.on(): ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to turn on LED: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="led_gpio17"
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
                event_type=EventType.LED_OFF,
                description="LED indicator turned off",
                actuator_id="led_gpio17"
            )
            return 0
        except RuntimeError as error:
            print("Error during operation led.off(): ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to turn off LED: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="led_gpio17"
            )
            return None
        
    def watering_on(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.on()
            # Log the event
            log_system_event(
                event_type=EventType.WATERING_ON,
                description="Watering system activated",
                actuator_id="relay_gpio27",
                details={"action": "watering_start", "duration_planned": "until_manual_stop"}
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned on: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate watering system: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
            )
            return None
        
    def watering_off(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.off()
            # Log the event
            log_system_event(
                event_type=EventType.WATERING_OFF,
                description="Watering system deactivated",
                actuator_id="relay_gpio27"
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to deactivate watering system: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
            )
            return None
        
    def watering_on(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.on()
            # Log the event
            log_system_event(
                event_type=EventType.WATERING_ON,
                description="Watering system activated",
                actuator_id="relay_gpio27",
                details={"action": "watering_start", "duration_planned": "until_manual_stop"}
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned on: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate watering system: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
            )
            return None
        
    def heating_off(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.off()
            # Log the event
            log_system_event(
                event_type=EventType.WATERING_OFF,
                description="Watering system deactivated",
                actuator_id="relay_gpio27"
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to deactivate watering system: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
            )
            return None
        
    def get_temperature(self) -> Optional[float]:
        if self.sensor is None:
            print("Warning: DS18B20 temperature sensor not available, returning default value")
            return 0.0  # Default temperature in Celsius
        try:
            temp = self.sensor.get_temperature()
            return temp
        except RuntimeError as error:
            print("Error while reading temperature from temp. sensor: ", error)
            return 0.0  # Default temperature in Celsius

    def get_humidity_and_temperature(self) -> Optional[Dict[str, float]]: 
        if self.aht20 is None:
            print("Warning: AHT20 sensor not available, returning default values")
            return {
                "temperature": 0.0,  # Default temperature in Celsius
                "humidity": 0.0      # Default humidity in %
            }
        try:
            if self.aht20.start_measurement_ready(crc_en = True):
                temperature = self.aht20.get_temperature_C()
                humidity = self.aht20.get_humidity_RH()
                return {
                    "temperature": temperature,
                    "humidity": humidity
                }
            else:
                print("Warning: AHT20 measurement not ready, returning default values")
                return {
                    "temperature": 0.0,  # Default temperature in Celsius
                    "humidity": 0.0      # Default humidity in %
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
            humidity_voltage = AnalogIn(self.mcp, MCP.P0).voltage
            return humidity_voltage
        except RuntimeError as e:
            print(f"Error reading from soil humidity sensor: {e}, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
        
    def get_lighting(self) -> Optional[float]: 
        if self.mcp is None:
            print("Warning: MCP3008 ADC not available, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
        try:
            light_voltage = AnalogIn(self.mcp, MCP.P1).voltage
            return light_voltage
        except RuntimeError as e:
            print(f"Error reading from light sensor: {e}, returning default value")
            return 0.0  # Default voltage (middle of 0-5V range)
