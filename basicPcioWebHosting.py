import network
import socket
import time
from machine import Pin as pin
import securityInfo
import uasyncio as asyncio

def connect_to_network():
    runningLED.value(1)
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(True)
    # wlan.config(pm = 0xa11140) # Disable power-save mode
    
    wlan.disconnect()
    wlan.connect(securityInfo.ssid, securityInfo.wifi_password)

    print("Finding Connection, timeout in 15 seconds")
    print("Network ssid: " + securityInfo.ssid)
    print("Password: " + securityInfo.wifi_password)
    print("waiting for connection...")
    max_wait = 15
    while max_wait > 0:
        if wlan.status() == 3:
            break
        max_wait -= 1
        time.sleep(1)

    if wlan.status() != 3:
        runningLED.value(0)
        print("wlan.status() == {0}".format(wlan.status()))
        print("Running wlan.scan() to get list of all available networks")
        for result in wlan.scan():
            print("    {0}".format(result))
        raise RuntimeError('network connection failed')
    else:
        print("Connected to {}".format(securityInfo.ssid))
        status = wlan.ifconfig()
        print('ip == ' + status[0])
    
    runningLED.value(0)


def load_html(path = "txtLog.html"):
    htmlFile = open(path, "r")
    html = htmlFile.read()
    htmlFile.close()
    return html

async def serve_client(reader, writer):
    print("Client connected")

    # no need to get reader input, oly displaying static page for now

    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    response = load_html()
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    connect_to_network()
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    
    while True:
        runningLED.value(1)
        await asyncio.sleep(0.25)
        runningLED.value(0)
        await asyncio.sleep(1.5)

        
runningLED = pin(0, pin.OUT)
try: 
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
