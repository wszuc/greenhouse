import time
import board
import busio
from app.external_libs.DFRobot_AHT20 import DFRobot_AHT20

i2c = busio.I2C(board.SCL, board.SDA)
aht = DFRobot_AHT20()

print("Initializing AHT20...")
if not aht.begin():
    print("AHT20 not detected!")
    exit(1)

while True:
    temp = aht.get_temperature()
    hum = aht.get_humidity()
    print(f"Temp: {temp:.2f}°C, Hum: {hum:.2f}%")
    time.sleep(2)
