#!/usr/bin/env python
# A program for testing the heat actuator

import time
import argparse

from assisipy import casu

def switch_temp_ref(temp_ref, temp_high, temp_low):
    """
    Switch the temperature setpoint.
    """
    if temp_ref > temp_low:
        temp_ref = temp_low
    else:
        temp_ref = temp_high

    return temp_ref

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Test casu heat actuator.")
    parser.add_argument('rtc_file', help='Name of the Casu rtc file.')
    args = parser.parse_args()

    Td = 5              # Sample time for checking sensor values
    T_cycle = 300       # Cycle time
    T_experiment = 1800 # Total experiment duration
    temp_high = 38
    temp_low = 28

    temp_ref = temp_high

    mycasu = casu.Casu(args.rtc_file)
    
    mycasu.set_temp(temp_ref)
    print("Temperature setpoint set to {0}C".format(temp_ref))
    time_start = time.time()
    time_cycle_start = time_start
    time_now = time.time()
    while time_now - time_start < T_experiment:
        if time_now - time_cycle_start > T_cycle:
            temp_ref = switch_temp_ref(temp_ref, temp_high, temp_low)
            print("{0}s elapsed, switching temperature setpoint to {1}C".format(
                time_now - time_cycle_start, temp_ref))
            mycasu.set_temp(temp_ref)
            time_cycle_start = time_now
        
        temp_now = mycasu.get_temp(casu.TEMP_L)
        print("Current temperature: {0}".format(temp_now))
        mycasu.set_light_rgb(r = (temp_now-temp_low)/(temp_high-temp_low), 
                             b = (temp_high - temp_now)/(temp_high - temp_low)) 
        time.sleep(Td)
        time_now = time.time()
