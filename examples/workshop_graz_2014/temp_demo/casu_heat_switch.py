#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple demo of Casu for using the Casu peltier actuator.
Every minute, the Casu switches its peltier actuator between heating and cooling.

While heating, the status LED is lit red, while cooling, it's lit blue.
"""

from assisipy import casu

from time import sleep

if __name__ == '__main__':

    heating_temp = 38
    cooling_temp = 25

    HEATING = 1
    COOLING = 0

    period = 60

    heater = casu.Casu(name='casu-001')
    state = COOLING
    
    while True:
        if state == COOLING:
            state = HEATING
            heater.set_temp(heating_temp)
            heater.set_diagnostic_led_rgb(r=1)
        elif state == HEATING:
            state = COOLING
            heater.set_temp(cooling_temp)
            heater.set_diagnostic_led_rgb(b=1)
        sleep(period)

    
