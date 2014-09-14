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
    num_bees = 3
    r_max = 12 # Arena radius is 15
    r_min = 2  # Casu radius is 1
    for i in range(1,num_bees+1):
        r = random.uniform(r_min,r_max)
        a = random.uniform(-pi,pi)
        yaw = random.uniform(-pi,pi)
        simctrl.spawn('Bee','bee-'+str(i),(r*cos(a),r*sin(a),yaw))
 
