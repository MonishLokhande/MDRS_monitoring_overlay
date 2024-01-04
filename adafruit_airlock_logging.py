import machine
import time
import network
from umqtt.simple import MQTTClient

try:
    import readCO2
    import readVOC
    import readPM2_5
    import readOnboardTemp
    import securityInfo
except ImportError as e:
    raise ValueError("Required files not found on local board: {}".format(e))

LED_pin = machine.Pin(7, machine.Pin.OUT)

def send_sensor_data():
    global inner_airlock_pin
    global outer_airlock_pin
    
    try:
        print('Sending data...')
        # TODO inner airlock, use above pins.value()
        # TODO outer airlock
        print('Data sent')
    except:
        machine.WDT(timeout=10)
    
debounce_time = 0

def manual_data_read(pin):
    global debounce_time
    if (time.ticks_ms() - debounce_time > 750):
        print('Manually interrupted')
        send_sensor_data()
        debounce_time = time.ticks_ms()

# TODO format into if __main__ blocks
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(securityInfo.ssid,securityInfo.wifi_password)

time_limit = 15
print("connecting to network {}...\nAuto timeout in {} seconds".format(securityInfo.ssid, time_limit))
LED_pin.value(1)
while (not wlan.isconnected()):
    time.sleep(1)
    time_limit -= 1
    if time_limit == 0:
        print(wlan.status())
        for x in range(9):
            LED_pin.toggle()
            time.sleep(0.1)
        raise ValueError("Could not connect to internet, ensure securityInfo properly updated and that internet is available")
print("Successfully connected to network")

# COPIED TOP, from https://core-electronics.com.au/guides/getting-started-with-mqtt-on-raspberry-pi-pico-w-connect-to-the-internet-of-things/

mqtt_host = "io.adafruit.com"
mqtt_username = securityInfo.mqtt_username
mqtt_password = securityInfo.mqtt_password

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = machine.RNG() # TODO verify that it randomly creates good IDs

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()
print("Successfully connected to mqtt client, now starting main loop...")
LED_pin.value(0)


def flash_LED(pin):
    global LED_pin
    
    LED_pin.value(1)
    time.sleep(0.05)
    LED_pin.value(0)


try:
    co2_topic = securityInfo.co2_topic
    voc_topic = securityInfo.voc_topic
    pm2_5_topic = securityInfo.pm2_5_topic
    temp_topic = securityInfo.temp_topic
    # ozone_topic
    # inner_door_topic
    # outer_door_topic
    # water_level_topic
    
    
    inner_airlock_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
    outer_airlock_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    inner_airlock_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=manual_data_read)
    outer_airlock_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=manual_data_read)
    
    co2_reading_pin, CO2_power = readCO2.setup_pins()
    VOC_power, VOC_outputA  = readVOC.setup_pins()
    
    led_timer = machine.Timer(period=5000, mode=machine.Timer.PERIODIC, callback=flash_LED)
    record_timer = machine.Timer(period=1800*1000, mode=machine.Timer.PERIODIC, callback=send_sensor_data())    
        
    print('idling...')
    machine.idle()
        
except ImportError:
    raise ValueError("Failed to import collectSensorData, make sure it is copied onto board")
finally:
    mqtt_client.disconnect()
