import network
import socket
import time
from machine import Pin as pin
import networkInfo

runningLED = pin(0, pin.OUT)

runningLED.value(1)
# reading network info from seperate py file
print("Network ssid: " + networkInfo.ssid)
print("Password: " + networkInfo.password)

wlan = network.WLAN(network.STA_IF)
wlan.disconnect()
wlan.active(True)
wlan.connect(ssid, password)

# htmlFile = open("txtLog.html", "r")
# html = htmlFile.read()
# htmlFile.close()
# # print(html)
max_wait = 10
while max_wait > 0:
    # if wlan.status() < 0 or wlan.status() >= 3:
    #     break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)

if wlan.status() != 3:
    runningLED.value(0)
    print("wlan.status() == {0}".format(wlan.status()))
    print("Running wlan.scan() to get list of all available networks")
    for result in wlan.scan():
        print("    {0}".format(result))
    raise RuntimeError('network connection failed')
else:
    print("Connected to {}".format(ssid))
    status = wlan.ifconfig()
    print('ip == ' + status[0])

try:
    while True:
        pass
except KeyboardInterrupt:
    runningLED.value(0)
    print("Exited with Keyboard Interruot")
