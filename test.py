# from sensor import Sensor

# s=Sensor(quiet=False)
# print(s.getData())

import machine
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
device = i2c.scan()
print(device)
