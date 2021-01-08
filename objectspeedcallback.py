import config
from log import log
import time

from gpiozero import Button

logFile = log(config.logFilePath)
first = Button(config.firstInput)
last = Button(config.lastInput)
firstTime = None

def firstEvent():
	"""
	Notes time when an object passes in front of the first light sensor
	"""
	try:
		global firstTime
		if firstTime == None:
			firstTime = time.time()
	except:
		print(f"firstEvent Error; firstTime: {firstTime}")
	
def lastEvent():
	"""
	Compares current time to time when object passed in front of the first light sensor and calculates the speed
	"""
	try:
		global firstTime
		if firstTime != None:
			#print("bottom activated")
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
			newArr = logFile.read("all")
			newArr.insert(0,{"value": final, "time": log.time()})
			logFile.write("all", newArr)
			print(final)
			firstTime = None
	except:
		print(f"lastEvent Error; firstTime: {firstTime}")


def setup():
	# """
	# Checks to see if an object is in front of the light sensors. Runs associated function/s
	# """
	last.when_pressed = lastEvent
	first.when_pressed = firstEvent


def reset(x):
	global firstTime
	if (firstTime != None):
		if (time.time() - firstTime > x):
			print("firstTime back to None")
			firstTime = None
	else:
		firstTime = firstTime
	# except:
	# 	print(f'reset Error; firstTime {firstTime}')