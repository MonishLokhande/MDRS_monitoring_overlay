from machine import Pin
import time

class ExternalLED:
    def __init__(self, name, pin_number):
        self.name = name
        self.led = Pin(pin_number, Pin.OUT)
    
    def value(self, state):
        self.led.value(state)

    def blink(self, on_time=1, off_time=1, count=30):
        for _ in range(count):
            self.led.value(1)  # Turn on
            time.sleep(on_time)
            self.led.value(0)  # Turn off
            time.sleep(off_time)

class LEDController:
    def __init__(self):
        self.leds = {}
    
    def add_led(self, name, pin_number):
        self.leds[name] = ExternalLED(name, pin_number)
    
    def set_led_value(self, name, value):
        if name in self.leds:
            self.leds[name].value(value)
        else:
            print(f"LED '{name}' not found!")

    def blink_led(self, name, on_time=1, off_time=1, count=10):
        if name in self.leds:
            self.leds[name].blink(on_time, off_time, count)
        else:
            print(f"LED '{name}' not found!")

    def all_off(self, location):
        """Turn off all LEDs in a specific location."""
        for led_name in self.leds:
            if location in led_name:
                self.leds[led_name].value(0)
        print(f"All LEDs in location '{location}' turned off.")
