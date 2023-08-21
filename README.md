# RPi_weather_station
Weather station code to run on a Raspberry Pi

This folder contains all the code necessary to run a weather station with a DS18B20 one-wire interface temperature sensor, a DHT22 humidity sensor and a BMP280 pressure sensor. It then sends the data, upon request by the website, to a website built with anvil.works (see your account there for more info)

Two libraries will need to be installed for this code to work:

(1): https://github.com/pimoroni/bmp280-python/tree/master
(2): https://github.com/adafruit/Adafruit_Python_DHT             [NOTE: This is a deprecated library, but still works just fine on RPi]

To set up one-wire communication for the DHT22 and DS18B20, run: sudo nano /boot/config.txt. At the bottom, add dtoverlay=w1-gpio,gpiopin=[GPIO PIN BOARD NUMBER HERE] 

To run this code, first run ./dbsetup.py from the command line to initialise the database.
Then, run ./weather_station.py to start collecting data.
Finally, run ./anvil_data_collection.py to enable the anvil.works website to collect the data for display.

The data is all shown on the website https://creepy-lovable-chinchilla.anvil.app
