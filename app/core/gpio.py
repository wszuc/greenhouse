from os import system
from gpiozero import LED, Servo
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

        # initialize temperature sensor 1 wire
        try:
            self.sensor = w1thermsensor.W1ThermSensor()
            print("DS18B20 temperature sensor initialized successfully")
        except Exception as e:
            print(f"Warning: DS18B20 temperature sensor initialization failed: {e}")
            self.sensor = None

        # Initialize AHT20 
        try:
            self.aht20 = DFRobot_AHT20()
            timeout = 10
            start_time = time.time()
            initialized = False

            while not initialized and (time.time() - start_time) < timeout:
                print("Initializing AHT20 Sensor...", end=" ")
                initialized = self.aht20.begin()
                print("Initialized: ", initialized)
                time.sleep(0.5)

            if initialized:
                print("Done, AHT20 initialized")

            else:
                print("Warning: AHT20 initialization timed out")
                self.aht20 = None

        except Exception as e:
            print(f"Warning: AHT20 sensor initialization failed: {e}")
            self.aht20 = None

        # Initialize SPI and MCP3008
        try:
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
        except Exception as e:
            print(f"Error while moving servo: {e}")

    def roof_close(self) -> Optional[int]:
        if self.servo is None:
            print("Warning: Servo not available")
            return None
        try:
            position = max(-1.0, min(1.0, 1))
            self.servo.value = position
            print(f"Servo set to position CLOSE")
        except Exception as e:
            print(f"Error while moving servo: {e}")

    def led_strip_on(self) -> Optional[int]:
        if self.led_strip is None:
            print("Warning: LED strip not available")
            return None
        try:
            self.led_strip.fill((200,200,200))  # biały
            # Log the event
            log_system_event(
                event_type=EventType.LED_ON,
                description="LED strip turned on (white)",
                actuator_id="led_strip_gpio18"
            )
            return 0
        except RuntimeError as error:
            print("Error during LED strip on: ", error)
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to turn on LED strip: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="led_strip_gpio18"
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
                event_type=EventType.LED_OFF,
                description="LED strip turned off",
                actuator_id="led_strip_gpio18"
            )
            return 0
        except RuntimeError as error:
            print("Error during LED strip off: ", error)
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to turn off LED strip: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="led_strip_gpio18"
            )
            return None

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
        
    def heating_off(self) -> Optional[int]:
        if self.relay_2 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_2.on()
            # Log the event
            log_system_event(
                event_type=EventType.HEATING_OFF,
                description="Heating system activated",
                actuator_id="relay_gpio27",
                details={"action": "heating_start", "duration_planned": "until_manual_stop"}
            )
            return 0
        except RuntimeError as error:
            print("Relay 2 couldn't be turned on: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate heating: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
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
                event_type=EventType.WATERING_OFF,
                description="Heating system activated",
                actuator_id="relay_gpio27"
            )
            return 0
        except RuntimeError as error:
            print("Relay 2 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate heating: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
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
                event_type=EventType.WATERING_OFF,
                description="Watering system activated",
                actuator_id="relay_gpio27"
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate heating: {error}",
                severity=EventSeverity.ERROR,
                actuator_id="relay_gpio27"
            )
            return None
        
    def watering_off(self) -> Optional[int]:
        if self.relay_1 is None:
            print("Warning: Relay not available")
            return None
        try:
            self.relay_1.on()
            # Log the event
            log_system_event(
                event_type=EventType.WATERING_OFF,
                description="Watering system activated",
                actuator_id="relay_gpio27"
            )
            return 0
        except RuntimeError as error:
            print("Relay 1 couldn't be turned off: ", error)
            # Log the error
            log_system_event(
                event_type=EventType.ACTUATOR_ERROR,
                description=f"Failed to activate heating: {error}",
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
            # Try to read temperature 10 times
            for i in range(10):
                if self.aht20.start_measurement_ready():
                    temperature = self.aht20.get_temperature_C()
                    humidity = self.aht20.get_humidity_RH()
                    return {
                        "temperature": temperature,
                        "humidity": humidity
                    }
                else:
                    time.sleep(2)
            
            print("Warning: AHT20 measurement not ready after 10 tries, returning default values")
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
