#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple simulation environment with one Casu and one bee.
"""

from assisipy import sim

from math import pi

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Bee and the Casu
    simctrl.spawn('Casu','Casu-02-02',(0,0,pi/2))
    simctrl.spawn('Casu','Casu-01-02',(0,9,pi/2))
    simctrl.spawn('Casu','Casu-02-01',(-9,0,pi/2))
    simctrl.spawn('Casu','Casu-02-03',(9,0,pi/2))
    simctrl.spawn('Casu','Casu-03-02',(0,-9,pi/2))
    simctrl.spawn('Bee','Bee-001',(2,0,pi/2))
