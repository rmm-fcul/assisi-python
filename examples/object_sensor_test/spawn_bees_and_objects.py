#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple simulation environment with several bees, casus and physical objects.
"""

from assisipy import sim

from math import pi

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Casus
    #simctrl.spawn('Casu','casu-001',(34,0,0))
    simctrl.spawn('Casu','casu-002',(31,5,0))

    # Spawn the physical object
    simctrl.spawn('Physical','box',(28.5,-3,0),polygon=((-1,-1),(1,-1),(1,1),(-1,1)),color=(0,0,1))

    simctrl.spawn('Bee','bee-001',(31,0,0))
    simctrl.spawn('Bee','bee-002',(31,-3,0))
    simctrl.spawn('Bee','bee-003',(28.5,2.5,-pi/4))
