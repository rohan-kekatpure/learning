from machine import Pin
from time import sleep

p0 = Pin(0, Pin.OUT)
p16 = Pin(16, Pin.OUT)
while True:
	p0.on()
	p16.on()	
	sleep(0.2)
	p0.off()
	p16.off()
	sleep(0.2)
