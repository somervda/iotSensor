#!/usr/bin/python3
import machine
import bme280
import time
from settings import Settings
import json


# Collects the sensor data and returns it as a dictionary of iotData

class Sensor:
    _quiet = True
    _i2c = None
    _bme = None
    _settings = None
    def __init__(self,quiet=True):
        not quiet and print('__init__',quiet)
        self._quiet = quiet
        self._settings = Settings()
        try:
            self._i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
            self._bme=bme280.BME280(i2c=self._i2c)
        except Exception as error:
            not self._quiet and print("An i2c exception occurred:", error)
            not self._quiet and print("Restarting...")
            machine.reset()

    def getData(self):
        # work out how long to wait for next data collection
        lastCollectionTime = self.getLastCollectionTime()
        collectionInterval = self._settings.getSECONDS()
        if time.time() < collectionInterval + lastCollectionTime:
            return False
        else:
            # get the sensor data (Replay with your particular data collection)
            t,p,h=self._bme.read_compensated_data()
            centigrade=t/100
            p /=25600
            h /= 1024
            iotData = {}
            iotData["celsius"] = centigrade
            #  Note: inMg = pi/33.86
            iotData["hPa"] = p
            iotData["humidity"] = h
            iotData["sensorTimestamp"] = time.time()

            self.saveLastCollectionTime()
            self.saveIOTData(iotData)
            return True

    def saveIOTData(self,iotData):
        # Save the iotData to data folder
        # We persist this info incase we do a restart and have not sent data yet
        with open("data/" + str(time.time()) + ".json", "w") as sensor_data_file:
            sensor_data_file.write(json.dumps(iotData))

    def saveLastCollectionTime(self):
        # Save the time of the last data collection
        # We persist this info incase we do a restart 
        with open("lastCollectionTime.dat", "w") as lastCollectionTime_file:
            lastCollectionTime_file.write(str(time.time()))

    def getLastCollectionTime(self):
        # get the time of the last data collection
        lastCollectionTime=0
        try:
            with open("lastCollectionTime.dat", "r") as lastCollectionTime_file:
                lastCollectionTime = int(lastCollectionTime_file.read())
        except Exception as error:
            not self._quiet and print("lastCollectionTime exception occurred:", error)
        return lastCollectionTime




