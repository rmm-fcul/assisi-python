#!/usr/bin/env python
# A program for testing the heat actuator

import time
import argparse

from assisipy import casu

def vibe_ref_step(vibe_ref, vibe_low, vibe_high, step, step_dir):
    """
    Switch the temperature setpoint.
    """
    vibe_ref = vibe_ref + step_dir*step
    if (vibe_ref > vibe_high) or (vibe_ref < vibe_low):
        step_dir = -1*step_dir
        vibe_ref = vibe_ref = vibe_ref + 2*step_dir*step

    return vibe_ref,step_dir

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Test casu heat actuator.")
    parser.add_argument('rtc_file', help='Name of the Casu rtc file.')
    args = parser.parse_args()

    Td = 10             # Sample time updating motor speed
    T_experiment = 1800 # Total experiment duration
    vibe_low = 0
    vibe_high = 500.0
    vibe_step = 10.0
    step_dir = 1

    mycasu = casu.Casu(args.rtc_file)
    
    time_start = time.time()
    time_now = time.time()
    vibe_ref = 0
    while time_now - time_start < T_experiment:
        (vibe_ref,step_dir) = vibe_ref_step(vibe_ref, vibe_low, vibe_high, vibe_step, step_dir)
        mycasu.set_vibration_freq(vibe_ref)
        print("Current vibration frequency: {0}".format(vibe_ref))
        mycasu.set_diagnostic_led_rgb(r = (vibe_ref-vibe_low)/(vibe_high-vibe_low), 
                                      b = (vibe_high - vibe_ref)/(vibe_high - vibe_low))
        time.sleep(Td)
        time_now = time.time()
