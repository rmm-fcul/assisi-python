#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi

from assisipy import sim


if __name__=='__main__':
    
    simctrl = sim.Control()

    simctrl.spawn('Casu','casu-003',(0,-2,0))
    simctrl.spawn('Casu','casu-004',(0,2,0))

