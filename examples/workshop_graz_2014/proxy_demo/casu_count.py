#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Count bees and indicate the count with diagnostic LED.
"""

import sys
from time import sleep

from assisipy import casu


def calibrate_thresholds(thiscasu, thresholds):

    num_readings = 5
    thresholds = [0 for i in range(len(thresholds))]

    print('Calibrating IR reading thresholds.')
    for i in range(num_readings):
        ir_values = thiscasu.get_ir_raw_value(casu.ARRAY)
        for k in range(len(thresholds)):
            if thresholds[k] < ir_values[k]:
                thresholds[k] = ir_values[k]
        print('Reading {0}/{1}'.format(i+1,num_readings))
        sleep(1)

    thresholds = [1.1*x for x in thresholds]

if __name__=='__main__':

    rtc = sys.argv[1]
    mycasu = casu.Casu(rtc_file_name=rtc,log=True,log_folder='logs')
    
    thresholds = mycasu.get_ir_raw_value(casu.ARRAY)
    calibrate_thresholds(mycasu, thresholds)
    print(thresholds)

    count = 0

    # NOTE: This CASU controller implementation is quite naive.
    # The sleep can not ensure a consistent sample time
    # A more sophisticated implementation would use threads.
    while True:
        red = green = blue = 0
        if mycasu.get_ir_raw_value(casu.IR_F) > thresholds[0]:
            green = 1
            count += 1
        if mycasu.get_ir_raw_value(casu.IR_B) > thresholds[3]:
            red = 1
            count +=1
        if mycasu.get_ir_raw_value(casu.IR_FR) > thresholds[1]:
            blue = 1
            count += 1
        if mycasu.get_ir_raw_value(casu.IR_BR) > thresholds[2]:
            blue = 1
            count += 1
        if mycasu.get_ir_raw_value(casu.IR_BL) > thresholds[4]:
            blue = 1
            count += 1
        if mycasu.get_ir_raw_value(casu.IR_FL) > thresholds[5]:
            blue = 1
            count += 1
        mycasu.set_diagnostic_led_rgb(r=red,g=green,b=blue)
        print('Total detection count: {0}'.format(count))
        sleep(1)
            
