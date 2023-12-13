import network
import socket
import time
from machine import Pin as pin
import securityInfo
import uasyncio as asyncio

def connect_to_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(True)
    # wlan.config(pm = 0xa11140) # Disable power-save mode
    
    wlan.disconnect()
    wlan.connect(securityInfo.ssid, securityInfo.wifi_password)

    print("Finding Connection, timeout in 30 seconds")
    print("Connecting with Network ssid: " + securityInfo.ssid + " and Password: " + securityInfo.wifi_password)
    print("waiting for connection...")
    max_wait = 30
    while max_wait > 0:
        if wlan.status() == 3:
            break
        max_wait -= 1
        time.sleep(1)

    if wlan.status() != 3:
        print("wlan.status() == {0}".format(wlan.status()))
        raise RuntimeError('network connection failed')
    else:
        print("Connected to {}".format(securityInfo.ssid))
        status = wlan.ifconfig()
        print('ip == ' + status[0])
    

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
    # response = load_html()
    response = """ <h2>
    Reading values from txt Log
</h2>
<p>
    <script>
        document.write(loadFile(sensor_data.txt))
    </script>
</p>
<button
    type="button"
    onclick = >
    Display Logs
</button>

<script>
    function loadFile(filePath){
        var result = null;
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", filepath, false);
        xmlhttp.send();
        if (xmlhttp.status==200){
            result = smlhttp.responseText;
        }
        else{
            result = "Failed to retrieve data";
        }
        return result
    }
</script> """


    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    connect_to_network()
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))


    # create file and read initial sensor values
    output_file = open("sensor_data.txt", 'a')
    curr_time = time.localtime()
    timestamp = str(str(curr_time[1])+', '+ str(curr_time[2]) +', '+ str(curr_time[0]) +'-' + str(curr_time[3]) +":"+ str(curr_time[4]))
    output_file.write("Tested at: {}\n".format(timestamp))
    output_file.close()
    print("Output file made and timestamped")
    
    while True:
        await asyncio.sleep(0.25)

try: 
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

