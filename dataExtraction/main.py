import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import ujson
import re

import MDRSOverlay.MDRS_monitoring_overlay.dataExtraction.securityInfo_sample_read_data as securityInfo_sample_read_data
from externalLed import LEDController

locations_timestamps = {}
# Wi-Fi and MQTT credentials from securityInfo module
ssid = securityInfo_sample_read_data.ssid
wifi_password = securityInfo_sample_read_data.wifi_password
mqtt_username = securityInfo_sample_read_data.mqtt_username
mqtt_password = securityInfo_sample_read_data.mqtt_password
mqtt_client_id = "rpipicoMDRStest_subscriber"  # Ensure unique client ID
sensor_topic = securityInfo_sample_read_data.sensor_topic
bad_sensor_topic = securityInfo_sample_read_data.bad_sensor_topic
locations = securityInfo_sample_read_data.locations

controller = LEDController()

# Initialize onboard LED (on GPIO 25 for Pico W)
led = Pin("LED", Pin.OUT)
locations_timestamps = {}
# Step 1: Wi-Fi Connection
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, wifi_password)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Still connecting...")

    print("Connected to Wi-Fi:", wlan.ifconfig())

# Step 2: Connect to Adafruit IO
def connect_to_adafruit():
    client = MQTTClient(mqtt_client_id, "io.adafruit.com", user=mqtt_username, password=mqtt_password)
    try:
        client.connect()
        print("Connected to Adafruit IO")
        return client
    except Exception as e:
        print("Could not connect to Adafruit IO:", e)
        return None

def initialize_timestamps(locations,time_now):
    locations_timestamps = {}
    for location in locations:
        locations_timestamps[location] = time_now
    return locations_timestamps

# Handle bad sensor values
def handle_bad_sensor_values(location,bad_values):
    global locations_timestamps
    time_now = time.time()
    locations_timestamps[location] = time_now
    for sensor, value in bad_values.items():
        led_name = f"{location}-{sensor}"
        print(f"Sensor: {sensor}, Value: {value}")
        if type(value) is float:
            controller.blink_led(led_name)
        else:
            controller.set_led_value(led_name, 0)

# Handle good sensor values
def handle_good_sensor_values(location, sensor_data):
    global locations_timestamps
    time_now = time.time()
    locations_timestamps[location] = time_now
    for sensor, value in sensor_data.items():
        led_name = f"{location}-{sensor}"
        print(f"Sensor: {led_name}, Value: {value}")
        controller.set_led_value(led_name, 1)

def parse_sensor_data(input_string):
    # Extract location by finding the first line and replacing hyphens with spaces
    lines = input_string.strip().split('\n')
    lines = lines[1:]
    location = lines[0]
    
    # Extract sensors and values using a regex for key-value pairs
    sensor_data = {}
    for line in lines[1:]:
        match = re.match(r"([a-zA-Z0-9]+):\s*([\d.]+)", line)
        if match:
            sensor, value = match.groups()
            sensor_data[sensor] = float(value)  # Convert value to float for flexibility
    
    return location, sensor_data

# Callback function for MQTT messages
def mqtt_callback(topic, msg):
    try:
        topic = topic.decode("utf-8")
        if topic == bad_sensor_topic:
            location, bad_values = parse_sensor_data(msg.decode("utf-8"))
            handle_bad_sensor_values(location,bad_values)
        elif topic == sensor_topic:
            print("Received sensor data")
            location, good_values = parse_sensor_data(msg.decode("utf-8"))
            handle_good_sensor_values(location,good_values)
    except Exception as e:
        print("Error parsing message or handling data:", e)

# Blink the LED
def blink_led():
    led.on()
    time.sleep(0.5)  # LED on for 0.5 seconds
    led.off()

def add_leds(locations=locations):
    pin = 0
    result = [f"{key}-{value}" for key, values in locations.items() for value in values]
    print("LEDs initialized:", result)
    for led_name in result:
        controller.add_led(name=led_name, pin_number=pin)
        pin += 1
    locations_checked = list(locations.keys())
    return locations_checked

def check_leds(locations_check, locations_timestamps, locations=locations):
    time_now = time.time()
    for location in locations_check:
        if time_now - locations_timestamps[location] > 40:
            for sensor in locations[location]:
                led_name = f"{location}-{sensor}"
                print(f"{led_name} not working")
                controller.set_led_value(led_name, 0)
            locations_timestamps[location] = time_now

# Main Function
def main():
    connect_to_wifi()
    client = connect_to_adafruit()
    global locations_timestamps
    if client:
        # Set callback function for received messages
        client.set_callback(mqtt_callback)
        time_start = time.time()
        # Subscribe to topics
        try:
            client.subscribe(sensor_topic)
            client.subscribe(bad_sensor_topic)
            locations_check = add_leds()
            print("Locations checked:", locations_check) 
            locations_timestamps = initialize_timestamps(locations_check,time_start)
            print("Subscribed to topics successfully!")
        except Exception as e:
            print("Error subscribing to topics:", e)
            return

        # Continuously check for messages
        while True:
            try:
                client.check_msg()  # Check for new messages
                blink_led()  # Blink the LED
                if time.time() - time_start > 60:
                    print("60 seconds have passed. Checking LEDS")
                    check_leds(locations_check, locations_timestamps)
                    time_start = time.time()
                time.sleep(10)  # Wait 10 second before checking again
            except Exception as e:
                print("Error checking messages:", e)

# Run the script
if __name__ == "__main__":
    main()


