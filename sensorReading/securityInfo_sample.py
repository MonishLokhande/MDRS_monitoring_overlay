## This is a sample file, add your corresponding details to record values.
ssid = ""  
    
wifi_password = ""

mqtt_username = ""

mqtt_password = ""

# Location where the RPi is placed
rpiName = "green-hab-local"

mqtt_client_id = "rpipicoMDRStest"+rpiName

co2_topic = "{}/feeds/{}".format(mqtt_username, rpiName+".co2")
pm2_5_topic = "{}/feeds/{}".format(mqtt_username, rpiName+".pm25")
temp_topic = "{}/feeds/{}".format(mqtt_username, rpiName+".temperature")
hum_topic = "{}/feeds/{}".format(mqtt_username, rpiName+".humidity")
sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorlocal")
bad_sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorlocalbad")
bad_global_sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorglobalbad")
good_global_sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorglobalgood")