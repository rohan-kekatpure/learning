"""
Script to measure WiFi signal strength (in dBm)

If you run this code and wander around your 
home, you will should see that the WiFi signal 
strength near your router is about 1k-10k times
stronger than one of your distant rooms.
"""
import network
from time import sleep

WIFI_ESSID = 'HOME-0E52'
WIFI_PASSWD = 'rohan123'

def _connect():    
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.active(True)
        wlan.connect(WIFI_ESSID, WIFI_PASSWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return wlan

def _scan(wlan):
    wifi_list = wlan.scan()
    for w in wifi_list:
        print(w)
    return wifi_list

def _signal_strength(wlan):
    return wlan.status('rssi')

def main():
    wlan = _connect()
    while True:    
        _str = _signal_strength(wlan)
        print(f'signal strength -> {_str}')
        sleep(0.1)

if __name__ == '__main__':
    main()
    