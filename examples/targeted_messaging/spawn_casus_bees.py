#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple simulation environment with one Casu and one bee.
"""

from assisipy import sim

from math import pi

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn bees and casus (syntax is 'type', 'name', (x,y,yaw))
    #yaw = 0.0 # this points to the RIGHT
    yaw = pi/2 # this points UP 
    #yaw = -pi/2 # this points down, 
    simctrl.spawn('Casu','casu-ctr',   (0,0, yaw))
    simctrl.spawn('Casu','casu-left',  (-9,0, yaw))
    simctrl.spawn('Casu','casu-right', (+9,0, yaw))

    simctrl.spawn('Bee','Bee-001',(-9+2, 0, pi/2))
    simctrl.spawn('Bee','Bee-002',(+9+0,+2, 2*pi/2))
