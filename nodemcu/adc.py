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
led = PWM(Pin(5), freq=1000, duty=10)
MINLIGHT = 0
MAXLIGHT = 500

while True:    
    light_level = ldr.read()
    duty = int(2 * (light_level - 1.0))
    duty = max(0, min(duty, 200))
    led.duty(duty)
    print(f'light_level={light_level}, duty={duty}')
    sleep(0.01)