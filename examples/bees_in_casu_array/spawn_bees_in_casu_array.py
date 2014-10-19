#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simulated world featuring 36 Casus and 36 bees.
"""

from assisipy import sim

from math import pi, sin, cos
from random import random
import threading

if __name__ == '__main__':

    simctrl = sim.Control()

    # Parameters of the CASU array.
    casu_rows = 6
    casu_cols = 6
    casu_dist = 8
    num_bees = 36

    radius = 40 # Arena radius
    
    # Spawn the Casus and run their controllers
    casus = []
    x = range(-int(casu_dist*casu_cols/2), int(casu_dist*(casu_cols+1)/2), casu_dist)
    y = range(-int(casu_dist*casu_rows/2), int(casu_dist*(casu_rows+1)/2), casu_dist)
    for i in range(casu_rows):
        for j in range(casu_cols):
            simctrl.spawn('Casu', 'Casu-0{0}-0{1}'.format(i,j), (x[i],y[j],0))

    # Spawn the bees at randomly generated poses and let them run :)
    bees = []
    for i in range(1,num_bees+1):
        d = 0.9*radius*random()
        a = 2*pi*random()
        if i < 10:
            simctrl.spawn('Bee', 'Bee-00{0}'.format(i), (d*cos(a), d*sin(a), a))
        else:
            simctrl.spawn('Bee', 'Bee-0{0}'.format(i), (d*cos(a), d*sin(a), a))



        
