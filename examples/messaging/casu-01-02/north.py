#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Control of the northern casu

from assisipy import casu

class CasuController:

    def __init__(self, rtc_file):
        self.__casu = casu.Casu(rtc_file)

    def handle_message(self):
        """
        Changes color to red, when a bee is detected by one of the proximity sensors.
        Notifies neighbor.
        """
        msg = self.__casu.read_message()
        if msg:
            if  msg['data'] == 'On':
                self.__casu.set_diagnostic_led_rgb(1, 0, 0, casu.DLED_TOP)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
            

    def loop(self):
        """
        Do some smart control stuff...
        """
        while True:
            self.handle_message()

if __name__ == '__main__':

    ctrl = CasuController('casu.rtc')

    ctrl.loop()

