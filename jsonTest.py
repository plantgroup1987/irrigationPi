######################Test Receipt of JSON Text##################
###########William Weiner 22Sep2018##############################

import urllib.request
import json
import datetime
import time

url = "http://app.plantgroup.co/api/controllers/Frito-backyard/config/"

response = urllib.request.urlopen(url).read()
resp2 = str(response)[2:len(str(response))-1]
jsonForm = json.loads(resp2)

thingspeakUpdate=((jsonForm["config"]["system"]["sync_interval_seconds"])*1000)
systemClock=(jsonForm["config"]["system"]["system_clock_seconds"])*1000
soilThres=(jsonForm["config"]["user"]["soil_moisture_threshold"])
waterDelay=(jsonForm["config"]["user"]["watering_delay_seconds"])*1000
waterDuration=(jsonForm["config"]["user"]["watering_duration_seconds"])*1000
intervals = len(jsonForm["config"]["user"]["watering_schedule"])
serverTime = jsonForm["local_time"]

#function to convert times into seconds
def secConv(x):
	secs = time.strptime(x,'%H:%M:%S')
	return datetime.timedelta(hours=secs.tm_hour,
		minutes=secs.tm_min,
		seconds=secs.tm_sec).total_seconds()

#interval building

stop={}
begin={}
for i in range(0,intervals):
	stop[i]=secConv((jsonForm["config"]["user"]["watering_schedule"][i]["end"])+":00")
	begin[i]=secConv((jsonForm["config"]["user"]["watering_schedule"][i]["begin"])+":00")

for i in range(0,intervals):
	print("Stop: "+str(stop[i]))
	print("Begin: "+str(begin[i]))

print("Water Delay: "+str(waterDelay))

