from microWebCli import MicroWebCli
from settings import Settings
import socket
import json
import time


class Web:
    _quiet = True

    def __init__(self,quiet=True):
        not self._quiet and print('__init__',quiet)
        self._settings = Settings()
        self._quiet = quiet


    def sendToLogger(self,values={}):
        not self._quiet and print("sendToLogger",values)
        iotData = {}
        iotData["user"] = self._settings.getUSER()
        iotData["appID"] = self._settings.getAPPID()
        iotData["deviceID"] = self._settings.getDEVICEID()
        iotData["sensorTimestamp"] = time.time()
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
        else:
            not self._quiet  and print(
                'Fail Response:'  ,resp.GetStatusCode(),resp.ReadContent())
        return resp.GetStatusCode()
        # except:
        #     return -1


    def sendToLogger2(self,values={}):
        not self._quiet and print("sendToLogger2",values)
        addr = socket.getaddrinfo(self._settings.getLOGGERHOST(), self._settings.getLOGGERPORT())[0][-1]
        not self._quiet and print("ADDR:",addr)
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % ("hello", self._settings.getLOGGERHOST() + ":" + str(self._settings.getLOGGERPORT())), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        s.close()
        return ""