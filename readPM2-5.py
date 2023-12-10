from machine import Pin as pin
import machine
import time

red = pin(0, pin.OUT)
PM = machine.ADC(pin(26))

try:
    while True:
        red.value(1)
        time.sleep(0.05)
        PM_value = PM.read_u16()
        print(PM_value)

        red.value(0)
        time.sleep(0.95)
except KeyboardInterrupt:    
    red.value(0)
    print("Exited Successfully")