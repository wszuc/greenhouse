import smbus2

bus = smbus2.SMBus(1)  
address = 0x38         

try:
    bus.write_quick(address)  
    print(f"Urządzenie znalezione pod adresem 0x{address:02X}")
except OSError:
    print(f"Brakk urządzenia pod adresem 0x{address:02X}")
