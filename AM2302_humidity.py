#!/usr/bin/env python3

import Adafruit_DHT
import time

def get_humidity():
	sensor = Adafruit_DHT.AM2302
	pin = 17

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	while not humidity:
		time.sleep(0.5)
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	return humidity

if __name__ == "__main__":
	humidity = get_humidity()
	humidity = round(humidity, 1)
#	temperature = round(temperature, 1)
	print("The humidity is {}%".format(humidity))
#	print("The humidity is {}%, and the temperature is {}*C".format(humidity, temperature))
# Un-hash the two hashed out lines above, hash out the first print statement and add temperature to the return statement of get_humidity() to get both temperature and humidity printed to the screen
