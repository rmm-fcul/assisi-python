#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple demo of Casu interaction.
The Casu diagnostic LED lights red, when an object appears in front,
and it lights green, when an object appears behind it.

This demo is suitable for deployment on the Casu hardware (BeagleBone).
Just copy this .py file and the casu.rtc file to a folder on the 
BeagleBone and run it.
"""

from assisipy import casu

class CasuController:
    """ 
    A demo Casu controller.
    Implements a simple bee-detecting behavior.
    """

    def __init__(self, rtc_file):
        self.__casu = casu.Casu(rtc_file)

    def react_to_bees(self):
        """ 
            Changes Casu color to red, when a bee is detected in front of the Casu,
            and to Green, when a bee is detected behind a Casu.
        """
        while True:
            if self.__casu.get_range(casu.IR_F) < 2:
                self.__casu.set_diagnostic_led_rgb(g=1)
            elif self.__casu.get_range(casu.IR_B) < 2:
                self.__casu.set_diagnostic_led_rgb(r=1)
            else:
                self.__casu.diagnostic_led_standby()

if __name__ == '__main__':

    ctrl = CasuController('casu.rtc')

    # Run the Casu control program.
    ctrl.react_to_bees()


            

    
