from machine import Pin as pin
import machine
import time


red = pin(0, pin.OUT)
temp_humid_sda = pin(8)
temp_humid_scl = pin(9)

i2c = machine.I2C(0, sda=temp_humid_sda, scl=temp_humid_scl, freq=200000)

time.sleep(0.5) # allow temp sensor time to reach idle state
devices = i2c.scan()

if len(devices) != 0:
    print("Found {} I2C devices".format(len(devices)))
    for device in devices:
        print("Device hex address {}".format(hex(device)))
else:
    print("No I2C devices found")
    
try:
    while True:
        red.value(1)
        time.sleep(0.15)
        red.value(0)
        time.sleep(2)
except KeyboardInterrupt:    
    red.value(0)
    print("Exited Successfully")