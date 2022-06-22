from time import sleep
from machine import SPI, Pin
import random

def segments_to_decimal(segment_str):
    places = 'PGFEDCBA'    
    bin_str = ''.join([str(int(p in segment_str)) for p in places])
    dec = int(bin_str, 2)
    return dec

DIGITS = {
    '0': segments_to_decimal('AFEDCB'),    
    '1': segments_to_decimal('BC'),
    '2': segments_to_decimal('ABGED'),
    '3': segments_to_decimal('ABGCD'),
    '4': segments_to_decimal('FGBC'),
    '5': segments_to_decimal('AFGCD'),
    '6': segments_to_decimal('AFEDCG'),
    '7': segments_to_decimal('ABC'),
    '8': segments_to_decimal('ABCDEFGH'),
    '9': segments_to_decimal('ABCFG'),
    'p': segments_to_decimal('P'),
}

def send(value, hspi, latch_pin):
    bval = value.to_bytes(1, 'big')
    latch_pin.value(0)    
    hspi.write(bval)                
    latch_pin.value(1)


def display(val, digit_selectors, hspi, latch, n=4):
    if (val < 0) or (val > 9999):
        return
    s = str(val)    
    # Make sure len(s) is 4, prepend 0s if necessary
    s = ('0000' + s)[-n:]  
    digits = list(s)

    for d, p in zip(digits, digit_selectors):
        p.value(0)        
        send(DIGITS[d], hspi, latch)                    
        p.value(1)        

def main():   

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

    # Digit selectors
    p2 = Pin(PINOUT['D1'], Pin.OUT)
    p3 = Pin(PINOUT['D2'], Pin.OUT)
    p4 = Pin(PINOUT['D3'], Pin.OUT)
    p1 = Pin(PINOUT['D4'], Pin.OUT)

    # Initialize HSPI
    hspi = SPI(1, baudrate=115200)
    latch = Pin(PINOUT['D8'], Pin.OUT)    
    digit_selectors = [p1, p2, p3, p4]    
    while True:
        n = random.getrandbits(8)
        # print(n)
        i = 0
        while i < 50:
            display(n, digit_selectors, hspi, latch)
            i += 1     


if __name__ == '__main__':
    main()