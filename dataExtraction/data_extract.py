import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import ujson

import MDRSOverlay.MDRS_monitoring_overlay.dataExtraction.securityInfo_sample_read_data as securityInfo_sample_read_data
from externalLed import LEDController

# Wi-Fi and MQTT credentials from securityInfo module
ssid = securityInfo_sample_read_data.ssid
wifi_password = securityInfo_sample_read_data.wifi_password
mqtt_username = securityInfo_sample_read_data.mqtt_username
mqtt_password = securityInfo_sample_read_data.mqtt_password
mqtt_client_id = "rpipicoMDRStest_subscriber"  # Ensure unique client ID

sensor_topic = securityInfo_sample_read_data.sensor_topic
bad_sensor_topic = securityInfo_sample_read_data.bad_sensor_topic
location = securityInfo_sample_read_data.location

controller = LEDController()

# Initialize onboard LED (on GPIO 25 for Pico W)
led = Pin("LED", Pin.OUT)

# Storage for local data
local_data = []
check_interval = 1  # seconds
publish_interval = 60*30  # seconds
last_publish_time = time.time()
bad_data_detected = False
bad_data_message = ""

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

# Handle sensor data locally
def handle_sensor_data(sensor_data):
    global bad_data_detected, bad_data_message

    print("Received sensor data:", sensor_data)
    local_data.append(sensor_data)

    # Check for bad sensor values
    for sensor, value in sensor_data.items():
        if type(value) is float or value == 0:  # Bad condition check
            bad_data_detected = True
            bad_data_message = {
                "location": location,
                "sensor": sensor,
                "value": value
            }
            controller.set_led_value(sensor, 0)  # Indicate bad sensor value
        else:
            controller.set_led_value(sensor, 1)  # Indicate good sensor value

# Publish data to Adafruit IO
def publish_data(client):
    global bad_data_detected, bad_data_message, last_publish_time

    current_time = time.time()
    if current_time - last_publish_time >= publish_interval:
        if bad_data_detected:
            print("Publishing bad data:", bad_data_message)
            client.publish(bad_sensor_topic, ujson.dumps(bad_data_message))
            bad_data_detected = False
        else:
            print("Publishing All systems OK")
            client.publish(sensor_topic, "All systems OK")

        last_publish_time = current_time

# Main Function
def main():
    connect_to_wifi()
    client = connect_to_adafruit()

    if client:
        # Subscribe to sensor topic
        try:
            client.subscribe(sensor_topic)
            controller.add_led(name="CO2", pin_number=2)
            controller.add_led(name="Temperature", pin_number=3)
            controller.add_led(name="PM2_5", pin_number=5)
            controller.add_led(name="Humidity", pin_number=4)
            print("Subscribed to topics successfully!")
        except Exception as e:
            print("Error subscribing to topics:", e)
            return

        # Continuously check for messages and handle data
        while True:
            try:
                # Simulate checking data locally every second
                if client.check_msg():
                    topic, msg = client.check_msg()
                    topic = topic.decode("utf-8")
                    if topic == sensor_topic:
                        sensor_data = ujson.loads(msg)
                        handle_sensor_data(sensor_data)

                # Publish data at regular intervals
                publish_data(client)

                time.sleep(check_interval)

            except Exception as e:
                print("Error during main loop:", e)

# Run the script
if __name__ == "__main__":
    main()
