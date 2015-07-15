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

    # Spawn the Casu
    simctrl.spawn ('Casu', 'casu-001', (0, 0, 0))
    simctrl.spawn ('Bee', 'bee1', (2, 0, 150))
    sleep (1)
    casuBlowing = casu.Casu (name = 'casu-001')
    sleep (1)
    iterations = 0
    while iterations < MAX_ITERATION:
        if iterations % 5 == 0:
            casuBlowing.airflow_standby ()
        else:
            casuBlowing.set_airflow_intensity (iterations % 5)
        iterations += 1
        sleep (1)
    print "Finished spawning"
