from machine import Pin, PWM
from time import sleep

# Initialize pwm
pwm0 = PWM(Pin(0), freq=1000, duty=1)
j = 1
while True:
	while j < 1000:
		pwm0.duty(j)		
		sleep(0.002)
		j += 1

	while j > 0:
		pwm0.duty(j)		
		sleep(0.002)
		j -= 1			


