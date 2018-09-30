##########Testing Multithreading##################
########William Weiner 29Sep2018##################

import threading
import serial
import time
import datetime
import ast
import urllib.request
import json

#from jsonTest import thingspeakUpdate

thingspeakUpdate=20
systemClock=60
soilThresh=""
waterDelay=0
waterDuration=0
intervals=0
serverTime=0
stop={}
begin={}

#write APIKey for piTest channel
tsAPI='PILI04S0O4KYN8VO'

url = "http://app.plantgroup.co/api/controllers/Frito-backyard/config/"

ser = serial.Serial(port='/dev/ttyAMA0',
			baudrate=115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			)
dict={'moisture':0,'temp':0,'bat':0,'ID':0}
x=""

#reads serial connection incoming data from the LoRa receiver
def serialRead():
	while True:
		global x
		x=ser.readline()
		global dict
		dict=x.decode('utf-8')
		if len(x)>0:
			dict=ast.literal_eval(dict)
			print(dict)
			print(dict['moisture'])
			x=""

count = 0
def foreground():
        global count
        global systemClock
        global soilThresh
        global waterDelay
        global waterDuration
        global intervals
        global serverTime
        global stop
        global begin
        while True:
                count=count+1
                print("This is cycle  "+str(count))
                print("SystemClock: "+str(systemClock))
                print("soilThresh: "+soilThresh)
                print("waterDelay: "+str(waterDelay))
                print("waterDuration: "+str(waterDuration))
                print("ServerTime: "+str(serverTime))
                for i in range(0,intervals):
                        print("Stop: "+str(stop[i]))
                        print("Begin: "+str(begin[i]))
                time.sleep(30)

#section that updates thingspeak website
def tsUpdate():
	global dict
	global tsAPI
	global thingspeakUpdate
	while True:
		tsURL = 'https://api.thingspeak.com/update?api_key='+tsAPI+'&field1='+str(dict['moisture'])+'&field2='+str(dict['temp'])+'&field3='+str(dict['bat'])
		urllib.request.urlopen(tsURL)
		print(thingspeakUpdate)
		time.sleep(thingspeakUpdate)

#function to convert times into seconds
def secConv(x):
	secs = time.strptime(x,'%H:%M:%S')
	return datetime.timedelta(hours=secs.tm_hour,
		minutes=secs.tm_min,
		seconds=secs.tm_sec).total_seconds()

def intervals():
        global url
        global thingspeakUpdate
        global systemClock
        global soilThresh
        global waterDelay
        global waterDuration
        global intervals
        global serverTime
        global stop
        global begin
        while True:
                try:
                        response = urllib.request.urlopen(url).read()
                except urllib.error.HTTPError as err:
                        print("There was an error calling this URL")
                        print(err)
                resp2=response.decode('utf-8')
                jsonForm = json.loads(resp2)
        
                thingspeakUpdate=((jsonForm["config"]["system"]["sync_interval_seconds"]))
                systemClock=(jsonForm["config"]["system"]["system_clock_seconds"])
                soilThresh=(jsonForm["config"]["user"]["soil_moisture_threshold"])
                waterDelay=(jsonForm["config"]["user"]["watering_delay_seconds"])
                waterDuration=(jsonForm["config"]["user"]["watering_duration_seconds"])
                intervals = len(jsonForm["config"]["user"]["watering_schedule"])
                serverTime = jsonForm["local_time"]

                #interval building

                for i in range(0,intervals):
                        stop[i]=secConv((jsonForm["config"]["user"]["watering_schedule"][i]["end"])+":00")
                        begin[i]=secConv((jsonForm["config"]["user"]["watering_schedule"][i]["begin"])+":00")

                #for i in range(0,intervals):
                        #print("Stop: "+str(stop[i]))
                        #print("Begin: "+str(begin[i]))
                time.sleep(60)
        
		
b = threading.Thread(name='serialRead',target=serialRead)
f = threading.Thread(name='foreground',target=foreground)
ts = threading.Thread(name='tsUpdate',target=tsUpdate)
interval = threading.Thread(name='intervals',target=intervals)

b.start()
f.start()
ts.start()
interval.start()
