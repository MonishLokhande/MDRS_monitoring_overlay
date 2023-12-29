import machine
import time


print('Starting')

reed_pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
try:
    while True:
        
        print(reed_pin.value())
        time.sleep(0.5)
except KeyboardInterrupt:
    print('exited via keyboard')