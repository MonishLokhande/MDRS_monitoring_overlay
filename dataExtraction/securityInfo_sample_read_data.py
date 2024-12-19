## This is a sample file, add your corresponding details to record values.
ssid = ""  
    
wifi_password = ""

mqtt_username = ""

mqtt_password = ""


locations = {"green-hab":["CO2", "Temperature", "Humidity"], "upper-hab":["CO2", "Temperature", "Humidity"]}

sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorlocal")
bad_sensor_topic = "{}/feeds/{}".format(mqtt_username, "sensorlocalbad")