# Pi version of init.lua
import time
import serial, io, sys
import RPi.GPIO as GPIO

#establish communication w LoRa module
GPIO.setmode(GPIO.BCM)
# set whatever pin is being used for LoRA
LORA = 23
GPIO.setup(LORA,GPIO.OUT)
GPIO.output(LORA,True)
print("LoRa module initiated.")
time.sleep(1)
#set GPIO channel 1 for motor controller as output
# set motor controller pin on ESP and set to off
motorController = 1
GPIO.setup(motorController,GPIO.OUT)
GPIO.output(motorController, GPIO.LOW)
print("Motor controller pin set and switched to off.")

# set network credentials
network = "FritoPendejoWiFi_EXT"
password = "Nb8a6qdq!"

waterDuration = 0
waterDelay = 0
systemClock = 60000
thingspeakUpdate = 20000
soilThres = 0
intervals = 0
currentTime = 0

Bat1 = 0
Bat2 = 0
Temp1 = 0
Temp2 = 0

# ThingSpeak configuration
#write API key for soil moisure probe
controlProbe = "SMQ9OUC4A53N22JE"
#deviceID is MCUid under Controllers in app.plantgroup.co
deviceID = "Frito-backyard"
#write API Key for Valve device 
valve = "XUCAGL8AGAY96RKL"

#watering variabes
waterCount = 0
soilNow = "dry"
delayGo = "no"
delayCount = 0
watering = 0

# variables for Thingspeak population
soilH201 = 0
soilH202 = 0

# Rest API calls http://app.plantgroup.co/api/#/

getURL = "http://app.plantgroup.co/api/controllers/"+str(deviceID)+"/config/"
ts1URL = "http://api.thingspeak.com/update.json?api_key="+str(controlProbe)+"&field1="+str(soilH202)

#WiFi configuration 


