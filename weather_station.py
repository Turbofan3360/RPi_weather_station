#!/usr/bin/env python3

# Importing required modules
import daemon
import sys
import time
import sqlite3
from contextlib import closing

# Importing other python scripts that find temperature and humidity
import AM2302_humidity as AM2302
import DS18B20_temperature as DS18B20
import BMP280_pressure as BMP280

# Initialising variables
current_temperature = 0
current_humidity = 0
current_pressure = 0
LOGGING_ENABLED = True
OUTPUT_DIR = "/home/pi/weather_station"

# Setting where error messages and output goes to when program is daemonized
def reset_stdoutputs():
	oo = open("/tmp/wx_stdout.txt", "at")
	oe = open("/tmp/wx_stderr.txt", "at")

	sys.stdout = oo
	sys.stderr = oe

# Function that puts a message on the screen when called (optional)
def log(message):
	if LOGGING_ENABLED:
		sys.stdout.write(message)
#		print(message)

# Functions to find the humidity, temperature and pressure 5 times and average the readings
def find_humidity():
	counter = 0
	results = []

	while counter != 5:
		results.append(AM2302.get_humidity())
		counter += 1

	total_humidity = results[0] + results[1] + results[2] + results[3] + results[4]
	humidity = total_humidity/5
	humidity = round(humidity, 1)

	return humidity

def find_temperature():
	counter = 0
	results = []

	while counter != 5:
		results.append(DS18B20.get_temperature())
		counter += 1

	total_temperature = results[0] + results[1] + results[2] + results[3] + results[4]
	temperature = total_temperature/5
	temperature = round(temperature, 1)

	return temperature

def find_pressure():
	counter = 0
	results = []

	while counter!= 5:
		results.append(BMP280.get_pressure())
		counter += 1

	total_pressure = results[0] + results[1] + results[2] + results[3] + results[4]
	pressure = total_pressure/5
	pressure = round(pressure, 1)

	return pressure

# Command function that collects humidity and temperature every minute and writes them to data .txt files
def store_data():
	while True:
		log("Reading humidity...")
		current_humidity = find_humidity()

		log("Reading temperature...")
		current_temperature = find_temperature()

		log("Reading pressure...")
		current_pressure = find_pressure()

		timestamp = time.time()

		with closing(sqlite3.connect(OUTPUT_DIR + "/rpi_env_data.db")) as connection:
			with closing(connection.cursor()) as cursor:
				cursor.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (timestamp, current_temperature, current_humidity, current_pressure,))
				connection.commit()

		log("Data entered into database")

		time.sleep(60)

if __name__ == '__main__':
	with daemon.DaemonContext():
		reset_stdoutputs()
		store_data()
