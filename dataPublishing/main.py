import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import ujson
import utime

import securityInfo
from checkval import checkval

ssid = securityInfo.ssid
wifi_password = securityInfo.wifi_password
mqtt_username = securityInfo.mqtt_username
mqtt_password = securityInfo.mqtt_password
mqtt_client_id = securityInfo.mqtt_client_id
co2_topic = securityInfo.co2_topic
pm2_5_topic = securityInfo.pm2_5_topic
temp_topic = securityInfo.temp_topic
hum_topic = securityInfo.hum_topic
sensors = securityInfo.sensor_topic
bad_sensors = securityInfo.bad_sensor_topic
good_global_sensor_topic = securityInfo.good_global_sensor_topic
bad_global_sensor_topic = securityInfo.bad_global_sensor_topic
rpi = securityInfo.rpiName
rpi = rpi.replace("-local","")

led = Pin("LED", Pin.OUT)

good_sensor_list = []
bad_sensor_list = []
delay = 20*60
val_temp = 10
time_error = 0 # Time sensor has error
time_good = 0 # TIme all sensors are good
error_check_prev = 0
sensor_okay_time = 60*60
last_post_time = 0 # Last timestamp of data published
try:
    import readCO2
    import readTempHumid
    
except:
    raise ValueError("Error importing files\nMake sure everything being imported is copied onto the pi and named exactly the same as specified in this file")  
    


def json_to_multiline_string(json_dict,tag='local'):
    if not isinstance(json_dict, dict):
            raise ValueError("Input must be a dictionary.")
        
    if tag == 'local':
        
        lines = []
        for key, value in json_dict.items():
            value_str = ujson.dumps(value) if isinstance(value, (dict, list)) else str(value)
            lines.append(f"{key}: {value_str}")
        
        return "\n".join(lines)
    
    elif tag == 'global':
        result_lines = []
        for timestamp, data in json_dict.items():
            # Convert the timestamp to a human-readable datetime string
            try:
                timestamp = int(timestamp)
                datetime_tuple = utime.localtime(timestamp)
                datetime_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                    datetime_tuple[0], datetime_tuple[1], datetime_tuple[2],
                    datetime_tuple[3], datetime_tuple[4], datetime_tuple[5]
                )
            except (ValueError, TypeError):
                raise ValueError(f"Invalid timestamp: {timestamp}")

            # Add the datetime line
            result_lines.append(f"Timestamp: {datetime_str}")

            # Add the nested dictionary lines
            if isinstance(data, dict):
                for key, value in data.items():
                    result_lines.append(f"  {key}: {value}")
            else:
                raise ValueError(f"Expected a dictionary as value, got {type(data)}")

        return "\n".join(result_lines)
    

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, wifi_password)

    #print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Still connecting...")

    #print("Connected to Wi-Fi:", wlan.ifconfig())

def connect_to_adafruit():
    client = MQTTClient(mqtt_client_id, "io.adafruit.com", user=mqtt_username, password=mqtt_password)
    try:
        client.connect()
        #print("Connected to Adafruit IO")
        return client
    except Exception as e:
        #print("Could not connect to Adafruit IO:", e)
        return None

def check():
    global time_error, time_good
    diff = time_good - time_error
    if diff > 0 and diff < sensor_okay_time:
        return 0
    elif diff >= sensor_okay_time:
        return 1
    else:
        return -1

def remove_entries(good_list, time):
    cop = good_list
    
    for di in cop:
        if list(di.keys())[0] < time - delay:
            good_list.remove(di)
    return good_list

def add_bad_sensor_data(bad_sensor_list, timestamp, not_acceptable_data):
    bad_sensor_entry = {timestamp: not_acceptable_data}
    bad_sensor_list.append(bad_sensor_entry)

    return bad_sensor_list

def add_good_sensor_data(good_sensor_list, bad_sensor_list, timestamp, acceptable_data):
    global error_check_prev
    time = timestamp  # Current time
    error_check = check()
    if error_check == 1:
        print("Measurement good for past 1 hour")
        good_sensor_entry = {time: {"message":"All Sensors Good"}}
        good_sensor_list.append(good_sensor_entry)
    elif error_check == 0:
        if error_check_prev == -1:
            print("Previous Measurement was an Error")
            good_sensor_entry = {time: acceptable_data}
            good_sensor_list.append(good_sensor_entry)
        else:        
            print("Measurement was all good, waiting for 1 hour")
            good_sensor_entry = {time: {"message":"All Sensors Good"}}
            good_sensor_list.append(good_sensor_entry)
        return good_sensor_list
    elif error_check == -1:
        print("Measurement has error")
        good_sensor_entry = {time: acceptable_data}
        good_sensor_list.append(good_sensor_entry)
    error_check_prev = error_check
    return good_sensor_list

def publish_values(client):
    try:
        from timenow import get_time
        global val_temp
        global time_good, time_error, last_post_time
        val_CO2 = readCO2.read_analog()  # Example CO2 value
        val_temp, val_humid = readTempHumid.get_value()  # Example temperature and humidity values
        client.publish(co2_topic, str(val_CO2))  # Example CO2 value
        #client.publish(pm2_5_topic, str(val_PM2_5))  # Example PM2.5 value
        client.publish(temp_topic, str(val_temp))  # Example temperature value
        client.publish(hum_topic, str(val_humid))  # Example humidity value
        payload = {
            "Temperature": val_temp,
            "Humidity": val_humid,
            #"PM2_5": val_PM2_5,
            "CO2": val_CO2
        }

        acceptable_data, not_acceptable_data = checkval(payload)
        dump_data_good = "-------\n" + f"{rpi}\n" + json_to_multiline_string(acceptable_data)
        client.publish(sensors, dump_data_good)

        current_time = get_time()
        
        if not_acceptable_data:
            time_error = current_time
            dump_data_bad = "-------\n" + f"{rpi}\n" + json_to_multiline_string(not_acceptable_data)
            client.publish(bad_sensors, dump_data_bad)
            add_bad_sensor_data(bad_sensor_list,current_time,not_acceptable_data)
            add_good_sensor_data(good_sensor_list,bad_sensor_list,current_time,acceptable_data)
        else:
            time_good = current_time
            add_good_sensor_data(good_sensor_list,bad_sensor_list,current_time,acceptable_data)
        print("Good:",good_sensor_list)
        print("Bad:",bad_sensor_list)
        #print("Times:", time_good, time_error)
        # print(list(bad_sensor_list[0].keys())[0] == time_print)
        time_print = list(good_sensor_list[0].keys())[0]
        if current_time - time_print >= delay:
            #print("30 minutes have passed. Resetting sensor lists.")
            if bad_sensor_list != []:
                first_error_time = list(bad_sensor_list[0].keys())[0]
                if first_error_time == time_print:
                    client.publish(good_global_sensor_topic,"-------\n" + f"{rpi}\n" + json_to_multiline_string(good_sensor_list[0],tag='global'))
                    client.publish(bad_global_sensor_topic,"-------\n" + f"{rpi}\n" + json_to_multiline_string(bad_sensor_list[0],tag='global'))
                    good_sensor_list.pop(0)
                    bad_sensor_list.pop(0)
                    last_post_time = time_print
                else:
                    print("No error at current time.")
                    if time_print - last_post_time >= sensor_okay_time:
                        print("Time still less than sensor okay time.")
                        client.publish(good_global_sensor_topic,"-------\n" + f"{rpi}\n" + json_to_multiline_string(good_sensor_list[0],tag='global'))
                        good_sensor_list.pop(0)
                        last_post_time = time_print
                    else:
                        good_sensor_list.pop(0)
            else:
                print("No error at current time. 1")
                if time_print - last_post_time >= sensor_okay_time:
                    print("Time still less than sensor okay time.")
                    client.publish(good_global_sensor_topic,"-------\n" + f"{rpi}\n" + json_to_multiline_string(good_sensor_list[0],tag='global'))
                    good_sensor_list.pop(0)
                    last_post_time = time_print
                else:
                    good_sensor_list.pop(0)
        return not_acceptable_data, acceptable_data
    except Exception as e:
        print("Error publishing values:", e)
        return None, None

def blink_led():
    led.on()
    time.sleep(0.5)  # LED on for 0.5 seconds
    led.off()

# Main Function
def main():
    connect_to_wifi()
    from timenow import get_time
    time_start = get_time()
    print(time_start)
    client = connect_to_adafruit()
    

    if client:
        while True:
            #print("Publishing values...")
            last_ok_time, last_bad_time = publish_values(client)
            blink_led()  # Blink the LED
            time.sleep(60)  # 30-second delay

# Run the script
if __name__ == "__main__":
    main()
