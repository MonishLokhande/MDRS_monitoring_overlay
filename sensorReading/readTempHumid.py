from machine import Pin as pin
import machine
import time


temp_humid_sda = pin(6)
temp_humid_scl = pin(3)
# temp_humid_scl = pin(7)
# temp_humid_sda = pin(10)

i2c = machine.I2C(1, sda=temp_humid_sda, scl=temp_humid_scl, freq=400000)

print("Waiting for i2c devices to settle...")
time.sleep(2) # allow temp sensor time to reach idle state
print("Done waiting")

try:
    while True:
        # temp sensor address = 0x38
        print(i2c.readfrom(56, 1))
except KeyboardInterrupt:   
    print("Exited Successfully")