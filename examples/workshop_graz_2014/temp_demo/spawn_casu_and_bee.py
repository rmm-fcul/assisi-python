#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple simulation environment with one Casu and one bee.
"""

from assisipy import sim

import random
from math import pi, sin, cos

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Bee and the Casu
    simctrl.spawn('Casu','casu-001',(0,0,0))

    random.seed()
    r_max = 8
    r_min = 2
    r = random.uniform(r_min,r_max)
    a = random.uniform(-pi,pi)
    yaw = random.uniform(-pi,pi)
    simctrl.spawn('Bee','bee-1',(r*cos(a),r*sin(a),yaw))



