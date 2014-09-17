#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A demo of using the Casu Peltier actuator for heating and cooling.
"""

import sys
from time import sleep

from assisipy import casu


if __name__ == '__main__':
    
    rtc = sys.argv[1]

    heating_temp = 36
    cooling_temp = 26
    sample_time = 5

    heatcasu = casu.Casu(rtc_file_name=rtc)
    temp = heating_temp
    heatcasu.set_diagnostic_led_rgb(r=1)

    while True:
        msg = heatcasu.read_message()
        print(msg)
        if msg:
            if 'Warm' in msg['data']:
                temp = heating_temp
                heatcasu.set_diagnostic_led_rgb(r=1)
            elif 'Cool' in msg['data']:
                temp = cooling_temp
                heatcasu.set_diagnostic_led_rgb(b=1)

        heatcasu.set_temp(temp)
        sleep(sample_time)



