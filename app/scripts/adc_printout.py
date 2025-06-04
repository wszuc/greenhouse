import time
import board
import digitalio
import bitbangio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Ustawienie SPI na niestandardowych pinach
spi = bitbangio.SPI(clock=board.D11, MISO=board.D13, MOSI=board.D19)
cs = digitalio.DigitalInOut(board.D26)  # CS

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
