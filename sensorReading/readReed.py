import machine
import time

def get_value(pin):
    return pin.value()

if __name__ == "__main__":
    print('Starting')

    reed_pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    try:
        while True:
            
            print(get_value(reed_pin))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('exited via keyboard')
