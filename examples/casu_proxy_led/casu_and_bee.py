#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A simple demo of bee-casu interaction

from assisipy import sim
from assisipy import bee
from assisipy import casu

from math import pi

class CasuController:
    """ A demo Casu controller.
        Implements a simple bee-detecting behavior.
    """

    def __init__(self, casu_name):
        self.__casu = casu.Casu(name = casu_name)

    def react_to_bees(self):
        """ 
            Changes Casu color to red, when a bee is detected in front of the Casu,
            and to Green, when a bee is detected behind a Casu.
        """
        while True:
            if self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
            elif self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 1, 0)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)

if __name__ == '__main__':

    simctrl = sim.Control()
    
    # Spawn the Bee and the Casu
    simctrl.spawn('Casu','casu1',(0,0,0))
    simctrl.spawn('Bee','bee1',(2,0,pi/2))

    ctrl = CasuController('casu1')

    bee1 = bee.Bee(name='bee1')
    
    # Let the bee run in circles
    bee1.set_vel(0.65,0.8)
    
    ctrl.react_to_bees()


            

    
