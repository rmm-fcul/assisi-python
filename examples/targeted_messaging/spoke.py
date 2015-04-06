#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
for all "spoke" CASUs, they emit when reading one specific directional
IR sensor.

set the direction that is sensed by the -d flag, from NESW

'''

from assisipy import casu
import argparse, os
import time

class CasuController:

    def __init__(self, rtc_file, direction, verb=False):
        self.__casu = casu.Casu(rtc_file)
        self._ctr_dir = direction
        self.old_state = 'Off'
        self.state = 'Off'
        self.verb = verb

    def stop(self):
        self.__casu.stop()
            
    def send_msg(self):

        while True:
            # North side => yellow
            if self._ctr_dir == 'N' and  self.__casu.get_range(casu.IR_N) < 2:
                self.__casu.set_diagnostic_led_rgb(1, 1, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Yellow On'
            # East => red
            elif self._ctr_dir == 'E' and ((self.__casu.get_range(casu.IR_NE) <
                2 or self.__casu.get_range(casu.IR_SE) < 2)):
                self.__casu.set_diagnostic_led_rgb(1, 0, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Red On'
            # South => blue
            elif self._ctr_dir == 'S' and self.__casu.get_range(casu.IR_S) < 2:
                self.__casu.set_diagnostic_led_rgb(0, 0, 1, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Blue On'
            # West => green
            elif self._ctr_dir == 'W' and ((self.__casu.get_range(casu.IR_SW) <
                2 or self.__casu.get_range(casu.IR_NW) < 2)):
                self.__casu.set_diagnostic_led_rgb(0, 1, 0, casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Green On'
            else:
                self.__casu.diagnostic_led_standby(casu.DLED_TOP)
                self.old_state = self.state
                self.state = 'Off'

            if self.old_state != self.state:
                if self.old_state in ['Red On', 'Green On', 'Blue On', 
                        'Yellow On']:
                    self.__casu.send_message('collector', 'Off')

                if self.state in ['Red On', 'Green On', 'Blue On', 
                        'Yellow On']:
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

    ctrl = CasuController(rtc_file=rtc, direction=args.dir, verb=args.verb)

    try:
        while True:
            ctrl.loop()
    except KeyboardInterrupt:
        # cleanup
        ctrl.stop()




