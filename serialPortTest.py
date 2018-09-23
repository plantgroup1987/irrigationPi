#!/usr/bin/env python

##############First Attempt at Lua to Python#######################
###########William Weiner 20Sep2018################################

import time
import serial

ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
)

while 1:
	x=ser.readline()
	if len(x)>0:
		print(x)
        sensorBattery = jsonForm[0]
		time.sleep(60)


