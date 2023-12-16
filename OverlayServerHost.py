import network
import socket
import time
from machine import Pin as pin
import securityInfo

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

def open_socket():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    return s

def read_txt(path):
    with open(path, 'r') as input_file:
        data = input_file.read()
    return data

# Listen for connections
connect_to_network()
load_html()
s = open_socket()
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        html = load_html()
        response = html
        sensor_data = read_txt('temp_data.txt')
        response = response.replace('txt_data', sensor_data)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
    except KeyboardInterrupt:
        print('Exited via KeyboardInterrupt')
        break
        
    



