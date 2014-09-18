#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple demo of Casu for using the Casu peltier actuator.
Every minute, the Casu switches its peltier actuator between heating and cooling.

While heating, the status LED is lit red, while cooling, it's lit blue.
"""

from assisipy import casu

import sys
import time
from datetime import datetime
import csv

if __name__ == '__main__':

    rtc = sys.argv[1]

    temp_values = [42,26,38,30,34]

    log_period = 1
    #log_cycles = 1200 # A cycle is about 20 minutes = 1200 seconds
    log_cycles = 5

    heater = casu.Casu(rtc_file_name=rtc)
    heater.set_diagnostic_led_rgb(r=1,b=1)

    # Open the log file
    now_str = datetime.now().__str__().split('.')[0]
    now_str = now_str.replace(' ','-').replace(':','-')
    with open('logs/'+now_str+'-'+'heat'+'.csv','wb') as logfile:
        logger = csv.writer(logfile,delimiter=';')
        logger.writerow(['time','t_ref','t1','t2','t3','t4','t5']);
        for t in temp_values:
            print('Setting temperature to {0}!'.format(t))
            heater.set_temp(t)
            for k in range(log_cycles):
                logger.writerow([time.time(),t]+heater.get_temp(casu.ARRAY))
                time.sleep(log_period)

    
