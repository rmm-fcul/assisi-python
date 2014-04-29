#!/usr/bin/env python
# A program for testing the heat actuator

import time
import argparse

from assisipy import casu

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Test casu heat actuator.")
    parser.add_argument('rtc_file', help='Name of the Casu rtc file.')
    args = parser.parse_args()

    Td = 1              # Sample time for checking sensor values
    T_experiment = 1800 # Total experiment duration
    N = 10              # Number of cycles for calibration

    mycasu = casu.Casu(args.rtc_file)
    
    # Calibrate the sensors
    raw_value_sums = mycasu.get_ir_raw_value(casu.ARRAY)
    for i in range(N):
        time.sleep(Td)
        raw_vals = mycasu.get_ir_raw_value(casu.ARRAY)
        for k in range(len(raw_vals)):
            raw_value_sums[k] = raw_value_sums[k] + raw_vals[k]

    thresholds = [raw_sum/(N+1) for raw_sum in raw_value_sums]
    thresholds = [thresh + 0.1*thresh for thresh in thresholds]

    time_start = time.time()
    time_now = time.time()
    while time_now - time_start < T_experiment:
        raw_vals = mycasu.get_ir_raw_value(casu.ARRAY)
        active = [False for val in raw_vals]
        for k in range(len(raw_vals)):
            active[k] = raw_vals[k] > thresholds[k]
        if True in active:
            print('Proxy sensor activity: {0}'.format(active))
            mycasu.set_diagnostic_led_rgb(g=1)
        else:
            mycasu.diagnostic_led_standby()
        time.sleep(Td)

