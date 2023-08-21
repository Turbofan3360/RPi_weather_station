#!/usr/bin/env python3

import time
from bmp280 import BMP280
from smbus2 import SMBus

def get_pressure():
	# Connecting to the sensor
	bus = SMBus(0)
	bmp280 = BMP280(i2c_dev=bus)

	pressure = bmp280.get_pressure()

	bus.close()

	return pressure

if __name__ == "__main__":
	pressure = get_pressure()
	print("The pressure is {}hPa/mbar".format(pressure))
