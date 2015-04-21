#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A simple demo of bee-casu interaction, with bees rotating about 
# CASUs to periodically trigger IR sensors.

from assisipy import bee
import time 

from math import pi

if __name__ == '__main__':

    # Connect to the bee
    walkers = []
    names = ['Bee-001', 'Bee-002']
    walkers = [bee.Bee(name=n) for n in names]
    
    # Let the bee run in circles
    for i, w in enumerate(walkers):
        f = (i+1) * 1.0 # growth rate

        w.set_vel(f*0.65, f*0.8)

    try:
        while True:
            time.sleep(3.5)
            pass
    except KeyboardInterrupt:
        print "shutting down bees..."
        for w in walkers: 
            w.set_vel(0, 0)



    


            

    
