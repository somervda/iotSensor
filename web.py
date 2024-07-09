#!/usr/bin/python3
from microWebCli import MicroWebCli
from settings import Settings
import socket
import json
import time
import machine


class Web:
    _quiet = True

    def __init__(self,quiet=True):
        not quiet and print('__init__',quiet)
        self._settings = Settings()
        self._quiet = quiet


    def sendToCacheServer(self,values={}):
        not self._quiet and print("sendToLogger",values)
        retryCount = 0
        while True:
            try:
                # Build the iotData dictionary with sensor data  and device specific information
                iotData = {}
                iotData["user"] = self._settings.getUSER()
                iotData["appID"] = self._settings.getAPPID()
                iotData["deviceID"] = self._settings.getDEVICEID()
                for key in values:
                    iotData[key] = values[key]
                not self._quiet and print("iotData:",json.dumps(iotData))
                url = "http://"  + self._settings.getLOGGERHOST() + ":" + str(self._settings.getLOGGERPORT()) + '/write?iotData=' + json.dumps(iotData)
                wCli = MicroWebCli(url)
                # wCli.QueryParams['iotData'] =  '{"temp":34}'
                not self._quiet and print("url:",url)
                # try:
                wCli.OpenRequest()
                buf = memoryview(bytearray(1024))
                resp = wCli.GetResponse()
                if resp.IsSuccess():
                    if not resp.IsClosed():
                        x = resp.ReadContentInto(buf)
                        if x < len(buf):
                            buf = buf[:x]
                        not self._quiet  and print(str(bytearray(buf), "utf-8"))
                    not self._quiet  and print(
                        'Ok Response:' ,resp.GetStatusCode(),resp.ReadContent())
                    return True
                else:
                    not self._quiet  and print(
                        'Fail Response:'  ,resp.GetStatusCode(),resp.ReadContent(),retryCount)
            except Exception as error:
                # handle the exception
                 not self._quiet  and print("An exception occurred:", error, retryCount)
            # Loop to retry 
            retryCount+=1
            time.sleep(5)
            if retryCount>5:
                # Tried a few times and it not working so restart microcontroller
                not self._quiet  and print("Retry count exceeded - restarting...")
                time.sleep(1)
                machine.reset()



    # def sendToLogger2(self,values={}):
    #     not self._quiet and print("sendToLogger2",values)
    #     addr = socket.getaddrinfo(self._settings.getLOGGERHOST(), self._settings.getLOGGERPORT())[0][-1]
    #     not self._quiet and print("ADDR:",addr)
    #     s = socket.socket()
    #     s.connect(addr)
    #     s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % ("hello", self._settings.getLOGGERHOST() + ":" + str(self._settings.getLOGGERPORT())), 'utf8'))
    #     while True:
    #         data = s.recv(100)
    #         if data:
    #             print(str(data, 'utf8'), end='')
    #         else:
    #             break
    #     s.close()
    #     return ""