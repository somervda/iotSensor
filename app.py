#!/usr/bin/python3
from settings import Settings
import network
import ntptime
import time
from  machine import Pin 
import machine
import json
import os
from web import Web

import micropython

from sensor import Sensor

def dir_exists(dirName):
    try:
        return (os.stat(dirName)[0] & 0x4000) != 0
    except OSError:
        return False


# Set up quiet mode
_quiet = False

# Load Setting
settings = Settings()

# Network Error Counter
network_error_count = 0

# Set up LED
led = Pin("LED", Pin.OUT)
led.on()

# Connect to network and get the NTP time

wlan = network.WLAN(network.STA_IF)
print("Connecting to " + settings.getSSID() + ":")
wlan.active(True)
network.hostname(settings.getHOSTNAME())
# wlan.ifconfig(('192.168.1.30', '255.255.255.0',
#                '192.168.1.1', '192.168.1.1'))
wlan.connect(settings.getSSID(), settings.getPASSWORD())
while not wlan.isconnected() and wlan.status() >= 0:
    # Slow LED flash while connecting
    print(".", end="")
    led.off()
    time.sleep(0.5)
    led.on()
    time.sleep(.5)

time.sleep(2)
print("Connected! ifconfig:",wlan.ifconfig()[0],wlan.ifconfig()[1],wlan.ifconfig()[2],wlan.ifconfig()[3])
# Short delay before getting ntp time
# There is a known timing bug with this so try again
# if it fails.
try:
    ntptime.host = settings.getNTP()
    print(ntptime.host)
    ntptime.timeout = 2
    ntptime.settime()
except:
    print("ntptime error! Rebooting...")
    time.sleep(1)
    machine.reset()



print("UMT time：%s" % str(time.localtime()))
for x in range(0, 10):
    # Quick flash to indicate we are connected
    time.sleep(.05)
    led.on()
    time.sleep(.05)

    led.off()

if not dir_exists("data"):
    os.mkdir("data")
web = Web(quiet=_quiet)
sensor = Sensor(quiet=_quiet)


while True:
    # Main event loop. Check if it is time to collect sensor data
    # and check if there is sensor data waiting to be written to
    # the iotCache service

    not _quiet and print(sensor.getData())
    # If a sensorData file is present then send it the iotCache service
    for fileName in os.listdir("data"):
        with open("data/" + fileName, "r") as iotDataFile:
            not _quiet and print("Sending ",fileName," to iotCache...")
            iotData = json.load(iotDataFile)
            result = web.sendToCacheServer(iotData)
            os.remove("data/" + fileName)
            # Only process one file per event loop
            break
    time.sleep(5)
    



