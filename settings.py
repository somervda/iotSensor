import json

class Settings:
    # Persist settings in a gardenSettings.json file
    def __init__(self):
        self._loadSettings()

    def _loadSettings(self):
        try:
            with open("settings.json", "r") as SettingsFile:
                self._settings = json.load(SettingsFile)
        except:
            self._settings = {}

    def getSSID(self):
        return self._settings.get("SSID","")

    def getPASSWORD(self):
        return self._settings.get("PASSWORD","")

    def getLOGGERHOST(self):
        return self._settings.get("LOGGERHOST","")

    def getLOGGERPORT(self):
        return self._settings.get("LOGGERPORT",80)

    def getNTP(self):
        return self._settings.get("NTP","")

    def getSECONDS(self):
        return self._settings.get("SECONDS","37007")

    def getUSER(self):
        return self._settings.get("USER","")

    def getAPPID(self):
        return self._settings.get("APPID",-1)

    def getDEVICEID(self):
        return self._settings.get("DEVICEID",-1)

    def getHOSTNAME(self):
        return self._settings.get("HOSTNAME","")