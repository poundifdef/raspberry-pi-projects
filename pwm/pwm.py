"""
Rudimentary manual PWM for a pin
"""

import signal
import sys
import time

import RPi.GPIO as gpio

def signal_handler(signal, frame):
        gpio.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)

denom = 0.006
rate = 5.0

on = (rate / 100) * denom
off = ((100 - rate) / 100) * denom
print on, off

rate = .5
#rate = 0.013

# upper bound
# rate = 0.001

rateR = 40

while True:
        for i in range(1, 100):
                if i <= rateR:
                        gpio.output(24, gpio.HIGH)
                else:   
                        gpio.output(24, gpio.LOW)
                time.sleep(0.0001)

