#!/usr/bin/env python3

# Importing required modules
import anvil.server
import daemon
import sys
import sqlite3
import time
from contextlib import closing

# Setting variables
LOGGING = True
OUTPUT_DIR = "/home/pi/weather_station"

# Setting where error messages and output goes to when the program is daemonized
def reset_stdoutputs():
	oo = open("/tmp/an_stdout.txt", "at")
	oe = open("/tmp/an_stderr.txt", "at")

	sys.stdout = oo
	sys.stderr = oe

# Function that prints a message (log) to the screen when you want
def log(message):
	if LOGGING:
		sys.stdout.write(message)

# Function that query the database for the temperature or humidity where the timestamp is more recent than the time now minus the requested length of data
@anvil.server.callable
def return_data(data_time_length):
	current_time = time.time()
	time_period = current_time - data_time_length

	with closing(sqlite3.connect(OUTPUT_DIR + "/rpi_env_data.db")) as connection:
		with closing(connection.cursor()) as cursor:
			data = cursor.execute("SELECT timestamp, temperature, humidity, pressure FROM data WHERE timestamp > ?", (time_period,)).fetchall()

	log("Data collected")

	return data

if __name__ == "__main__":
	with daemon.DaemonContext():
		reset_stdoutputs()
		anvil.server.connect(xyz)
#		change "xyz" above to your anvil.works server ID
		anvil.server.wait_forever()
#	print(return_data(300))
