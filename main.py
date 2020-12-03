#!/usr/bin/env python

import config

from time import sleep
from objectspeed import checkSpeed

def initial():
    """Run commands on main.py startup"""
    print("Starting...")

#run loop commands
def loop():
    """Run loop commands with a delay set in conifg.py (loopDelay)"""
    checkSpeed()

initial()

while True:
	loop()
	sleep(config.loopDelay)