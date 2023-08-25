#!/usr/bin/env python3

# Program to set up the database for RPi environment monitoring data

import sqlite3
from contextlib import closing

OUTPUT_DIR = "/home/weather_station"

with closing(sqlite3.connect(OUTPUT_DIR + "/rpi_env_data.db")) as connection:
	with closing(connection.cursor()) as cursor:
		cursor.execute("CREATE TABLE data (timestamp FLOAT, temperature FLOAT, humidity FLOAT, pressure FLOAT)")
		connection.commit()
