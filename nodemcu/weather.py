import socket
import json
import time
import os
import random

try:
    from machine import Pin
    import network
except:
    pass

API_KEY = 'f76777ad611a48b395c45889d8d04cf0'
WIFI_ESSID = 'HOME-0E52'
WIFI_PASSWD = 'rohan123'

PINOUT = {
    'D3': 0,
    'TX': 1,
    'D4': 2,
    'RX': 3,
    'D2': 4,
    'D1': 5,
    'SD2': 9,
    'SD3': 10,
    'D7': 13,
    'D5': 14,
    'D8': 15
}

def show_status(temperature, pin_hot, pin_cold):    
    # Randomization for debug
    # r = random.getrandbits(1)
    # if r > 0:
    #     temperature = 60
    # else:
    #     temperature = 40   
    
    if temperature > 60:
        pin_hot.value(1)
        pin_cold.value(0)
    else:
        pin_hot.value(0)
        pin_cold.value(1)

def flash(pin):
    pin.value(1)
    time.sleep(0.05)
    pin.value(0)
    time.sleep(0.05)

def urlparse(url):
    protocol, rest = url.split('://', 1)
    host, path = rest.split('/', 1)
    path = '/{}'.format(path) 
    return protocol, host, path

def get(url, status_pin):    
    protocol, host, path = urlparse(url)    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    # Get IP address and port of the host
    host_ip, port = socket.getaddrinfo(host, 80)[0][-1]    
    sock.connect((host_ip, 80))    
    req = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)    
    sock.send(req.encode())
    reply = b''
    bufsize = 32
    while True:
        try:
            chunk = sock.recv(bufsize)
            flash(status_pin)
            if chunk:
                reply += chunk
            else:
                break            
        except OSError:
            break                    

    sock.close()    
    return reply

def read_temperature(status_pin):    
    url = 'https://api.openweathermap.org/data/2.5/weather?zip=94087,us&appid={}'.format(API_KEY)     
    response = get(url, status_pin)
    response = response.decode('ascii')
    startindex = response.index('{')  # Start of json string
    response = json.loads(response[startindex:])    
    temp_K = response['main']['temp']
    temp_F = (temp_K - 273.15) * 9/5 + 32.0
    return temp_F

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ESSID, WIFI_PASSWD)
    while not wlan.isconnected():
        pass    

def main():
    pin_hot = Pin(PINOUT['D3'], Pin.OUT)
    pin_cold = Pin(PINOUT['D1'], Pin.OUT)                                
    pin_data = Pin(PINOUT['D8'], Pin.OUT)

    # Startup
    for pin in [pin_hot, pin_cold, pin_data]:
        pin.value(1)
        time.sleep(0.3)
        pin.value(0)
    
    # Connect to Wifi
    connect()

    # Main loop
    while True:
        try:
            temperature = read_temperature(pin_data)        
            show_status(temperature, pin_hot, pin_cold)
        except:
            pass

        time.sleep(10)

if __name__ == '__main__':
    main()