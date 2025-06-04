import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Ustawienie SPI na sprzętowych pinach
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)  # lub board.CE0 jeśli używasz GPIO 8

# Inicjalizacja MCP3008
mcp = MCP3008(spi, cs)

# Kanały: CH0 = wilgotność, CH1 = światło
soil_sensor = AnalogIn(mcp, MCP3008.P0)
light_sensor = AnalogIn(mcp, MCP3008.P1)

try:
    while True:
        print(f"Soil moisture: {soil_sensor.voltage:.2f} V")
        print(f"Light level  : {light_sensor.voltage:.2f} V")
        print("-" * 30)
        time.sleep(1)
except KeyboardInterrupt:
    print("Zakończono.")
