#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Control of the central Casu

from assisipy import casu

class CasuController:

    def __init__(self, rtc_file):
        self.__casu = casu.Casu(rtc_file)
        self.old_state = 'Off'
        self.state = 'Off'

    def react_to_bees(self):
        """
        Changes color to red, when a bee is detected by one of the proximity sensors.
        Notifies neighbor.
        """
        while True:
            if self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(1, 0, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Red On'
            elif (self.__casu.get_range(casu.IR_NE) < 2 or
                  self.__casu.get_range(casu.IR_SE) < 2):
                self.__casu.set_diagnostic_led_rgb(0, 1, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Green On'
            elif self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(0, 0, 1, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Blue On'
            elif (self.__casu.get_range(casu.IR_SW) < 2 or
                  self.__casu.get_range(casu.IR_NW) < 2):
                self.__casu.set_diagnostic_led_rgb(1, 1, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Yellow On'
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'

            if self.old_state != self.state:
                if self.old_state == 'Red On':
                    self.__casu.send_message('north', 'Off')
                elif self.old_state == 'Green On':
                    self.__casu.send_message('east', 'Off')
                elif self.old_state == 'Blue On':
                    self.__casu.send_message('south', 'Off')
                elif self.old_state == 'Yellow On':
                    self.__casu.send_message('west', 'Off')

                if self.state == 'Red On':
                    self.__casu.send_message('north', 'On')
                if self.state == 'Green On':
                    self.__casu.send_message('east', 'On')
                if self.state == 'Blue On':
                    self.__casu.send_message('south', 'On')
                if self.state == 'Yellow On':
                    self.__casu.send_message('west', 'On')



if __name__ == '__main__':

    ctrl = CasuController('casu.rtc')

    ctrl.react_to_bees()


        
        
