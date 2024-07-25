# [Errno 9] EBADF: potential fixes from github issues:
#     make sure board firmware is updated and we're using latest libraries for everything
#     move mqtt.connect() to inside send_sensor_data function, machine.idle() may be disconnecting and thus causing error

import machine
import time
import network
from umqtt.simple import MQTTClient
import logging

try:
    import readCO2
    import readVOC
    import readPM2_5
    import readOnboardTemp
    import securityInfo
except ImportError as e:
    raise ValueError("Required files not found on local board: {}".format(e))

LED_pin = machine.Pin(7, machine.Pin.OUT)

def send_sensor_data(pin):
    voc_topic = securityInfo.voc_topic
    pm2_5_topic = securityInfo.pm2_5_topic
    temp_topic = securityInfo.temp_topic
    
    try:
        print('Sending data...')
        mqtt_client.publish(securityInfo.co2_topic, '902')
        mqtt_client.publish(co2_topic, str(readCO2.read_analog()))
        mqtt_client.publish(voc_topic, str(readVOC.get_value(VOC_outputA)))
        mqtt_client.publish(pm2_5_topic, str(readPM2_5.get_value()))
        mqtt_client.publish(temp_topic, str(readOnboardTemp.get_value()))
        print('Data sent')
    except Exception as e:
        print(e)
        
        timeList = time.localtime()
        timestamp = str(timeList[0]) +'_'+ str(timeList[1]) +'_'+ str(timeList[2]) +'_'+ str(timeList[3]) +':'+ str(timeList[4]) + ':'+str(timeList[5])
        logging.error(timestamp +': '+ str(e))
        # machine.WDT(timeout=10)
    
debounce_time = 0

def manual_data_read(pin):
    global debounce_time
    if (time.ticks_ms() - debounce_time > 750):
        print('Manually interrupted')
        send_sensor_data()
        debounce_time = time.ticks_ms()

def button_interrupt_setup(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=manual_data_read)
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
mqtt_client_id = securityInfo.mqtt_client_id
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
    time.sleep(0.1)
    LED_pin.value(0)


try:
    logging.basicConfig(filename='adafruit_sensor.log', level=logging.INFO)
    
    # interrupt_button_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)
    # button_interrupt_setup(interrupt_button_pin)
    
    
    co2_reading_pin, CO2_power = readCO2.setup_pins()
    VOC_power, VOC_outputA  = readVOC.setup_pins()
    
    led_timer = machine.Timer(period=5000, mode=machine.Timer.PERIODIC, callback=flash_LED)
    record_timer = machine.Timer(period=5000, mode=machine.Timer.PERIODIC, callback=send_sensor_data)
    # TODO change period on record_timer to desired delay
    
    print('idling...')
    machine.idle()
        
except ImportError:
    raise ValueError("Failed to import collectSensorData, make sure it is copied onto board")
finally:
    mqtt_client.disconnect()

