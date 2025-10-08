import time
import smbus2

I2C_ADDR = 0x38
bus = smbus2.SMBus(1)

# Sprawdzenie statusu
status = bus.read_byte_data(I2C_ADDR, 0x71)
print(f"Status: 0x{status:02X}")

# Wyślij polecenie pomiaru (trigger measurement)
bus.write_i2c_block_data(I2C_ADDR, 0xAC, [0x33, 0x00])
time.sleep(0.1)  # czas konwersji ~80ms

# Odczytaj 6 bajtów z pomiaru
data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 6)
print("Raw data:", [hex(x) for x in data])

# Parsowanie surowych danych
raw_humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
raw_temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5])

humidity = (raw_humidity / 1048576.0) * 100.0
temperature = ((raw_temperature / 1048576.0) * 200.0) - 50.0

print(f"Temperature: {temperature:.2f} °C")
print(f"Humidity: {humidity:.2f} %")
