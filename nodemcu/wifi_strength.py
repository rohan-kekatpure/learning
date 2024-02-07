"""
Script to measure WiFi signal strength (in dBm)

If you run this code and wander around your 
home, you will should see that the WiFi signal 
strength near your router is about 1k-10k times
stronger than one of your distant rooms.
"""
import network
from time import sleep
from machine import Pin, PWM

WIFI_ESSID = 'HOME-0E52'
WIFI_PASSWD = 'rohan123'
MIN_FREQ = 10
MAX_FREQ = 1000
MIN_SIG = -75
MAX_SIG = -15
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
    buzzer = PWM(Pin(4), freq=1000, duty=20)        

    # Calculate coefs
    a = (MAX_FREQ - MIN_FREQ) / (MAX_SIG - MIN_SIG)
    b = MAX_FREQ - MAX_SIG * a
    while True:    
        sig = _signal_strength(wlan)
        f = int(a * sig + b)        
        buzzer.freq(f)
        buzzer.duty(f // 2)
        print(f'signal strength -> {sig}, freq -> {f}')
        sleep(0.01)

if __name__ == '__main__':
    main()
    