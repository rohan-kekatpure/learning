"""
This is the example code for reading analog input from 
ESP8266. 

We attach an LDR to Pin 0 (the analog IN pin) and change
the intensity of the LED on pin 5 using PWM.
"""
from time import sleep
from machine import ADC, PWM, Pin
from math import log, exp

ldr = ADC(0)
led = PWM(Pin(5), freq=4000, duty=100)

while True:    
    light_level = ldr.read()
    freq = int(2 * (light_level - 1.0))
    freq = max(0, min(freq, 1000))

    if freq == 0:
        led.duty(0)
    else:
        led.freq(freq)
        # led.duty(freq//4)
        led.duty(200)        
    
    print(f'light_level={light_level}, freq={freq}')
    sleep(0.01)