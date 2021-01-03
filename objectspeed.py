import config
from log import log
import time

from gpiozero import Button

logFile = log(config.logFilePath)
first = Button(config.firstInput)
last = Button(config.lastInput)
firstActive = False
lastActive = False
firstTime = None

def firstEvent():
	"""
	Notes time when an object passes in front of the first light sensor
	"""
	global firstActive
	global lastActive
	if not(firstActive):
		firstActive = True
		lastActive = False
		global firstTime
		firstTime = time.time()
	
def lastEvent():
	"""
	Compares current time to time when object passed in front of the first light sensor and calculates the speed
	"""
	global lastActive
	global firstTime
	if firstTime != 0 and not(lastActive):
		# calculate fps
		lastActive = True
		timeDiff = time.time() - firstTime
		final = config.lightSensorDistance/timeDiff/12
		print(timeDiff)

		# conversions
		if (config.conversion == 'fpm'):
			final *= 60
			print("fpm")
		elif (config.conversion == 'mph'):
			final = final * (3600/5280)
			print("mph")
		elif (config.conversion != 'fps'):
			final = config.customConversion(final)
			print("custom")

		final = round(final, 2)

		# data is written to logFile
		newArr = logFile.read("all")
		newArr.insert(0,{"value": final, "time": log.time()})
		logFile.write("all", newArr)

		# prints and returns text value
		print(final)
		return final

def checkSpeed():
	"""
	Checks to see if an object is in front of the light sensors. Runs associated functions
	"""
	
	if last.is_pressed:	
		return lastEvent()
	elif first.is_pressed:
		firstEvent()
	else:
		global firstActive
		firstActive = False