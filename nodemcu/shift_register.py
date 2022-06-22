from machine import SPI, Pin
from time import sleep

def send(value, hspi, latch_pin):
	bval = value.to_bytes(1, 'big')
	hspi.write(bval)
	latch_pin.value(0)
	latch_pin.value(1)


def main():
	# Set clock frequency. This is equivalent to the baud rate 
	# of the SPI interface. This DOES NOT need to be equal to 
	# the baudrate of the USB to serial driver.
	clk_freq = 115200  # Reduce to view the clock pulses

	# Create the Hardware SPI interface
	hspi = SPI(1, baudrate=clk_freq)

	# Create a latch pin
	latch_pin = Pin(15, Pin.OUT)	

	# Send data

	try:
		while True:
			for i in range(255):
				send(i, hspi, latch_pin)
				sleep(0.05)
	finally:
		send(0, hspi, latch_pin)


if __name__ == '__main__':
	main()
