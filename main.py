#!/usr/bin/env python3
# chmod +x main.py

import config

from time import sleep
from objectspeed import checkSpeed
import objectspeedcallback as osc

def initial():
    """Run commands on main.py startup"""
    print("Starting...")
    if (not(config.mainRunsLoop)):
        osc.setup()

#run loop commands
def loop():
    """Run loop commands with a delay set in conifg.py (loopDelay)"""
    if (config.mainRunsLoop):
        checkSpeed()
    else: 
        osc.reset(config.timeoutTime) 

initial()

while True:
	loop()
	sleep(config.loopDelay)