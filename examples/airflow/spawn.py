#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple simulation environment with a CASU blowing air.
"""

from assisipy import sim
from assisipy import casu

from time import sleep

MAX_ITERATION = 120

if __name__ == '__main__':

    simctrl = sim.Control ()

    # Spawn the CASUs
    simctrl.spawn ('Casu', 'casu-003', (0,  5, 0))
    simctrl.spawn ('Casu', 'casu-002', (0,  0, 0))
    simctrl.spawn ('Casu', 'casu-001', (0, -5, 0))
    simctrl.spawn ('Bee', 'bee1', (2, 0, 150))
    sleep (1)
    print "Finished spawning"
    casuBlowing = []
    casuBlowing.append (casu.Casu (name = 'casu-001'))
    casuBlowing.append (casu.Casu (name = 'casu-002'))
    casuBlowing.append (casu.Casu (name = 'casu-003'))
    rate = [4, 5, 6]
    rate = [5, 5, 5]
    sleep (1)
    print "CASUs main loop"
    iterations = 0
    while iterations < MAX_ITERATION:
        for idx in range (0, 3):
            if iterations % rate [idx] == 0:
                casuBlowing [idx].airflow_standby ()
            else:
                casuBlowing [idx].set_airflow_intensity (iterations % rate [idx])
        iterations += 1
        sleep (1)
    print "Finished"

