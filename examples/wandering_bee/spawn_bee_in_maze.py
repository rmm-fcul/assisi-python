#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simulated world with a bee in a maze-like environment.
"""

from assisipy import sim
from assisipy import physical

from math import pi

if __name__ == '__main__':
    
    simctrl = sim.Control()

    # Spawn some obstacles into the world.
    l = 5
    w = 2
    wall = ((-l,-w/2),(l,-w/2),(l,w/2),(-l,w/2))
    blue = (0,0,1)
    simctrl.spawn('Physical', 'wall1', (0,-6,0), 
                  polygon = wall,
                  color = blue, height = 1)

    simctrl.spawn('Physical', 'wall2', (5,-1,pi/2), 
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall3', (5,7,0),
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall4', (15,7,pi/2),
                  polygon = wall,
                  color = blue, height = 1)
    simctrl.spawn('Physical', 'wall5', (-7,9,pi/2),
                  polygon = wall,
                  color = blue, height = 1)

    # Spawn the bee.
    simctrl.spawn('Bee', 'bee1', (0,0,0))


