# suprisingly lard to connect pins without headers, but we can read input
import machine
import time

# if __name__ == "__main__": unnessecary
# name file main.py if tou want it to run on boot

red = machine.Pin(0, machine.Pin.OUT)
try:
    while True:
        red.value(1)
        time.sleep(0.25)
        red.value(0)
        time.sleep(0.25)
except KeyboardInterrupt:    
    red.value(0)
    print("Exited Successfully")
