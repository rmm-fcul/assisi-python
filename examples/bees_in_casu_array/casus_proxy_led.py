#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Identical controllers for 36 casus. Every casu lights its diagnostic led red or green,
when an object approaches it from the front, or back, respectively.
"""

from assisipy import casu

from math import pi, sin, cos
from random import random
import threading

class CasuController:
    """ 
    A demo Casu controller.
    Implements a simple bee-detecting behavior.
    """

    def __init__(self, casu_name):
        self.__casu = casu.Casu(name = casu_name)
        self.__thread = threading.Thread(target=self.react_to_bees)
        self.__thread.daemon = True
        self.__thread.start()

    def react_to_bees(self):
        """ 
        Changes Casu color to red, when a bee is detected 
        in front of the Casu, and to Green, when a bee is 
        detected behind a Casu.
        """
        while True:
            if self.__casu.get_range(casu.IR_F) < 2:
                self.__casu.set_diagnostic_led_rgb(1, 0, 0)
            elif self.__casu.get_range(casu.IR_B) < 2:
                self.__casu.set_diagnostic_led_rgb(0, 1, 0)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)

if __name__ == '__main__':

    # Parameters of the CASU array.
    casu_rows = 6
    casu_cols = 6

    # Spawn the Casus and run their controllers
    casus = []
    for i in range(casu_rows):
        for j in range(casu_cols):
            casus.append(CasuController('Casu-0{0}-0{1}'.format(i,j)))

    print('All Casus connected!')
    
    # Prevent the program from exiting
    while True:
        pass

        
