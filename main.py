#!/usr/bin/python3
from machine import Pin

button = Pin(15, Pin.IN, Pin.PULL_UP)

# Will start main app automatically based on 
# switch across pin 15 and ground  value

if button.value() == 0:
    import app