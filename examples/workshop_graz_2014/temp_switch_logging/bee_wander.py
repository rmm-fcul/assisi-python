#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple bee wander behavior.

Running the program:

$ ./bee_wander beename

Makes the bee "beename" wander in the simulator.
"""

import sys
import random
from time import sleep

from assisipy import bee

def go_straight(bee):
    vel = 0.5
    bee.set_vel(vel,vel)

def turn_random(bee):
    vel = 0.2
    direction = random.choice([-1,1])
    bee.set_vel(direction*vel, -direction*vel)
    sleep(random.uniform(1,5))

if __name__ == '__main__':

    
    mybee = bee.Bee(name=sys.argv[1])

    random.seed()
    count = 0

    # Naive wander control loop
    while True:
        while mybee.get_range(bee.OBJECT_FRONT) < 2:
            turn_random(mybee)
        go_straight(mybee)
        count += 1
        if count % 10 == 0:
            print("I'm feeling {0} degrees.".format(mybee.get_temp()))
        sleep(0.1)

