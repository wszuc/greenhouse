from gpiozero import LED
import w1thermsensor

def led_on():
    led = LED(17)

def led_off():
    led = LED(17)

def get_temp():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    return temp
