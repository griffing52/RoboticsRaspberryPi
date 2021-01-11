# RoboticsRaspberryPi

# Doc and code is not up to date
## Note for future: https://raspberrypi.stackexchange.com/questions/89732/run-a-script-at-shutdown-on-raspbian
## maybe make it so everytime raspberry pi is shutdown, log file is sent as an email 

2 light sensors display the speed of an object moving in front of it in feet per second (this can be changed). The 5 most recent speeds are displayed on the user interface.

# Setup

From the two light sensors, plug the red wires into 5v and the black wires into ground on the Raspberry Pi. Plug the white wire from the the sensor that will activate first as the object passes through to whatever IO pin is written in the config.py file (default 23). Do the same for the white wire from the light sensor which will have the object go past it last (default 24).

The pinout for the Raspberry Pi 3 can be found [here](https://www.raspberrypi.org/documentation/usage/gpio/)

# Framework

There are 3 important files: [main.py](#mainpy), [config.py](#configpy), and [userinterface.py](#userinterfacepy). 

## main.py

### What it does

This file is the main loop. All commands apart from the user interface are run through here.

### How to use

  1. Ensure importation of your command or function.
  2. Add function that is supposed to loop in the main.py loop function

### Example

```python
from objectspeed import checkSpeed
```
```python
def loop():
  if (config.mainRunsLoop):
        checkSpeed() # if config is set to run check speed, it will add checkSpeed function to the loop from objectspeed file
    else: 
        osc.reset(config.timeoutTime) # if config is set to run sensor callback function, a timeout is set to reset variables after config.timeoutTime in seconds
```

## config.py

### What it does

A single place to store variables which affect how the program runs

### How to use
  
  Change variable values to change how functions work

### Example

This is a variable used in the objectspeed file. Changing this variable will specify the distance between the two light sensors, which is necessary for the calculation of speed
```python
lightSensorDistance = 3 # distance in inches, 1 hole separation = 3 inches, 0 hole = 1.5 inches
```

## userinterface.py

### What it does

The information which the user can see at a glance. This updates on a different loop compared to the main.py loop.

### How to use

  1. Create text using guizero library
  2. Change text using guizero library in loop function

### Example

```python
text4 = Text(app, "xx", grid=[5, 0]) # creation of text
```
```python
def loop():
    recents = read('recents') # views content of array in log.json file
    text4.value = recents[-1]["value"] # sets text element to value of the array's last element
```
# Notes for further development

If changes are made to main.py or userinterace.py and it is no longer running on startup, go into cmd and cd into the files path. Then run these commands:
```bash
chmod +x main.py
chmod +x userinterface.py
```
