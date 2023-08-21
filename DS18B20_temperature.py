#!/usr/bin/python3

import glob
import time
import os

def setup():
	os.system("modprobe w1-gpio")
	os.system("modprobe w1-therm")

	therm_folder = glob.glob("/sys/bus/w1/devices/28*")[0]
	therm_file = therm_folder + "/w1_slave"

	return therm_file

def get_temp_data(therm_file):
	f = open(therm_file, "r")
	therm_data = f.readlines()
	f.close()
	return therm_data

def get_temperature():
	therm_file = setup()

	time.sleep(0.5)
	therm_data = get_temp_data(therm_file)

	while not therm_data:
		time.sleep(0.5)
		therm_data = get_temp_data(therm_file)

	therm_data = therm_data[1]
	temp_pos = therm_data.find("t=")

	if temp_pos != -1:
		temp = therm_data[(temp_pos+2):]
		temp = temp.strip("/n")
		temp = float(temp)/1000
	else:
		temp = 0

	return temp


if __name__ == "__main__":
	temp = get_temperature()
	print ("The temperature is", temp, "degrees celsius")
