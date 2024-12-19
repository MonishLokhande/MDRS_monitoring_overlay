import time

class ExternalLED:
    def __init__(self, name, pin_number):
        self.name = name
        self.pin_number = pin_number  # Simulated pin number
        self.state = 0  # 0 = OFF, 1 = ON
        print(f"Initialized LED '{self.name}' on simulated pin {self.pin_number}")

    def value(self, state):
        self.state = state
        state_str = "ON" if state else "OFF"
        print(f"LED '{self.name}' on pin {self.pin_number} is now {state_str}")

    def blink(self, on_time=1, off_time=1, count=30):
        print(f"Starting blink for LED '{self.name}' ({count} times)...")
        for i in range(count):
            print(f"Blink {i + 1}: LED '{self.name}' is ON")
            time.sleep(on_time)
            print(f"Blink {i + 1}: LED '{self.name}' is OFF")
            time.sleep(off_time)
        print(f"Finished blinking LED '{self.name}'")


class LEDController:
    def __init__(self):
        self.leds = {}
    
    def add_led(self, name, pin_number):
        """Add a simulated LED."""
        if name in self.leds:
            print(f"Warning: LED '{name}' already exists.")
        else:
            self.leds[name] = ExternalLED(name, pin_number)
            print(f"LED '{name}' added to controller.")
    
    def set_led_value(self, name, value):
        """Turn LED ON (1) or OFF (0)."""
        if name in self.leds:
            self.leds[name].value(value)
        else:
            print(f"Error: LED '{name}' not found in controller!")

    def blink_led(self, name, on_time=1, off_time=1, count=30):
        """Blink a specific LED."""
        if name in self.leds:
            self.leds[name].blink(on_time, off_time, count)
        else:
            print(f"Error: LED '{name}' not found in controller!")
    
    def all_off(self, location):
        """Turn off all LEDs in a specific location."""
        for led_name in self.leds:
            if location in led_name:
                self.leds[led_name].value(0)
        print(f"All LEDs in location '{location}' turned off.")