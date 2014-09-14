#!/usr/bin/env python
# A program that spawns one casu and a bunch of bees (at random locations)

import random
from math import pi, sin, cos

from  assisipy import sim


if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Casu in the middle
    simctrl.spawn('Casu','casu-001',(0,0,0))


    # Spawn bees at random locations
    random.seed()
    num_bees = 5
    r_max = 10 # Arena radius
    for i in range(num_bees):
        r = random.uniform(-r_max,r_max)
        a = random.uniform(-pi,pi)
        yaw = random.uniform(-pi,pi)
        simctrl.spawn('Bee','bee-'+str(i),(r*cos(a),r*sin(a),yaw))
 
