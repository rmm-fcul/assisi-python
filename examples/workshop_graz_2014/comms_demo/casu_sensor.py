#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import sys

from assisipy import casu


if __name__ == '__main__':

    rtc = sys.argv[1]
    
    senscasu = casu.Casu(rtc_file_name=rtc)

    max_temp = 30
    min_temp = 28
    
    while True:
        temp = senscasu.get_temp(casu.TEMP_R)
        print('Temperature on EAST sensor: {0}'.format(temp));
        if temp > max_temp:
            senscasu.send_message('east','Cool down you maniac!')
            print('Temperature too hot!')
            senscasu.set_diagnostic_led_rgb(r=1)
        elif temp < min_temp:
            senscasu.send_message('east','Warm up!')
            print('Temperature too low!')
            senscasu.set_diagnostic_led_rgb(b=1)
        else:
            senscasu.set_diagnostic_led_rgb(g=1)
        sleep(5)

