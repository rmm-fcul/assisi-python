#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for all "spoke" CASUs, they emit when reading one specific directional
# IR sensor.


from assisipy import casu
import argparse, os
from hub import find_comm_links
import time

class CasuController:

    def __init__(self, rtc_file, direction, verb=False):
        self.__casu = casu.Casu(rtc_file)
        self._ctr_dir = direction
        self.old_state = 'Off'
        self.state = 'Off'
        self.verb = verb
        self._comm_links = find_comm_links(rtc_file, verb=self.verb)

    def stop(self):
        self.__casu.stop()

    def handle_message(self):
        """
        Changes color to red, when a bee is detected by one of the proximity sensors.
        Notifies neighbor.
        """
        msg = self.__casu.read_message()
        if msg:
            if  msg['data'] == 'On':
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
            
    def send_msg(self):

        while True:
            # North side
            if self._ctr_dir == 'N' and  self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 0, 0)
                self.old_state = self.state
                self.state = 'Red On'
            # East
            elif self._ctr_dir == 'E' and ((self.__casu.get_range(casu.IR_NE) <
                2 or self.__casu.get_range(casu.IR_SE) < 2)):
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 1, 0)
                self.old_state = self.state
                self.state = 'Green On'
            # West
            elif self._ctr_dir == 'W' and self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 0, 0, 1)
                self.old_state = self.state
                self.state = 'Blue On'
            # South
            elif self._ctr_dir == 'S' and ((self.__casu.get_range(casu.IR_SW) <
                2 or self.__casu.get_range(casu.IR_NW) < 2)):
                self.__casu.set_diagnostic_led_rgb(casu.DLED_TOP, 1, 1, 0)
                self.old_state = self.state
                self.state = 'Yellow On'
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'

            if self.old_state != self.state:
                if self.old_state == 'Red On':
                    self.__casu.send_message('collector', 'Off')
                elif self.old_state == 'Green On':
                    self.__casu.send_message('collector', 'Off')
                elif self.old_state == 'Blue On':
                    self.__casu.send_message('collector', 'Off')
                elif self.old_state == 'Yellow On':
                    self.__casu.send_message('collector', 'Off')

                if self.state == 'Red On':
                    self.__casu.send_message('collector', 'On')
                if self.state == 'Green On':
                    self.__casu.send_message('collector', 'On')
                if self.state == 'Blue On':
                    self.__casu.send_message('collector', 'On')
                if self.state == 'Yellow On':
                    self.__casu.send_message('collector', 'On')



    def loop(self):
        """
        Do some smart control stuff...
        """
        while True:
            self.send_msg()
            time.sleep(0.5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--rtc-path', type=str, default='',
            help="location of RTC files to configure CASUs",)
    parser.add_argument('-n', '--name', type=str, default='casu-ctr',
            help="location of RTC files to configure CASUs",)
    parser.add_argument('-v', '--verb', type=int, default=1,
            help="verbosity level")
    parser.add_argument('-d', '--dir', type=str, default='N',
            help="direction of centre")
    args = parser.parse_args()

    fname = "{}.rtc".format(args.name)
    rtc = os.path.join(args.rtc_path, fname)
    print "connecting to casu {} ('{}')".format(args.name, rtc)

    ctrl = CasuController(rtc_file=rtc, direction=args.dir)

    try:
        while True:
            ctrl.loop()
    except KeyboardInterrupt:
        # cleanup
        ctrl.stop()




