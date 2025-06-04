import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D25)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

try:
    while True:
        humidity_voltage = AnalogIn(mcp, MCP.P0).voltage
        light_voltage = AnalogIn(mcp, MCP.P1).voltage

        print(f'Humidity voltage: {humidity_voltage:.2f} V')
        print(f'Light voltage   : {light_voltage:.2f} V')
        print('-' * 30)

        time.sleep(0.1)  # 100 ms
except KeyboardInterrupt:
    print("end")