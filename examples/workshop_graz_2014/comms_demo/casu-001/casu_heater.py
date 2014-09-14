#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from assisipy import casu


heating_temp = 40
cooling_temp = 25

if __name__ == '__main__':
    
    heatcasu = casu.Casu()
    temp = heating_temp
    heatcasu.set_diagnostic_led_rgb(r=1)

    while True:
        msg = heatcasu.read_message()
        if msg:
            if 'Warm' in msg['data']:
                temp = heating_temp
                heatcasu.set_diagnostic_led_rgb(r=1)
            elif 'Cool' in msg['data']:
                temp = cooling_temp
                heatcasu.set_diagnostic_led_rgb(b=1)

        heatcasu.set_temp(temp)
        sleep(5)



